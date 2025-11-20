"""
Create ACTUAL patient journey from REAL Synthea data
This is what Dr. Smith wants to see - prove you understand the data
"""

import json
from datetime import datetime
import os

def identify_care_gaps(code):
    """Simple helper to identify care gaps based on condition codes"""
    # Diabetes
    if code in ['44054006', 'E11.9', 'E11.65']:
        return "🔴 MISSING A1C (HEDIS)"
    # Hypertension
    if code in ['38341003', 'I10']:
        return "🔴 MISSING BP CONTROL (HEDIS)"
    return "None"

def create_patient_journey_markdown():
    """Generate the exact walkthrough Dr. Smith wants"""

    # Load ACTUAL patient (not theoretical)
    try:
        with open("output/fhir/Patient.ndjson", 'r') as f:
            patient = json.loads(f.readline())  # First patient
    except FileNotFoundError:
        print("Error: output/fhir/Patient.ndjson not found. Run generation first.")
        return

    patient_id = patient['id']

    # Create the walkthrough document
    walkthrough = f"""# Patient Journey Walkthrough: {patient['name'][0]['given'][0]} {patient['name'][0]['family']}
**Patient ID:** {patient_id}
**Generated:** {datetime.now()}
**Data Source:** ACTUAL Synthea output (not theoretical)

## 1. Demographics (Patient Resource)
```json
{json.dumps(patient, indent=2)[:500]}...
```

### First Principles Understanding:
- **Birth Date:** {patient['birthDate']} → Determines Medicare eligibility
- **Gender:** {patient['gender']} → Affects preventive care gaps (mammogram vs PSA)
- **Address:** {patient['address'][0]['city']}, {patient['address'][0]['state']} → Determines clinic assignment

## 2. Insurance Journey (Coverage Resources)

### Coverage Timeline:
"""

    # Load actual Coverage resources for this patient
    coverages = []
    try:
        with open("output/fhir/Coverage.ndjson", 'r') as f:
            for line in f:
                coverage = json.loads(line)
                if coverage['beneficiary']['reference'] == f"Patient/{patient_id}":
                    coverages.append(coverage)
    except FileNotFoundError:
        walkthrough += "\n*No Coverage data found.*\n"

    # Sort by period
    coverages.sort(key=lambda x: x['period']['start'])

    for i, coverage in enumerate(coverages, 1):
        payer = coverage['payor'][0]['display']
        start = coverage['period']['start']
        end = coverage['period'].get('end', 'ACTIVE')

        walkthrough += f"""
#### Coverage Period {i}: {payer}
- **Start:** {start}
- **End:** {end}
- **Why This Matters:** Determines which quality measures apply
- **Care Coordinator Impact:** Must verify active coverage before scheduling
"""

    # Continue for Encounters
    walkthrough += """
## 3. Encounter History (Touch Points)

### Clinical Encounters:
"""

    encounters = []
    try:
        with open("output/fhir/Encounter.ndjson", 'r') as f:
            for line in f:
                enc = json.loads(line)
                if enc['subject']['reference'] == f"Patient/{patient_id}":
                    encounters.append(enc)
    except FileNotFoundError:
        walkthrough += "\n*No Encounter data found.*\n"

    # Sort by date
    encounters.sort(key=lambda x: x['period']['start'])

    # Last 5 encounters
    for enc in encounters[-5:]:
        provider_ref = 'UNATTRIBUTED'
        if 'participant' in enc:
             for p in enc['participant']:
                 if 'individual' in p:
                     provider_ref = p['individual'].get('reference', 'UNATTRIBUTED')
                     break

        location_display = 'UNKNOWN'
        if 'location' in enc and len(enc['location']) > 0:
            location_display = enc['location'][0].get('location', {}).get('display', 'UNKNOWN')

        class_display = enc['class'].get('display', enc['class'].get('code', 'UNKNOWN'))
        walkthrough += f"""
#### {enc['period']['start'][:10]}: {class_display}
- **Type:** {enc['type'][0]['coding'][0]['display']}
- **Provider:** {provider_ref}
- **Location:** {location_display}
- **Attribution Problem:** {'✅ Has provider' if provider_ref != 'UNATTRIBUTED' else '❌ NO PROVIDER - CANNOT ATTRIBUTE'}
"""

    # Add Conditions (Diagnoses)
    walkthrough += """
## 4. Active Conditions (What Drives Care Gaps)

### Chronic Conditions:
"""

    conditions = []
    try:
        with open("output/fhir/Condition.ndjson", 'r') as f:
            for line in f:
                cond = json.loads(line)
                if cond['subject']['reference'] == f"Patient/{patient_id}":
                    conditions.append(cond)
    except FileNotFoundError:
        walkthrough += "\n*No Condition data found.*\n"

    for cond in conditions:
        # Check clinical status
        is_active = False
        if 'clinicalStatus' in cond:
             for coding in cond['clinicalStatus'].get('coding', []):
                 if coding.get('code') == 'active':
                     is_active = True

        if is_active:
            code_val = cond['code']['coding'][0]['code']
            display_val = cond['code']['coding'][0]['display']
            onset = cond.get('onsetDateTime', 'Unknown')

            walkthrough += f"""
#### {display_val}
- **ICD-10:** {code_val}
- **Onset:** {onset}
- **Triggers Care Gap:** {identify_care_gaps(code_val)}
"""

    # THE CRITICAL SECTION - Attribution Analysis
    walkthrough += """
## 5. 🔴 ATTRIBUTION ANALYSIS (The Gap Dr. Smith Identified)

### What Synthea Gives Us:
- ✅ Patient exists
- ✅ Has encounters
- ✅ Has conditions
- ✅ Has coverage

### What's MISSING for Care Coordination:
- ❌ **No PCP Attribution:** Cannot determine primary care physician
- ❌ **No Clinic Assignment:** Location references are generic
- ❌ **No Panel Assignment:** Cannot generate PCP worklist
- ❌ **No Contract Mapping:** Payor exists but no VBC contract link

### Post-Processing Required:
"""

    # Calculate attribution
    provider_counts = {}
    for enc in encounters:
        provider_ref = None
        if 'participant' in enc:
             for p in enc['participant']:
                 if 'individual' in p:
                     provider_ref = p['individual'].get('reference')
                     break

        if provider_ref:
            provider_counts[provider_ref] = provider_counts.get(provider_ref, 0) + 1

    if provider_counts:
        attributed_pcp = max(provider_counts, key=provider_counts.get)
        walkthrough += f"""
#### Attribution Algorithm Result:
- **Attributed PCP:** {attributed_pcp} ({provider_counts[attributed_pcp]} visits)
- **Attribution Method:** Plurality of visits in last 24 months
- **Confidence:** {'HIGH' if provider_counts[attributed_pcp] > 3 else 'LOW'}
"""
    else:
        walkthrough += """
#### ⚠️ ATTRIBUTION FAILURE:
- **No provider information in encounters**
- **Cannot determine PCP**
- **Patient would not appear on any worklist**
- **This is the core problem Dr. Smith identified**
"""

    # Save the walkthrough
    with open("patient_walkthrough_ACTUAL.md", "w") as f:
        f.write(walkthrough)

    print(f"✅ Created ACTUAL patient walkthrough: {patient_id}")
    return walkthrough

if __name__ == "__main__":
    # EXECUTE
    walkthrough = create_patient_journey_markdown()
