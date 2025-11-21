# Task: Andor 1000 Wisconsin Run (seed 5150/5150)

Status: **Partially complete – mapping not yet applied**

What we did
- Generated bulk NDJSON + CSV (`runs/20251120_170157_andor1000/output/`, hashes present).
- Practitioner/organization inventory:
  - Practitioner refs: Encounter, DiagnosticReport, DocumentReference, CareTeam, EOB, MedicationRequest, Provenance.
  - Organization refs: Encounter, Claim, DiagnosticReport, DocumentReference, CareTeam, Provenance.
  - Encounter missingness: 0% practitioner, 0% organization.
  - Five drilldowns (pediatric, teen, elderly, multi-morbid adult, deceased adult) with resource/pract/org counts (see `docs/andor_practitioner_org_analysis.md`).
- GraphViz rerun under Java 21 (see `docs/disease_modules_explained.md`).

What remains
- Apply practitioner/org replacement maps (NPI→Andor, Org GUID→Andor) per `docs/mapping_plan.md`.
- Re-run frequency/missingness and regenerate practitioner_org_pairs after mapping.
- Add two more drilldowns (specialist-heavy, low-utilization) post-mapping.

Files to show
- Output: `runs/20251120_170157_andor1000/output/fhir/`.
- Narrative: `docs/andor_practitioner_org_analysis.md`, `docs/mapping_plan.md`.
