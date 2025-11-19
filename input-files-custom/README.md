# Payers File: MIXED REAL/SYNTHETIC

**File:** `payers__wi__mixed__real-synthetic__n9__v3_0__demo.csv`
**Total Entries:** 9 (1 real + 7 synthetic + 1 self-pay concept)

### ✅ NEW: Andor v3.1 Roster (Production Run Inputs)

- **Payers CSV:** `payers__andor__n8__v3_0__prod.csv`
- **Plans CSV:** `insurance_plans__andor__v3_0__prod.csv`
- **Purpose:** Alive-only Andor cohort (v3.1, seed 3333, N=1000) documented in `old-files/02_CONFIGURATION/andor_v3_1_runbook.csv`.
- **Mix:** Medicare 40% (18% FFS + 22% MA), Medicaid HMO 20%, Commercial 35%, Self-pay 5%.
- **Status:** ✅ Ready for Synthea (used by `synthea_alive.properties`). Keep this alongside the legacy mixed file for audit/history.

---

## ⚠️ IMPORTANT: Data Quality Notice

**This file contains MIXED real and synthetic data:**
- **1 REAL:** CMS Medicare FFS (federal program)
- **7 SYNTHETIC:** Local Wisconsin payers (fabricated for testing)
- **1 CONCEPT:** Uninsured (represents self-pay, not a payer)

**Breakdown:** 1 real + 7 synthetic + 1 concept = 9 total entries

**NOT SUITABLE FOR PRODUCTION USE without replacing synthetic payer data with real Wisconsin health plans.**

---

## What Is REAL

### CMS Medicare FFS (CSV Row 2)
- ✅ Real federal program
- ✅ Real headquarters address: 7500 Security Blvd, Baltimore, MD
- ✅ Real phone: 1-800-633-4227
- ✅ NAIC Code: N/A-Federal (federal programs don't have NAIC codes)
- ✅ Market share: 25% (realistic for Wisconsin Medicare FFS)
- ✅ States Covered: WI (corrected from "WI|MD" in previous version)

---

## What Is SYNTHETIC

### All 7 Local Wisconsin Payers (CSV Rows 3-9)
**These payers DO NOT EXIST. They are fabricated for testing:**

1. **Sunrise Medicare Advantage** - SYNTHETIC
2. **Evergreen Medicare Advantage** - SYNTHETIC
3. **HealthOne Medicaid HMO** - SYNTHETIC
4. **FamilyCare Medicaid HMO** - SYNTHETIC
5. **HorizonHealth** - SYNTHETIC
6. **ClearBlue** - SYNTHETIC
7. **AxisBenefits** - SYNTHETIC

**Synthetic Elements:**
- ❌ Payer names: Fabricated
- ❌ Addresses: All Madison addresses are fake
- ❌ Phone numbers: Labeled "SYNTHETIC-XXXX"
- ❌ NAIC codes: Synthetic numbers (not real NAIC registrations)

**What May Be Realistic:**
- ✅ Market share proportions (40% Medicare, 20% Medicaid, 35% Commercial, 5% Uninsured)
- ✅ Cost-sharing structures (deductibles, coinsurance, copays)
- ✅ Plan types (Medicare Advantage, Medicaid HMO, Commercial)

---

## Uninsured Entry (CSV Row 10)

**Represents:** Self-pay patients with no insurance
- **Not a real payer** - conceptual entry for tracking uninsured population
- **Market share:** 5% (realistic for Wisconsin)
- **Cost-sharing:** 100% patient responsibility

---

## Corrections Made

### From Original File:
1. ✅ Fixed header typo: "State Headquarterd" → "State Headquartered"
2. ✅ CMS States Covered: Changed from "WI|MD" to "WI" (Wisconsin-focused dataset)
3. ✅ Added NAIC codes with explanations:
   - CMS: "N/A-Federal" (federal programs don't have NAIC codes)
   - Uninsured: "N/A-Self-Pay" (not an insurance company)
4. ✅ Phone numbers: Changed from fake "608-555-XXXX" to "SYNTHETIC-XXXX" with clear labeling
5. ✅ Uninsured Plan_Type: Changed from "None" to "No Insurance"
6. ✅ Added Notes column explaining real vs synthetic

---

## Market Share Breakdown

| Payer Category | Market Share | Components |
|----------------|--------------|------------|
| **Medicare** | 40% | CMS FFS (25%) + 2 MA plans (15%) |
| **Medicaid** | 20% | 2 HMO plans |
| **Commercial** | 35% | 3 private insurers |
| **Uninsured** | 5% | Self-pay |
| **TOTAL** | 100% | Validated ✅ |

---

## Use Cases

### ✅ APPROPRIATE:
- Development and testing environments
- Synthea data generation for demos
- Workflow testing
- UI/UX development

### ❌ INAPPROPRIATE:
- Production deployment
- Real claims submission
- Regulatory reporting
- Patient billing

---

## To Make Production-Ready

Replace synthetic payers with real Wisconsin health plans:

1. Research actual Wisconsin payers from:
   - Wisconsin Office of the Commissioner of Insurance
   - CMS Medicare Advantage plan finder
   - Wisconsin Department of Health Services (Medicaid)

2. Obtain real data:
   - Official payer names
   - Real NAIC codes
   - Actual headquarters addresses
   - Real customer service phone numbers
   - Verified market share data

3. Update cost-sharing with:
   - Current year plan benefits
   - Real deductibles and copays
   - Actual premium amounts

---

**Last Updated:** 2025-11-07
**Status:** ⚠️ MIXED REAL/SYNTHETIC - For testing only
