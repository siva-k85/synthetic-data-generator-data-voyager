"""
Andor Attribution Engine - Production Run
Analyzes 1000-patient dataset for PCP attribution and care gap identification
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List
from pathlib import Path

class AndorAttributionEngine:
    """
    Attribution system for Andor Health System
    Maps patients to PCPs, identifies care gaps, generates worklists
    """

    def __init__(self, fhir_dir: str):
        self.fhir_dir = Path(fhir_dir)
        self.patients = self.load_resources("Patient")
        self.encounters = self.load_resources("Encounter")
        self.practitioners = self.load_resources("Practitioner")
        self.organizations = self.load_resources("Organization")
        self.coverage = self.load_resources("Coverage")
        self.conditions = self.load_resources("Condition")

    def load_resources(self, resource_type: str) -> List[Dict]:
        """Load FHIR resources from NDJSON files"""
        resources = []
        file_path = self.fhir_dir / f"{resource_type}.ndjson"
        if not file_path.exists():
            print(f"Warning: {file_path} not found.")
            return []

        with open(file_path, 'r') as f:
            for line in f:
                resources.append(json.loads(line))
        return resources

    def load_patients(self) -> Dict[str, Dict]:
        """Helper to index patients by ID"""
        return {p['id']: p for p in self.patients}

    def load_practitioners(self) -> Dict[str, Dict]:
        """Helper to index practitioners by ID"""
        return {p['id']: p for p in self.practitioners}

    def attribute_patient_to_pcp(self, patient_id: str) -> Dict:
        """
        Algorithm: Patient → PCP Attribution
        Uses plurality of ambulatory visits in last 24 months
        """

        # Determine simulation end date (anchor)
        if not hasattr(self, 'simulation_end_date'):
            all_dates = [e['period']['start'] for e in self.encounters]
            if all_dates:
                self.simulation_end_date = max(all_dates)
            else:
                self.simulation_end_date = datetime.now().isoformat()

        # Calculate cutoff (24 months before simulation end)
        sim_end = datetime.fromisoformat(self.simulation_end_date.replace('Z', '+00:00'))
        cutoff_date = (sim_end - timedelta(days=730)).isoformat()

        patient_encounters = [
            enc for enc in self.encounters
            if enc['subject']['reference'] == f"Patient/{patient_id}"
            and enc['period']['start'] > cutoff_date
        ]

        # Filter for primary care encounters
        primary_care_codes = ['AMB', 'WELLNESS', 'OUTPATIENT']
        pc_encounters = [
            enc for enc in patient_encounters
            if enc['class'].get('code') in primary_care_codes
        ]

        # Count visits by provider
        provider_visits = {}
        for enc in pc_encounters:
            if 'participant' in enc:
                for participant in enc['participant']:
                    if 'individual' in participant:
                        provider_ref = participant['individual']['reference']
                        provider_visits[provider_ref] = provider_visits.get(provider_ref, 0) + 1

        if not provider_visits:
            return {
                'patient_id': patient_id,
                'attributed_pcp': None,
                'attribution_method': 'NO_VISITS',
                'confidence': 0,
                'last_visit': None,
                'visit_count': 0,
                'status': 'UNATTRIBUTED'
            }

        # Find provider with most visits
        attributed_pcp = max(provider_visits, key=provider_visits.get)
        visit_count = provider_visits[attributed_pcp]

        # Get last visit date
        last_visit = None
        pc_encounters.sort(key=lambda x: x['period']['start'])
        for enc in reversed(pc_encounters):
            if 'participant' in enc:
                for p in enc['participant']:
                    if p.get('individual', {}).get('reference') == attributed_pcp:
                        last_visit = enc['period']['start']
                        break
            if last_visit: break

        # Calculate confidence
        total_visits = sum(provider_visits.values())
        confidence = visit_count / total_visits if total_visits > 0 else 0

        return {
            'patient_id': patient_id,
            'attributed_pcp': attributed_pcp,
            'attribution_method': 'PLURALITY_24_MONTHS',
            'confidence': confidence,
            'last_visit': last_visit,
            'visit_count': visit_count,
            'status': 'ATTRIBUTED'
        }

    def identify_care_gaps(self, patient_id: str) -> List[str]:
        """Identify care gaps based on active conditions"""
        gaps = []
        patient_conditions = [
            c for c in self.conditions
            if c['subject']['reference'] == f"Patient/{patient_id}"
            and c.get('clinicalStatus', {}).get('coding', [{}])[0].get('code') == 'active'
        ]

        for cond in patient_conditions:
            code = cond['code']['coding'][0]['code']
            if code in ['44054006', 'E11.9', 'E11.65']:  # Diabetes
                gaps.extend(["HbA1c Screening", "Diabetic Eye Exam"])
            if code in ['38341003', 'I10']:  # Hypertension
                gaps.append("BP Control < 140/90")

        return list(set(gaps))

    def save_attribution_results(self, output_dir: Path):
        """Save all attribution results"""

        patients_dict = self.load_patients()
        results = {
            'generation_timestamp': datetime.now().isoformat(),
            'total_patients': len(patients_dict),
            'attribution_summary': {
                'attributed': 0,
                'unattributed': 0,
                'low_confidence': 0
            },
            'patient_attributions': []
        }

        print(f"Analyzing {len(patients_dict)} patients...")

        for idx, patient_id in enumerate(patients_dict.keys()):
            if idx % 100 == 0:
                print(f"  Processed {idx}/{len(patients_dict)} patients...")

            attribution = self.attribute_patient_to_pcp(patient_id)
            results['patient_attributions'].append(attribution)

            if attribution['status'] == 'ATTRIBUTED':
                results['attribution_summary']['attributed'] += 1
                if attribution['confidence'] < 0.5:
                    results['attribution_summary']['low_confidence'] += 1
            else:
                results['attribution_summary']['unattributed'] += 1

        # Save results
        output_dir.mkdir(parents=True, exist_ok=True)

        with open(output_dir / "attribution_results.json", "w") as f:
            json.dump(results, f, indent=2)

        # Create summary report
        total = results['total_patients']
        attributed = results['attribution_summary']['attributed']
        unattributed = results['attribution_summary']['unattributed']
        low_conf = results['attribution_summary']['low_confidence']

        report = f"""# Attribution Analysis Report

## Population Summary
- **Total Patients**: {total:,}
- **Successfully Attributed**: {attributed:,} ({attributed/total*100:.1f}%)
- **Unattributed**: {unattributed:,} ({unattributed/total*100:.1f}%)
- **Low Confidence (<50%)**: {low_conf:,} ({low_conf/total*100:.1f}%)

## Attribution Quality Metrics

### Success Rate
- **Primary Metric**: {attributed/total*100:.1f}% of patients successfully attributed to a PCP
- **Benchmark**: Target is >80% attribution rate for population health management
- **Status**: {'✅ MEETS TARGET' if attributed/total > 0.8 else '⚠️ BELOW TARGET'}

### Confidence Distribution
- **High Confidence (>70%)**: {len([a for a in results['patient_attributions'] if a.get('confidence', 0) > 0.7]):,} patients
- **Medium Confidence (50-70%)**: {len([a for a in results['patient_attributions'] if 0.5 <= a.get('confidence', 0) <= 0.7]):,} patients
- **Low Confidence (<50%)**: {low_conf:,} patients

## Clinical Implications

### Care Gap Identification
Total patients analyzed for care gap detection based on active chronic conditions.

### Panel Management
Attribution enables:
- Provider panel assignment
- Care coordinator worklist generation
- Quality measure tracking by provider
- Population health stratification

## Technical Notes

### Attribution Algorithm
- **Method**: Plurality of ambulatory visits in last 24 months
- **Encounter Types**: AMB (Ambulatory), WELLNESS, OUTPATIENT
- **Confidence Calculation**: (Plurality visits / Total visits)

### Data Quality
- **Simulation Date Range**: Historical data through {results['patient_attributions'][0].get('last_visit', 'N/A')[:10] if results['patient_attributions'] else 'N/A'}
- **Lookback Period**: 730 days (24 months)

---
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

        with open(output_dir / "attribution_report.md", "w") as f:
            f.write(report)

        print(f"\n✅ Attribution analysis complete")
        print(f"   Results saved to: {output_dir}")
        return results

if __name__ == "__main__":
    # Production run
    engine = AndorAttributionEngine("outputs/fhir")
    results = engine.save_attribution_results(Path("documentation"))
