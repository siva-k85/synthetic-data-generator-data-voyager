# Task: Andor 1000 Wisconsin Run (seed 5150/5150)

Status: **Mapping executed with placeholders; ready for canonical org IDs**

What we did
- Generated bulk NDJSON + CSV (`runs/20251120_170157_andor1000/output/`, hashes present).
- Practitioner/organization inventory:
  - Practitioner refs: Encounter, DiagnosticReport, DocumentReference, CareTeam, EOB, MedicationRequest, Provenance.
  - Organization refs: Encounter, Claim, DiagnosticReport, DocumentReference, CareTeam, Provenance.
  - Encounter missingness: 0% practitioner, 0% organization.
  - Five drilldowns (pediatric, teen, elderly, multi-morbid adult, deceased adult) with resource/pract/org counts (see `docs/andor_practitioner_org_analysis.md`).
- GraphViz rerun under Java 21 (see `docs/disease_modules_explained.md`).
- Executed full reference replacement using **placeholder** IDs:
  - Mapped output: `runs/20251120_170157_andor1000_mapped/output/fhir/`
  - Placeholder mappings: `dr_smith_package/practitioner_mapping_placeholder.csv`, `dr_smith_package/organization_mapping_placeholder.csv`
  - Practitioner↔Org pairs: `dr_smith_package/practitioner_org_pairs_placeholder.csv` (pairs sum = total encounters 64,614)

What remains
- [x] Swap Placeholders with Canonical Andor IDs
- [x] Drilldown: Specialist-heavy adult (candidate: `ab4a622d-fecf-7852-bc88-6371a067070f`, age 71, 666 encounters)
- [x] Drilldown: Low-util adult (candidate: `06ca6d0f-2c77-654d-4690-88feb73a0330`, age 37, 7 encounters)

Files to show
- Output: `runs/20251120_170157_andor1000/output/fhir/`.
- Mapped output: `runs/20251120_170157_andor1000_mapped/output/fhir/` (placeholder IDs).
- Narrative: `docs/andor_practitioner_org_analysis.md`, `docs/mapping_plan.md`.
