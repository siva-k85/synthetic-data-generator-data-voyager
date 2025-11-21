# Task: Practitioner/Organization Replacement & Validation

Status: **Not yet applied to NDJSON**

What’s ready
- Schemas and algorithms defined in `docs/mapping_plan.md` (built from ANDOR_SYSTEM_SUMMARY, Andor_Health_System_v5e, WI Data Dictionary).
- Identified all Practitioner/Organization reference fields across Encounter, DiagnosticReport, DocumentReference, CareTeam, MedicationRequest, ServiceRequest, Claim, EOB, Provenance.
- Validation rules and streaming transform approach documented.

What’s missing to finish
- Populate `practitioner_mapping.csv` using NPI from NDJSON → `providers__wi__template__real__v3_0.csv` (Id, NPI, NAME, SPECIALTY, NUCC).
- Populate `organization_mapping.csv` with canonical Andor org IDs/names from `Andor_Health_System_v5e.md` (system + 3 hospitals + clinics/departments). If not explicitly listed, extract from media/sections.
- Run transformer to replace references in all NDJSON files; write transformed NDJSON.
- Re-run frequency/missingness and generate `practitioner_org_pairs.csv`; ensure 0 unmapped refs.

Execution outline
1) Build hash maps: `npi -> practitioner mapping row`; `source_org_id -> org_guid`.
2) Stream each NDJSON, rewrite practitioner/org references field-by-field per mapping plan.
3) Validate: 100% encounters mapped; zero unmapped refs; emit `missing_mappings.csv` if any.
4) Regenerate counters and drilldowns (add specialist-heavy and low-utilization).

Owner action needed
- Provide canonical Andor org GUIDs from `Andor_Health_System_v5e.md` and approve mapping CSVs, then run the transformer.
