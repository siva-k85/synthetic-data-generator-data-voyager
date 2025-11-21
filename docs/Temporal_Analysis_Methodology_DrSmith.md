# Temporal Analysis Approach: Dr. Smith's Methodology

## Base Synthea & Andor Health System Implementation

---

## Executive Summary

Dr. Smith's temporal analysis methodology employs a **first-principles approach** to longitudinal patient data analysis, focusing on extracting actionable insights from chronologically sequenced clinical events. The approach emphasizes care continuity assessment, quality gap detection, and attribution logic across temporal boundaries.

---

## Part 1: Base Synthea Temporal Analysis

### 1.1 Data Extraction & Timeline Construction

#### Core Principle: Comprehensive Event Collection

The temporal analysis begins by parsing the Wisconsin Baseline v3.0 FHIR dataset to collect **all temporal markers** for each patient. Dr. Smith's approach requires:

```python
# Resource types for temporal extraction (in priority order)
TEMPORAL_RESOURCES = [
    'encounters.csv',      # Primary care touchpoints
    'conditions.csv',      # Disease onset markers
    'procedures.csv',      # Intervention points
    'observations.csv',     # Clinical measurements
    'medications.csv',     # Therapy initiation/changes
    'payer_transitions.csv' # Insurance coverage changes
]
```

#### Timeline Assembly Process

1. **Patient-Specific Filtering**: Extract all records matching patient UUID (e.g., `624c651e-8c7c-48e5-8ff5-4df3f219d24c`)
2. **Date Normalization**: Parse START, DATE, or END fields using ISO format
3. **Event Characterization**: Create tuples of `(date, resource_type, description, clinical_value)`
4. **Chronological Sorting**: Order events by datetime to create integrated timeline

### 1.2 Clinical Event Categorization

#### Encounter Classification Hierarchy

```
ENCOUNTERS:
├── AMB (Ambulatory/Outpatient) → Routine primary care
├── EMER (Emergency) → Acute care events
├── IMP (Inpatient) → Hospitalizations
├── WELLNESS → Annual wellness visits
└── URGENTCARE → Urgent care visits
```

#### Temporal Event Patterns

Dr. Smith identifies five critical temporal patterns:

1. **Chronic Condition Progression**
   - Prediabetes (2010) → Type 2 Diabetes (2014) → Complications (2019)
   - Tracked via condition onset dates and HbA1c trajectories

2. **Preventive Care Cadence**
   - Annual wellness visits (AWV) presence/absence
   - Screening intervals (mammography, colonoscopy)
   - Immunization schedules

3. **Acute Event Sequences**

   ```
   Emergency Admission → Inpatient Stay → Procedure → Discharge → Follow-up
   (2019-11-05)        (2019-11-06)    (2019-11-07) (2019-11-10) (2019-11-24)
   ```

4. **Care Gaps**
   - Defined as periods > 365 days without qualifying ambulatory encounters
   - Maximum identified gap: 2.5 years (2016-2018)

5. **Payer Transitions**
   - Commercial → Medicare at age 65
   - Impacts quality measure applicability

### 1.3 Gap Analysis Methodology

#### Gap Detection Algorithm

```python
def detect_care_gaps(timeline):
    gaps = []
    last_encounter = None

    for event in timeline:
        if event['type'] == 'ambulatory':
            if last_encounter:
                days_between = (event['date'] - last_encounter).days
                if days_between > 365:
                    gaps.append({
                        'start': last_encounter,
                        'end': event['date'],
                        'duration_days': days_between,
                        'severity': classify_gap_severity(days_between)
                    })
            last_encounter = event['date']

    return gaps

def classify_gap_severity(days):
    if days > 730:  # 2+ years
        return 'CRITICAL'
    elif days > 540:  # 1.5+ years
        return 'HIGH'
    elif days > 365:  # 1+ year
        return 'MODERATE'
    return 'LOW'
```

### 1.4 eCQM-Relevant Temporal Analysis

#### CMS122 - Diabetes HbA1c Control

**Temporal Requirements:**

- Measurement frequency: Every 3-6 months for controlled, every 3 months for uncontrolled
- Most recent value determines measure status
- Patient Abe's trajectory: 6.8% (2011) → 8.1% (2020) → Controlled but worsening

#### CMS2 - Depression Screening

**Temporal Logic:**

- Annual screening required for patients without active depression
- Once diagnosed (2021), patient exits screening population
- Follow-up plan must be documented within 2 weeks of positive screen

#### CMS165 - Blood Pressure Control

**Temporal Assessment:**

- Most recent reading determines control status
- Abe's last reading: 142/95 (above 140/90 threshold)
- Requires intervention intensification

---

## Part 2: Andor Health System Temporal Analysis

### 2.1 Multi-Phase Temporal Configuration

#### Phase 1: Baseline Without PCP Attribution

**Temporal Setup:**

```properties
# Fixed seed for temporal reproducibility
seed = 12345

# Temporal boundaries
generate.start_date = 2020-01-01
generate.end_date = 2025-12-31

# No prospective PCP attribution
generate.providers.assignment = retrospective
```

**Purpose**: Establish natural temporal patterns without forced provider relationships

#### Phase 2: PCP Attribution via Temporal Plurality

**Attribution Algorithm:**

```python
def attribute_pcp_temporal(patient_id, encounters):
    """
    Dr. Smith's plurality attribution with temporal weighting
    """
    provider_scores = {}

    for encounter in encounters:
        if is_qualifying_encounter(encounter):
            provider = encounter['provider_id']

            # Base count
            if provider not in provider_scores:
                provider_scores[provider] = {
                    'count': 0,
                    'last_visit': None,
                    'continuity_score': 0
                }

            provider_scores[provider]['count'] += 1

            # Recency bonus (decaying weight over time)
            days_ago = (datetime.now() - encounter['date']).days
            recency_weight = 1.0 / (1 + days_ago/365)  # Yearly decay
            provider_scores[provider]['continuity_score'] += recency_weight

            # Update last visit
            if not provider_scores[provider]['last_visit'] or \
               encounter['date'] > provider_scores[provider]['last_visit']:
                provider_scores[provider]['last_visit'] = encounter['date']

    # Select PCP: Highest continuity score wins
    return max(provider_scores.items(),
               key=lambda x: x[1]['continuity_score'])[0]
```

### 2.2 Temporal Analysis Across Care Settings

#### Specialty Care Temporal Patterns

```
PRIMARY CARE          SPECIALTY CARE         EMERGENCY/HOSPITAL
     │                      │                        │
     ├─[Referral]──────────>│                        │
     │                      ├─[Consultation]         │
     │<─────[Report]────────┤                        │
     │                      │                        │
     │                      │<────[Admission]────────┤
     │<──────────────────[Discharge Summary]─────────┤
     │                                               │
     └─[Follow-up within 7-30 days]                  │
```

#### Out-of-System Care Temporal Tracking

1. **Cerner Community Hospital Integration**
   - HIE feeds provide encounter notifications
   - 48-72 hour lag for clinical data
   - Temporal alignment via encounter timestamps

2. **Snowbird Population**
   - Seasonal gaps (November-March)
   - Claims data provides 3-6 month delayed visibility
   - Requires temporal interpolation for quality measures

### 2.3 Temporal Cohort Definitions

#### High-Risk Patient Temporal Criteria

```sql
-- Dr. Smith's high-risk temporal identification
WITH patient_events AS (
    SELECT
        patient_id,
        COUNT(CASE WHEN encounter_type = 'EMERGENCY'
                   AND encounter_date >= CURRENT_DATE - INTERVAL '12 months'
              THEN 1 END) as ed_visits_12mo,
        COUNT(CASE WHEN encounter_type = 'INPATIENT'
                   AND encounter_date >= CURRENT_DATE - INTERVAL '12 months'
              THEN 1 END) as admissions_12mo,
        MAX(hcc_score) as current_hcc_score,
        COUNT(DISTINCT chronic_condition) as chronic_count
    FROM patient_timeline
    GROUP BY patient_id
)
SELECT
    patient_id,
    CASE
        WHEN ed_visits_12mo >= 3 OR admissions_12mo >= 2 THEN 'CRITICAL'
        WHEN current_hcc_score > 3.5 THEN 'HIGH'
        WHEN chronic_count >= 3 THEN 'MODERATE'
        ELSE 'LOW'
    END as risk_tier,
    ed_visits_12mo + (admissions_12mo * 3) as utilization_score
FROM patient_events;
```

### 2.4 Temporal Quality Measure Windows

#### Measurement Period Alignment

```
CALENDAR YEAR          PAYER YEAR           REPORTING PERIOD
Jan 1 - Dec 31        Jul 1 - Jun 30       Varies by contract
      │                     │                      │
      ├─Q1──┬─Q2──┬─Q3──┬─Q4                      │
             │                                     │
             └─────Payer Year Start                │
                                                   │
                        90-day run-out period──────┘
```

#### Temporal Compliance Windows

1. **Annual Requirements**
   - AWV: Once per calendar year
   - HbA1c: 2x/year minimum for diabetics
   - Depression screening: Annual if no diagnosis

2. **Post-Discharge Requirements**
   - Follow-up within 7 days (TCM billing)
   - Medication reconciliation within 48 hours
   - Care plan transmission within 24 hours

3. **Preventive Care Schedules**
   - Mammography: Every 2 years (age 50-74)
   - Colonoscopy: Every 10 years (age 45+)
   - DEXA scan: Every 2 years (women 65+)

---

## Part 3: Advanced Temporal Analytics

### 3.1 Longitudinal Pattern Recognition

#### Disease Progression Modeling

```python
def analyze_disease_progression(patient_timeline):
    """
    Identify temporal patterns in disease evolution
    """
    progression_markers = []

    # Extract condition onsets
    conditions = patient_timeline[patient_timeline['type'] == 'condition']

    # Identify progression sequences
    if 'prediabetes' in conditions['description'].values:
        prediabetes_onset = conditions[
            conditions['description'].contains('prediabetes')
        ]['date'].min()

        if 'diabetes' in conditions['description'].values:
            diabetes_onset = conditions[
                conditions['description'].contains('diabetes')
            ]['date'].min()

            progression_time = (diabetes_onset - prediabetes_onset).days / 365
            progression_markers.append({
                'sequence': 'prediabetes->diabetes',
                'years_to_progress': progression_time,
                'preventable': progression_time > 2  # Could have been prevented
            })

    return progression_markers
```

### 3.2 Care Coordination Temporal Metrics

#### Transition Success Scoring

```python
def score_care_transition(discharge_date, follow_up_date, readmission_check_date):
    """
    Dr. Smith's transition quality scoring
    """
    score = 100

    # Follow-up timeliness
    days_to_followup = (follow_up_date - discharge_date).days
    if days_to_followup <= 7:
        score += 20  # Bonus for TCM window
    elif days_to_followup <= 14:
        score += 10
    elif days_to_followup <= 30:
        score += 0
    else:
        score -= 20  # Penalty for delayed follow-up

    # Readmission check
    if readmission_occurred_within_30_days:
        score -= 40

    return min(max(score, 0), 100)  # Bound 0-100
```

### 3.3 Temporal Attribution Hierarchies

#### Multi-Level Attribution Timeline

```
PATIENT LEVEL          PROVIDER LEVEL         SYSTEM LEVEL
     │                      │                      │
T0 ──┼─ Initial PCP         │                      │
     │  Assignment          │                      │
T1 ──┼──────────────────────┼─ Provider joins     │
     │                      │  practice            │
T2 ──┼─ Care transition ────┼──────────────────────┼─ ACO formation
     │                      │                      │
T3 ──┼─ PCP change ─────────┼─ Provider           │
     │                      │  specialty change    │
T4 ──┼──────────────────────┼──────────────────────┼─ Payer contract
     │                      │                      │  renewal
```

---

## Part 4: Implementation Requirements

### 4.1 Temporal Data Quality Checks

```python
def validate_temporal_integrity(timeline):
    """
    Dr. Smith's temporal data quality validation
    """
    issues = []

    # Check for impossible sequences
    for i in range(1, len(timeline)):
        if timeline[i]['date'] < timeline[i-1]['date']:
            issues.append(f"Temporal paradox at index {i}")

    # Check for duplicate timestamps
    timestamps = timeline['date'].value_counts()
    if timestamps.max() > 5:  # More than 5 events at exact same time
        issues.append("Suspicious timestamp clustering detected")

    # Check for gaps exceeding human lifespan
    max_gap = timeline['date'].diff().max()
    if max_gap > pd.Timedelta(days=365*120):
        issues.append("Impossible temporal gap detected")

    return issues
```

### 4.2 Performance Considerations

#### Temporal Indexing Strategy

```sql
-- Optimize for temporal queries
CREATE INDEX idx_encounters_temporal ON encounters(patient_id, encounter_date DESC);
CREATE INDEX idx_conditions_onset ON conditions(patient_id, onset_date);
CREATE INDEX idx_observations_recent ON observations(patient_id, observation_date)
    WHERE observation_date >= CURRENT_DATE - INTERVAL '2 years';

-- Materialized view for patient timelines
CREATE MATERIALIZED VIEW patient_timelines AS
SELECT
    patient_id,
    array_agg(
        json_build_object(
            'date', event_date,
            'type', event_type,
            'detail', event_detail
        ) ORDER BY event_date
    ) as timeline
FROM all_events
GROUP BY patient_id;
```

### 4.3 Real-Time Temporal Monitoring

```python
class TemporalMonitor:
    """
    Real-time temporal pattern detection
    """
    def __init__(self):
        self.alert_rules = {
            'care_gap': lambda t: (datetime.now() - t.last_pcp_visit).days > 365,
            'overdue_screening': lambda t: t.needs_screening_check(),
            'readmission_risk': lambda t: t.days_since_discharge < 30
        }

    def check_patient(self, patient_timeline):
        alerts = []
        for rule_name, rule_func in self.alert_rules.items():
            if rule_func(patient_timeline):
                alerts.append({
                    'type': rule_name,
                    'patient': patient_timeline.patient_id,
                    'timestamp': datetime.now(),
                    'severity': self.calculate_severity(rule_name)
                })
        return alerts
```

---

## Conclusion

Dr. Smith's temporal analysis methodology provides a comprehensive framework for understanding patient care trajectories across time. The approach emphasizes:

1. **First-principles thinking** in event extraction and sequencing
2. **Multi-dimensional temporal views** (patient, provider, system)
3. **Actionable gap detection** tied to quality measures
4. **Attribution logic** that respects temporal continuity
5. **Real-time monitoring** capabilities for proactive intervention

This methodology transforms raw temporal data into clinically meaningful insights that drive quality improvement and care coordination across the healthcare continuum.

---
*Document Version: 1.0*
*Last Updated: November 21, 2025*
*Author: Data Voyager Team - Symphony Corps*
