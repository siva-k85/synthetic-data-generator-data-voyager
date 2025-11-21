# Task: ServiceRequest Counting & Coverage Handling

Status: **Counting rules set; Coverage still a gap in default run**

ServiceRequests
- Full mode (recommended): standalone ServiceRequest + EOB-contained ServiceRequest.
- Minimal mode: standalone ServiceRequest only.
- Observed: 14 EOB-contained ServiceRequests for “Abe” surrogate in default run; no standalone SR.ndjson.
- Action: report both `service_requests_full` and `service_requests_minimal`; reconcile delta to EOB-only services.

Coverage
- Default run lacks Coverage NDJSON. WI Data Dictionary (Sec. 3.2) shows Coverage is expected when included.
- Options to fix:
  1) Enable Coverage export in Synthea (include Coverage in included_resources).
  2) Or synthesize Coverage FHIR from `payers__andor__n8__v3_0__prod.csv` + `insurance_plans__andor__v3_0__prod.csv` (map payor -> Organization, plan -> coverage.class).
- Validation when enabled: every patient in measure population has ≥1 active Coverage; payor identifiers match payer/plan tables.

Deliverables to update after fix
- `docs/default_synthea_training.md` (Coverage counts for “Abe”).
- `docs/andor_practitioner_org_analysis.md` (payer/coverage presence in drilldowns).
