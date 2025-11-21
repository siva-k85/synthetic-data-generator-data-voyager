# Andor 1000 Run – Handoff for Dr. Smith (seed 5150)

## Core Message
The mapping/validation pipeline is **implemented and tested end‑to‑end** on the 1000‑patient Andor run using placeholder Andor org IDs (ANDOR_ORG_xxx) and canonical practitioner IDs (AHSP‑xxxx). All encounter/practitioner references now resolve to the mapping tables with **0 missing mappings**. To ship the final production mapping we only need the **canonical Andor organization GUIDs**; swapping them in is a one‑hour rerun.

## What Is Inside This Folder
- `practitioner_mapping.csv` – canonical AHSP practitioner IDs with specialties and target orgs (placeholder orgs currently).
- `organization_mapping.csv` – Andor organization hierarchy template (Org/1 system, Org/2–4 hospitals, clinics/locations placeholders until GUIDs are supplied).
- `replace_references.py` – streaming NDJSON transformer used for the run.
- `mapping_plan.md` – field‑by‑field replacement & validation spec.
- `TASK_andor1000_analysis.md` – task tracker/status.
- `drilldowns/` – two mapped drilldowns (specialist‑heavy adult, low‑utilization pediatric). When canonical orgs are applied, regenerate to reflect final IDs.

## What We Executed (Current State)
- Ran `replace_references.py` on `runs/20251120_170157_andor1000/output/fhir` → produced fully mapped placeholders in `runs/20251120_170157_andor1000_mapped/output/fhir`.
- Validation: 0 unmapped practitioner/org references across Encounter, DiagnosticReport, DocumentReference, CareTeam, MedicationRequest, ServiceRequest, Claim, EOB, Provenance. Practitioner IDs are all AHSP‑xxxx; organizations are ANDOR_ORG_xxx placeholders derived from source displays.
- Generated drilldowns on mapped data:
  - `drilldown_ab4a622d-fecf-7852-bc88-6371a067070f.md` – specialist‑heavy adult.
  - `drilldown_06ca6d0f-2c77-654d-4690-88feb73a0330.md` – low‑util pediatric (no true low‑util adult exists in this run; see “Gap” below).

## Gaps / Decision Points
1) **Canonical org GUIDs**: needed to replace ANDOR_ORG_xxx placeholders. Once provided, rerun `replace_references.py` (runtime ~10 min) to write `..._canonical/output/fhir` and regenerate drilldowns.
2) **Low‑util adult drilldown**: the dataset has no adults with ≤6 encounters. If you want an adult exemplar, we can regenerate with a higher threshold or run a smaller cohort tuned for low utilization.
3) **Coverage**: ServiceRequest counting is already set to “full” (standalone + EOB‑contained). If you want explicit Coverage resources, I can synthesize them from payer/plan CSVs or enable export in the next run.

## How to Reproduce Final Mapping Once Org GUIDs Arrive
1. Populate `organization_mapping.csv` `source_org_id → org_guid` using the provided GUIDs (keep parent hierarchy columns).
2. (Optional) If practitioner org affiliations change, update `practitioner_mapping.csv` `andor_org_guid` column accordingly.
3. Run: `python3 replace_references.py --input runs/20251120_170157_andor1000/output/fhir --mapping dr_smith_package/andor1000 --output runs/20251120_170157_andor1000_canonical/output/fhir`
4. Regenerate drilldowns with `python3 dr_smith_package/generate_drilldowns.py --input runs/20251120_170157_andor1000_canonical/output/fhir --out runs/20251120_170157_andor1000_canonical/output/drilldowns`
5. Validate: ensure practitioner/org missing counts = 0; practitioner↔org pairs sum to total encounters.

## Files To Hand Dr. Smith
- This README.
- `practitioner_mapping.csv`, `organization_mapping.csv` (current mappings + template).
- Drilldowns in `drilldowns/`.
- Spec (`mapping_plan.md`) and task log (`TASK_andor1000_analysis.md`).
- GraphViz PNGs already stored in `dr_smith_package/graphviz/` (diabetes, HTN, CKD) – ready to add to the zip.

## Contact Prep / Talking Points
- “All references now resolve to AHSP practitioner IDs; 0 missing. Org placeholders will be swapped as soon as you provide the GUID list.”
- “Full ServiceRequest counting includes EOB‑embedded referrals (mirrors Epic order‑in‑visit behavior).”
- “Low‑util adult exemplar not present; we can generate one with a tuned run if you want it for training materials.”
