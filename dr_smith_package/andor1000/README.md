# Andor 1000 Run (seed 5150) — Presentation-Ready Brief for Dr. Smith

## 🧭 Core Message
“The practitioner/org mapping pipeline is ready to execute. I need the canonical Andor organization hierarchy to finish the replacement and release mapped analytics. I can prove the logic today with placeholder org IDs if you approve.”

---

## ✅ What’s Done (First Principles Framing)
**Why:** Encounters must be attributable to real Andor providers/clinics for quality credit, billing, and care coordination roll‑ups.

- Extracted provider roster from Synthea output (practitioner IDs, NPIs, names) — this is the synthetic analog of Epic’s provider master.
- Built mapping templates:
  - `dr_smith_package/practitioner_mapping_stub.csv` (NPIs prefilled, ready for Andor IDs/orgs).
  - `dr_smith_package/organization_mapping_stub.csv` (headers ready; needs org GUIDs).
- Documented replacement & validation logic in `docs/mapping_plan.md`:
  - Field-by-field Practitioner/Org replacement across Encounter, DiagnosticReport, DocumentReference, CareTeam, MedicationRequest, ServiceRequest, Claim, EOB, Provenance.
  - Validation: 100% Encounters mapped to PCP + serviceProvider; zero unmapped refs; practitioner↔org pair counts.
- Analysis complete on unmapped data:
  - 0% missing practitioners/orgs in Encounter references.
  - Five drilldowns (pediatric, teen, elderly, multimorbid adult, deceased adult) in `docs/andor_practitioner_org_analysis.md`.
- GraphViz fixed (Java 21) and ready to share: metabolic syndrome, hypertension, CKD PNGs copied to `dr_smith_package/graphviz/`.

---

## ⏳ What’s Ready to Execute (Awaiting One Input)
**Blocker:** Canonical Andor org hierarchy (system → 3 hospitals → clinics/departments).

**Why it matters:** Replacement needs real org IDs/names to roll encounters to “Andor West Clinic” (not random GUIDs) for contract attribution and performance dashboards.

**Workarounds you can choose:**
1) **Fast path (preferred):** You provide org GUIDs/names/parents from Andor_Health_System_v5e.md → I run full mapping/validation in 1 day.
2) **Test path:** I use placeholder org IDs (ANDOR_ORG_001…) and execute the full pipeline now; swap to real IDs later (1 hour to rerun).
3) **Partial path:** Map practitioners by NPI only, leave orgs unmapped; still validates practitioner attribution.

**My recommendation:** Option 2 now to show end-to-end results; swap IDs when you hand them over.

---

## 🧪 Validation Plan (already coded)
- Hash maps: `NPI → Andor Practitioner ID`, `source_org_id → Andor Org GUID`.
- Streaming NDJSON transformer: rewrites references in all target resources.
- Post-checks: 100% Encounters with mapped participant + serviceProvider; zero unmapped Practitioner/Org refs; practitioner↔org pair totals = Encounter count; missing_mappings.csv if any gaps.
- Drilldowns: regenerate with mapped IDs + add two more (specialist-heavy, low-utilization).

---

## 📄 Deliverables in this folder
- This brief: `dr_smith_package/andor1000/README.md`
- Mapping stubs: `dr_smith_package/practitioner_mapping_stub.csv`, `dr_smith_package/organization_mapping_stub.csv`
- Specs: `docs/mapping_plan.md`, `docs/andor_practitioner_org_analysis.md`
- GraphViz assets: `dr_smith_package/graphviz/*.png`

---

## ❓ Decisions Needed from You
1) Provide or approve the Andor org hierarchy (GUIDs, names, parent-child).
2) Approve running with placeholder org IDs now (yes/no).
3) Coverage handling: do you want synthetic Coverage built from payer CSVs immediately, or wait for Coverage export to be enabled?

---

## 📅 Timeline After Org IDs Arrive
Day 1: Apply mappings + validate + rerun frequency/pairs  
Day 2: Add two drilldowns; rerun generic clinic (if needed); assemble package  
Total: ~3 days to final delivery (including review buffer)

---

## 🔎 If Asked in the Meeting
- “Why not keep Synthea orgs?” → Because performance reports must say “Andor West Clinic closed 85% of eye exam gaps,” not “Org abc-123.”
- “How do you ensure correctness?” → Validation enforces 0 unmapped refs; encounter counts must reconcile; pair table must sum to total encounters.
- “What about referrals?” → ServiceRequest counting uses full mode (standalone + EOB-contained); validated on Abe surrogate with 14 contained SRs—this mirrors Epic order-in-visit behavior.
