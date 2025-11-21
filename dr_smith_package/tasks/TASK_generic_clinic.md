# Task: Generic 6-Clinic + Specialists Experiment (seed 6201/6201, p=200)

Status: **Partially complete**

What we did
- Created `input/refdata/generic_clinics.csv` with 6 primary clinics (930001–930006) and 4 specialists (930101–930104).
- Ran Synthea with network=true, bulk NDJSON (`runs/20251120_1715_generic/output/`).
- Encounter stats: 18,073 encounters; practitioner/org missingness = 0%.
- Top org share is uneven (max ~9.4%); load not yet balanced to 16–20% target.

Gaps
- `Organization.ndjson` not present in this run (likely excluded by config) — cannot map org GUIDs to names; need rerun with Organization export or infer via identifiers.
- Practitioner/org mapping to Andor not applied.
- Clinic load not rebalanced.

Next steps to finish
1) Re-run with Organization export enabled (ensure `exporter.fhir.included_resources` is empty or includes Organization).
2) Build `generic_clinic_dimension.csv` (org_guid, clinic_code, npi, clinic_name, clinic_type, city, zip) from `generic_clinics.csv`.
3) Apply mappings per `docs/mapping_plan.md`; recompute encounter distribution; optionally reassign encounters to balance to ~16–20% per clinic.
4) Update `docs/generic_clinic_experiment.md` with balanced results.
