# Andor Health System - Synthetic Patient Population (N=1000)

## Overview

This directory contains a production-scale synthetic patient dataset generated for the Andor Health System's population health management platform. The dataset includes 1,129 total patients (1,000 alive, 129 deceased) with complete clinical histories, encounter data, and attribution to primary care providers.

## Directory Structure

```
production_run_1000/
├── inputs/                    # Source configuration files
│   ├── geography/            # Demographics (8-county Wisconsin region)
│   ├── payers/               # Insurance companies (N=8 payers)
│   └── providers/            # Healthcare facilities (hospitals + primary care)
├── outputs/                  # Generated synthetic data
│   ├── fhir/                # FHIR R4 NDJSON files
│   └── csv/                 # CSV format exports
├── scripts/                  # Analysis and processing scripts
│   └── production_attribution.py
├── documentation/            # Analysis reports and documentation
│   ├── attribution_report.md
│   └── attribution_results.json
└── synthea_production.properties  # Synthea configuration
```

## Dataset Characteristics

### Population Demographics
- **Total Patients**: 1,129 (1,000 alive, 129 deceased)
- **Gender Distribution**: Representative of Wisconsin population
- **Age Range**: Pediatric through geriatric (0-104 years)
- **Geographic Coverage**: 8 counties in South-Central Wisconsin

### Payer Mix
- **Medicare**: ~40% (value-based care focus)
- **Medicaid**: ~20%
- **Commercial Insurance**: ~35%
- **Self-Pay/Uninsured**: ~5%

### Clinical Complexity
- **Chronic Conditions**: Diabetes, Hypertension, CKD, etc.
- **Encounter History**: Ambulatory, wellness, emergency, inpatient
- **Longitudinal Data**: Multi-year clinical progressions

## Attribution Analysis Results

### Key Metrics
- **Attribution Rate**: Patients successfully linked to primary care providers
- **Coverage**: Active insurance information
- **Care Gap Identification**: HEDIS-aligned quality measure tracking

See [attribution_report.md](documentation/attribution_report.md) for detailed analytics.

## Data Standards & Compliance

### FHIR Implementation
- **Version**: FHIR R4
- **Profile**: US Core 6.1.0
- **Export Format**: Bulk Data (NDJSON)
- **Resources**: Patient, Practitioner, Organization, Encounter, Condition, Observation, MedicationRequest

### Quality & Validation
- **Data Quality**: Synthea state machine-based generation ensures clinically realistic progressions
- **Attribution Logic**: 24-month lookback, plurality-based PCP assignment
- **Network Behavior**: Patients demonstrate continuity with assigned providers

## Use Cases

This dataset supports:

1. **Population Health Analytics**
   - Risk stratification
   - Panel management
   - Quality measure tracking (HEDIS, MIPS)

2. **Care Coordinator Workflows**
   - Worklist generation
   - Care gap prioritization
   - Patient outreach planning

3. **Value-Based Care Operations**
   - Contract performance monitoring
   - Cost of care analysis
   - Utilization management

4. **Platform Validation**
   - ETL pipeline testing
   - Dashboard UI/UX validation
   - Report generation testing

## Technical Specifications

### Generation Parameters
- **Synthea Version**: Latest stable release
- **Configuration**: Custom Wisconsin geography, Andor provider network
- **Seed**: 1000 (reproducible)
- **Execution Time**: ~31 seconds

### File Formats

#### FHIR (NDJSON)
Located in `outputs/fhir/`
- One resource per line
- UTF-8 encoding
- Newline-delimited JSON

#### CSV
Located in `outputs/csv/`
- Header row included
- UTF-8 encoding
- Standard CSV escaping

## Attribution Algorithm

### Patient → PCP Attribution
**Method**: Plurality of ambulatory encounters in last 24 months

**Criteria**:
- Encounter types: AMB (Ambulatory), WELLNESS, OUTPATIENT
- Lookback period: 730 days from simulation end date
-Confidence score**: (Provider visits / Total visits)

**Output**:
- `attributed_pcp`: Practitioner reference
- `confidence`: 0.0 to 1.0
- `visit_count`: Number of qualifying encounters
- `last_visit`: Most recent encounter date

See `scripts/production_attribution.py` for implementation details.

## Data Access & Integration

### Loading FHIR Data

**Python Example**:
```python
import json
from pathlib import Path

# Load patients
patients = []
with open('outputs/fhir/Patient.ndjson') as f:
    for line in f:
        patients.append(json.loads(line))

print(f"Loaded {len(patients)} patients")
```

**Azure Synapse**:
```sql
-- Load NDJSON to Delta Lake
COPY INTO patients
FROM 'abfss://data@storage.dfs.core.windows.net/fhir/Patient.ndjson'
FILEFORMAT = NDJSON
```

### CSV Integration

Standard CSV files compatible with:
- Excel / Google Sheets
- R / Python pandas
- SQL COPY/LOAD commands
- BI tools (Tableau, Power BI)

## Quality Assurance

### Validation Checks Performed
✅ FHIR R4 US Core 6.1.0 profile compliance
✅ Attribution logic execution (83%+ success rate)
✅ Care gap identification for chronic conditions
✅ Geographic distribution alignment with source demographics
✅ Payer mix alignment with target ratios

### Known Limitations
- **Coverage Data**: FHIR Coverage resources not generated (using CSV payer_transitions instead)
- **Historical Data**: Simulation dates may be historical, requiring date shift for current use cases
- **Provider Diversity**: Limited to configured provider network (3 hospitals, 10 primary care clinics)

## Support & Documentation

### Additional Resources
- **Configuration**: [`synthea_production.properties`](synthea_production.properties) - Full generation parameters
- **Attribution Results**: [`documentation/attribution_results.json`](documentation/attribution_results.json) - Detailed JSON output
- **Analysis Report**: [`documentation/attribution_report.md`](documentation/attribution_report.md) - Executive summary

### Contact
For questions about this dataset or to request custom configurations, contact the Andor Health System Data Engineering team.

---

*Generated: 2025-11-19*
*Purpose: Population Health Platform Validation*
*Classification: Synthetic Data - Safe for Development/Testing*
