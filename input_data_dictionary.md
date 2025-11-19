# Andor Health System - Input Data Dictionary (Workflow Centric)

This document maps the raw input data elements to the **Care Coordinator Actions** they enable. It answers the question: *"How does this field help Maria (the Care Coordinator) close a care gap?"*

## 1. Demographics & Geography

**Files:**

- `geography/demographics__wi_8counties__synthea_ready__y2022__complete__v3_0__prod.csv`
- `geography/zipcodes__wi__zcta__y2020__real__n140__v3_0__prod.csv`

| Field Name | Data Type | Operational "Why" (First Principle) |
| :--- | :--- | :--- |
| `ZIP` | String | **Transportation Assistance**: Used to calculate the distance between `Patient.address` and `Encounter.location`. If > 20 miles, the Care Coordinator receives a task to offer an Uber Health voucher. |
| `POPESTIMATE2020` | Integer | **Panel Sizing**: Ensures the generated patient density matches reality. This prevents us from assigning 5,000 patients to a single rural PCP in the simulation. |
| `RACE_` columns | Float | **Health Equity Dashboard**: Critical for the "Disparity Analysis" report. Allows us to flag if Hispanic patients have lower Diabetes Control rates than the network average. |
| `INCOME` | Integer | **SDOH Referral**: Used as a proxy for financial risk. Patients with `INCOME < $25k` are automatically flagged for a Social Worker assessment for food/housing insecurity. |

## 2. Providers (The Medical Home)

**Files:**

- `providers/hospitals__andor__n3__v3_0__prod.csv`
- `providers/primary_care_facilities__andor__v3_0__prod.csv`

| Field Name | Data Type | Operational "Why" (First Principle) |
| :--- | :--- | :--- |
| `id` | String | **Attribution & Routing**: The "Medical Home" anchor. When a patient is discharged from the ED, this ID determines *which* clinic's inbox receives the "Transition of Care" alert. |
| `specialty` | String | **Referral Management**: Distinguishes PCPs from Specialists. Care Coordinators use this to ensure a Diabetic patient is seeing *both* their PCP (for management) and an Endocrinologist (for complex cases). |
| `name` | String | **Patient Communication**: Displayed in the Patient Portal. "You have an appointment at *Andor General*" is actionable; "Appointment at Loc-123" is not. |
| `address` | String | **Network Adequacy**: Used to verify that the patient has access to a PCP within the 30-minute drive-time standard required by our payer contracts. |

## 3. Payers & Contracts (Financial Risk)

**Files:**

- `payers/payers__andor__n8__v3_0__prod.csv`
- `payers/insurance_plans__andor__v3_0__prod.csv`

| Field Name | Data Type | Operational "Why" (First Principle) |
| :--- | :--- | :--- |
| `id` | String | **Contract Mapping**: The bridge between a patient and a Value-Based Contract. Maps `Plan-12001` -> `Contract-C002`, which activates the "Shared Savings" logic for that patient. |
| `deductible` | Decimal | **Financial Counseling**: High-deductible plans trigger a "Financial Risk" flag. Care Coordinators use this to discuss payment plans *before* scheduling elective procedures. |
| `name` | String | **Benefit Verification**: Allows the Care Coordinator to check if specific services (e.g., "Home Health", "DME") are covered under the patient's specific plan (e.g., "Sunrise MA Gold"). |
