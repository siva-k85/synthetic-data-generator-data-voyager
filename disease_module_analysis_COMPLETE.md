# Disease Module Analysis (Dr. Smith's Request)


# Disease Module Analysis: Metabolic Syndrome Disease Progression

## Module Metadata
- **Name:** Metabolic Syndrome Disease Progression
- **Specialty:** Primary Care
- **States:** 32

## State Machine Analysis

### Initial State: Initial

### State: Initial
- **Type:** Initial

### State: Initial_Eye_Health
- **Type:** SetAttribute

### State: Initial_Macular_Edema
- **Type:** SetAttribute

### State: Initial_Nerve_Health
- **Type:** SetAttribute

### State: Age_Guard
- **Type:** Guard

### State: Eventual_Prediabetes
- **Type:** Delay

### State: Eventual_Diabetes
- **Type:** SetAttribute

### State: Onset_Prediabetes
- **Type:** SetAttribute

### State: No_Diabetes
- **Type:** Terminal

### State: Onset_Prediabetes_Towards_Diabetes
- **Type:** SetAttribute

### State: Onset_Diabetes
- **Type:** SetAttribute

### State: Chance_to_Onset_Hypertension_at_Diabetes_Onset
- **Type:** Simple

### State: Onset_Hypertension_with_Diabetes
- **Type:** SetAttribute

### State: No_Hypertension_With_Diabetes
- **Type:** SetAttribute

### State: Diabetes_Progression
- **Type:** Delay

### State: Retinopathy_Progression
- **Type:** CallSubmodule

### State: Neuropathy_Progression
- **Type:** Simple

### State: Set_Mild_Nerve_Damage
- **Type:** SetAttribute

### State: Set_Neuropathy
- **Type:** SetAttribute

### State: Mild_Nerve_Damage_Symptom
- **Type:** Symptom

### State: Set_Moderate_Nerve_Damage
- **Type:** SetAttribute

### State: Moderate_Nerve_Damage_Symptom
- **Type:** Symptom

### State: Set_Severe_Nerve_Damage
- **Type:** SetAttribute

### State: Severe_Nerve_Damage_Symptom
- **Type:** Symptom

### State: Loop_back_to_Start
- **Type:** Simple

### State: Non_Veteran_Diabetes_Prevalence
- **Type:** Simple

### State: Veteran_Diabetes_Prevalence
- **Type:** Simple

### State: Onset_Prediabetes_2
- **Type:** SetAttribute

### State: Countdown to Diabetes
- **Type:** Counter

### State: Already_age_18
- **Type:** Counter

### State: Delay_Another_Year
- **Type:** Delay

### State: Check Onset
- **Type:** Simple

## Impact on Care Coordination

### Care Gaps This Module Triggers:
Standard preventive care.

### Post-Processing Requirements:
1. Track state transitions over time
2. Link conditions to quality measures
3. Generate appropriate care gaps based on state

---


# Disease Module Analysis: Hypertension

## Module Metadata
- **Name:** Hypertension
- **Specialty:** Primary Care
- **States:** 47

## State Machine Analysis

### Initial State: Initial

### State: Initial
- **Type:** Initial

### State: Onset_Hypertension
- **Type:** SetAttribute

### State: Diagnose_Hypertension
- **Type:** ConditionOnset

- **Condition Codes:**
  - System: SNOMED-CT
  - Code: 59621000
  - Display: Essential hypertension (disorder)
- **First Principles:** This creates a Condition resource with ICD-10/SNOMED code

### State: Hypertension_Followup_Encounter
- **Type:** Encounter

### State: End_Hypertension_Followup_Encounter
- **Type:** EncounterEnd

### State: Hypertension_Followup_Encounter_2
- **Type:** Encounter

### State: Hypertension_Followup_Encounter_3
- **Type:** Encounter

### State: End_Hypertension_Followup_Encounter_2
- **Type:** EncounterEnd

### State: End_Hypertension_Followup_Encounter_3
- **Type:** EncounterEnd

### State: LifeStyle_Modifications_Hypertension_CarePlan
- **Type:** CarePlanStart

### State: Wellness_Encounter
- **Type:** Encounter

### State: End_Wellness_Encounter
- **Type:** EncounterEnd

### State: Delay_One_Month
- **Type:** Delay

### State: Record_BP
- **Type:** MultiObservation

### State: Record_BP_2
- **Type:** MultiObservation

### State: Record_BP_3
- **Type:** MultiObservation

### State: Referral To Hypertension Clinic
- **Type:** Procedure

### State: Set_BP_Not Controlled
- **Type:** SetAttribute

### State: Delay 2_Month
- **Type:** Delay

### State: Delay_2_Month_2
- **Type:** Delay

### State: Set_BP_Controlled
- **Type:** SetAttribute

### State: Set_BP_Controlled_2
- **Type:** SetAttribute

### State: Set_BP_Controlled_3
- **Type:** SetAttribute

### State: Prescribe_Medication_3
- **Type:** CallSubmodule

### State: Prescribe_Medication_2
- **Type:** CallSubmodule

### State: Prescribe_Medication
- **Type:** CallSubmodule

### State: Terminal
- **Type:** Terminal

### State: Drop Outs
- **Type:** Simple

### State: Check for Hypertension
- **Type:** Simple

### State: Hypertension_Screening_Reason
- **Type:** SetAttribute

### State: White
- **Type:** Simple

### State: Black
- **Type:** SetAttribute

### State: All Others
- **Type:** SetAttribute

### State: White Male
- **Type:** SetAttribute

### State: White Female
- **Type:** SetAttribute

### State: Assign Hypertension Base Probability
- **Type:** Simple

### State: Eventual Hypertension
- **Type:** Simple

### State: Wait for Hypertension Onset
- **Type:** Delay

### State: Black Onset Age
- **Type:** SetAttribute

### State: White Onset Age
- **Type:** SetAttribute

### State: All Others Onset Age
- **Type:** SetAttribute

### State: Unlikely Onset
- **Type:** SetAttribute

### State: Check for Hypertension Override
- **Type:** Simple

### State: Check for Smoking related Hypertension
- **Type:** Simple

### State: Check for Exclusions
- **Type:** Simple

### State: Decrement_Years
- **Type:** Counter

### State: Check Result
- **Type:** Simple

## Impact on Care Coordination

### Care Gaps This Module Triggers:

1. **BP Control**: Regular blood pressure monitoring (< 140/90).
2. **Medication Adherence**: Statin therapy if indicated.


### Post-Processing Requirements:
1. Track state transitions over time
2. Link conditions to quality measures
3. Generate appropriate care gaps based on state

---


# Disease Module Analysis: Chronic Kidney Disease

## Module Metadata
- **Name:** Chronic Kidney Disease
- **Specialty:** Primary Care
- **States:** 35

## State Machine Analysis

### Initial State: Initial

### State: Initial
- **Type:** Initial

### State: Initial_Kidney_Health
- **Type:** SetAttribute

### State: Guard_for_Htn_or_DM
- **Type:** Guard

### State: Nephropathy_Progression
- **Type:** Delay

### State: Set_Nephropathy
- **Type:** SetAttribute

### State: Set_Microalbuminuria
- **Type:** SetAttribute

### State: Set_Proteinuria
- **Type:** SetAttribute

### State: Expected_Lifespan_for_ESRD
- **Type:** Death

### State: Loop_back_to_Start
- **Type:** Simple

### State: Set_CKD_1 Damage
- **Type:** SetAttribute

### State: Set_CKD_2 Damage
- **Type:** SetAttribute

### State: Set_CKD_3 Damage
- **Type:** SetAttribute

### State: Set_CKD_4 Damage
- **Type:** SetAttribute

### State: Set_CKD_5 Damage
- **Type:** SetAttribute

### State: CKD1_Symptom_1
- **Type:** Symptom

### State: CKD2_Symptom_1
- **Type:** Symptom

### State: CKD2_Symptom_2
- **Type:** Symptom

### State: CKD2_Symptom_3
- **Type:** Symptom

### State: CKD2_Symptom_4
- **Type:** Symptom

### State: CKD1_Symptom_2
- **Type:** Symptom

### State: CKD1_Symptom_3
- **Type:** Symptom

### State: CKD1_Symptom_4
- **Type:** Symptom

### State: CKD3_Symptom_1
- **Type:** Symptom

### State: CKD3_Symptom_2
- **Type:** Symptom

### State: CKD3_Symptom_3
- **Type:** Symptom

### State: CKD3_Symptom_4
- **Type:** Symptom

### State: CKD5_Symptom_1
- **Type:** Symptom

### State: CKD5_Symptom_2
- **Type:** Symptom

### State: CKD5_Symptom_3
- **Type:** Symptom

### State: CKD5_Symptom_4
- **Type:** Symptom

### State: CKD4_Symptom_1
- **Type:** Symptom

### State: CKD4_Symptom_2
- **Type:** Symptom

### State: CKD4_Symptom_3
- **Type:** Symptom

### State: CKD4_Symptom_4
- **Type:** Symptom

### State: Renal Dysplasia
- **Type:** ConditionOnset

- **Condition Codes:**
  - System: SNOMED-CT
  - Code: 204949001
  - Display: Renal dysplasia (disorder)
- **First Principles:** This creates a Condition resource with ICD-10/SNOMED code

## Impact on Care Coordination

### Care Gaps This Module Triggers:

1. **eGFR Monitoring**: Track kidney function decline.
2. **ACE/ARB Therapy**: Renoprotective medication.


### Post-Processing Requirements:
1. Track state transitions over time
2. Link conditions to quality measures
3. Generate appropriate care gaps based on state

---

