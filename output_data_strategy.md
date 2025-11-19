# Andor Health System - Output Data Strategy (The Attribution Gap)

**The Problem:** Synthea generates *patients* and *events*. It does not generate a *Health System*.
**The Solution:** This document defines the **Post-Processing Logic** required to transform raw FHIR NDJSON into the "Andor Health System" view used by Care Coordinators.

## 1. Entity Relationships (Cardinality)

We must enforce these relationships to maintain data integrity in the Data Warehouse.

*   **1 Patient : N Encounters**
    *   *Constraint:* A patient cannot have an encounter without a valid Patient ID.
*   **1 Patient : N Coverages**
    *   *Constraint:* Coverage periods must be contiguous (or explicitly show gaps). Overlapping primary coverage is a data error.
*   **1 Coverage : 1 Payer (Organization)**
    *   *Constraint:* Every Coverage resource must link to a valid Organization in `payers.csv`.
*   **1 Encounter : 1 Practitioner**
    *   *Constraint:* Every "Office Visit" encounter must have a primary performer (Practitioner) for attribution.

## 2. The Attribution Algorithms (Post-Processing)

These algorithms run nightly in the Data Warehouse to assign patients to Care Teams.

### A. Patient-to-PCP Attribution (The "Medical Home")
*   **Goal:** Assign every patient to a specific Primary Care Provider (PCP).
*   **Algorithm:**
    1.  **Filter:** Select all `Encounter` resources where `class = 'ambulatory'` OR `class = 'wellness'` in the last 24 months.
    2.  **Group:** Group by `Encounter.participant.individual` (The Practitioner).
    3.  **Rank:** Count visits per Practitioner.
    4.  **Select:** The Practitioner with the highest visit count is the **Attributed PCP**.
        *   *Tie-Breaker:* The Practitioner with the most recent visit.
*   **Workflow Impact:** The Attributed PCP's name appears on the patient's "Face Sheet" in the EMR.

### B. Payer-to-Contract Mapping (The "Risk Model")
*   **Goal:** Determine which Quality Measures apply to the patient.
*   **Algorithm:**
    1.  **Identify:** Find the active `Coverage` (where `period.end` is NULL or > Today).
    2.  **Extract:** Get the `Coverage.payor.identifier` (The Payer ID).
    3.  **Map:** Use the `Contract_Mapping_Table` (Reference Data):
        *   `Sunrise MA Gold` -> **Contract C002** (Risk Sharing / HEDIS)
        *   `Medicare FFS` -> **Contract C001** (MSSP / ACO Measures)
*   **Workflow Impact:** Determines if the Care Coordinator sees a "HEDIS Gap" (Commercial) or a "Stars Gap" (Medicare).

## 3. Worklist Generation (Condition + Observation = Gap)

How we generate the "Daily Task List" for Maria (Care Coordinator).

### Scenario: "Uncontrolled Diabetes"
1.  **Trigger (Condition):** Patient has an active `Condition` with code `44054006` (Type 2 Diabetes).
2.  **Check (Observation):** Query `Observation` resources for LOINC `4548-4` (HbA1c) in the last 12 months.
3.  **Logic:**
    *   IF `Observation` is MISSING -> **Task:** "Order HbA1c Lab".
    *   IF `Observation.value` > 9.0% -> **Task:** "Schedule Diabetes Education".
    *   IF `Observation.value` <= 9.0% -> **No Task** (Gap Closed).
