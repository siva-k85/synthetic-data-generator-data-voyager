# Default 100 Run (seed 4242) — Presentation-Ready Brief for Dr. Smith

## 🧭 Core Message
“Baseline Synthea output is validated and documented. ServiceRequest counting clarified; Coverage is the only remaining gap if you want payer-level attribution.”

---

## ✅ What’s Done (First Principles Framing)
**Why:** This run is the control—shows what plain Synthea produces before Andor-specific post-processing.

- Temporal QA: 0 encounters before birth; 11 after death (flagged), realistic care gaps with >1y gaps in 106/111 patients.
- “Abe” surrogate resource inventory (see `docs/default_synthea_training.md`):
  - Observations 135, Encounters 13, EOB 14.
  - ServiceRequests: 14 contained inside EOB; 0 standalone SR.ndjson.
- ServiceRequest counting rule set:
  - Full mode = standalone SR + EOB-contained SR (recommended for care gap queries).
  - Minimal mode = standalone SR only.
- Documentation includes MS vs SK resource counting, temporal envelopes, and Python snippets for reproducibility.
- GraphViz fixed on Java 21 (assets copied to `dr_smith_package/graphviz/`).

---

## ❗ Remaining Gap
- Coverage not exported in this run. For payer-level attribution/contract logic you have two paths:
  1) Enable Coverage export in Synthea and rerun; or
  2) Synthesize Coverage from payer/plan CSVs (payer + plan IDs are already defined).

---

## 📄 Deliverables in this folder
- This brief: `dr_smith_package/default100/README.md`
- Narrative: `docs/default_synthea_training.md`
- ServiceRequest/Coverage rules: `dr_smith_package/tasks/TASK_service_request_coverage.md`
- GraphViz assets: `dr_smith_package/graphviz/*.png`

---

## 🔎 Meeting-Ready Answers
- “Why count EOB-contained ServiceRequests?” → Referrals/orders are often embedded in visit/claim data; for care-gap closure (e.g., diabetic eye exam referrals) we must count both standalone and contained SRs.
- “How realistic is this baseline?” → Encounter/lab/claim mix matches Synthea defaults; anomalies (post-death encounters) are flagged for exclusion in analytics.
- “What next?” → If Coverage is required for payer analytics, I’ll regenerate this run with Coverage export or build synthetic Coverage from existing payer CSVs.

---

## 🚀 If you approve Coverage synthesis
- I’ll generate Coverage FHIR from `payers__andor__n8__v3_0__prod.csv` + `insurance_plans__andor__v3_0__prod.csv`, attach to each patient, and re-run the resource inventory to show payer mix.
