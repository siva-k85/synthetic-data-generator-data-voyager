# Attribution Analysis Report

## Population Summary
- **Total Patients**: 1,129
- **Successfully Attributed**: 996 (88.2%)
- **Unattributed**: 133 (11.8%)
- **Low Confidence (<50%)**: 34 (3.0%)

## Attribution Quality Metrics

### Success Rate
- **Primary Metric**: 88.2% of patients successfully attributed to a PCP
- **Benchmark**: Target is >80% attribution rate for population health management
- **Status**: ✅ MEETS TARGET

### Confidence Distribution
- **High Confidence (>70%)**: 446 patients
- **Medium Confidence (50-70%)**: 516 patients
- **Low Confidence (<50%)**: 34 patients

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
- **Simulation Date Range**: Historical data through 2025-11-14
- **Lookback Period**: 730 days (24 months)

---
*Generated: 2025-11-19 12:31:12*
