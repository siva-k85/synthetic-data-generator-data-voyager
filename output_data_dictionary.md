# Andor Health System - Output Data Dictionary & Attribution Strategy

This document defines the FHIR Bulk Data (NDJSON) outputs and the **post-processing strategy** required to bridge the gap between raw Synthea output and the Care Coordinator's worklist.

## 1. The Cardinality Map (Entity Relationships)

Understanding these relationships is required to join the data files into a cohesive view for attribution.

| Relationship | Cardinality | Why this matters for the Care Coordinator |
| :--- | :--- | :--- |
| **Patient : Encounter** | 1 : N | Used to calculate **Attribution**. The provider seen most often in `Encounter` becomes the attributed PCP. |
| **Patient : Coverage** | 1 : N | Historical view. Filter by `period.end` is NULL to find the **Current Payer** (who pays for the gap closure). |
| **Coverage : Organization** | 1 : 1 | Links patient to the Payer (e.g., "Sunrise MA"). Necessary to map to **Contract C002** (Risk Sharing). |
| **Encounter : Practitioner** | N : 1 | Links care delivery to a specific doctor. Used to generate **Provider Performance Reports**. |
| **Patient : Condition** | 1 : N | The source of truth for **Risk Adjustment (HCC)**. Defines the "High Risk" worklist. |

## 2. The "Gap" Strategy: Post-Processing Attribution Logic

*Synthea generates raw events (visits, claims). You must aggregate these to build "Panels" and "Worklists".*

### Step 1: Establish Patient-to-PCP Attribution
*   **Input:** `Encounter.ndjson`, `Practitioner.ndjson`
*   **Logic:** Filter Encounters for "Wellness" or "Office Visit" types in the last 24 months. Group by `Encounter.participant.individual`.
*   **Rule:** Assign PCP = Provider with the highest count of visits. (Tie-breaker: Most recent visit).
*   **Outcome:** Care Coordinator knows **who** to message about the patient.

### Step 2: Establish Payer-to-Contract Attribution
*   **Input:** `Coverage.ndjson`, `Organization.ndjson` (Payers)
*   **Logic:** Extract `Coverage.payor.identifier` and `Coverage.class`.
*   **Rule:** Map `Sunrise MA Gold` (Plan ID 12001) $\rightarrow$ **Contract C002** (Risk Sharing).
*   **Outcome:** System knows **which** Quality Measures (HEDIS vs. Stars) apply to this patient.

### Step 3: Generate the Worklist
*   **Input:** `Condition.ndjson` (Diabetes), `Observation.ndjson` (HbA1c results).
*   **Logic:** IF `Condition` = Diabetes AND `Observation` (HbA1c) is missing in last 12 months...
*   **Rule:** Flag as **CARE GAP**.
*   **Outcome:** Patient appears on the "Diabetic Gaps" worklist for the attributed Care Coordinator.

## 3. FHIR Resource Dictionary (NDJSON Files)

| File Name | Content | Criticality | Processing Logic & VBC Context |
| :--- | :--- | :--- | :--- |
| **Patient.ndjson** | Demographics, Extensions. | **High** | **The Anchor**: All analytics join back to `Patient.id`. Used for per-capita cost calculations. |
| **Coverage.ndjson** | Payer details, periods. | **Critical** | **Attribution**: Determines the financial responsible party. |
| **Encounter.ndjson** | Visits, Locations. | **High** | **Utilization**: High ED/Inpatient utilization flags "High Cost" patients. |
| **Condition.ndjson** | Diagnosis Codes (ICD-10). | **Critical** | **Risk Adjustment**: Maps to HCCs for revenue opportunity calculation. |
| **Observation.ndjson** | Vitals, Labs, SDOH. | **Medium** | **Quality Gaps**: Missing values here trigger "Gap Closure" tasks. |
| **Practitioner.ndjson** | Provider names, NPIs. | **Low** | **Reference**: Essential for assigning patients to specific doctors. |
