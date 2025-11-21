# Final To-Do (Gap List) – As of 2025-11-20

## Replacement & Validation
- [ ] Build practitioner/organization mapping tables (NPI → Andor practitioner, Org GUID → Andor org) for the Andor 1000 run and the generic 6-clinic run. **See `docs/mapping_plan.md` and `dr_smith_package/tasks/TASK_mapping_replacement.md`; awaiting canonical Andor org IDs and populated CSVs.**
- [ ] Apply mappings to all NDJSON resources (Encounter, DiagnosticReport, DocumentReference, CareTeam, EOB, MedicationRequest, Provenance, Claim) and re-run frequency/missingness counters to confirm 100% Andor coverage.
- [ ] Recompute practitioner↔organization pairs post-replacement; verify totals = 100% encounters.

## Drilldowns
- [ ] Add two more drilldown patients covering: (a) specialist-heavy adult; (b) low-utilization adult. Existing five cover pediatric, pediatric-teen, elderly, multimorbid adult, deceased adult. **Selection filters defined in `docs/mapping_plan.md`; execute after mappings.**
- [ ] After mappings, regenerate drilldown tables with updated references.

## Default Run Parity Checks
- [ ] Count EOB-contained ServiceRequests explicitly; if Coverage needed, enable Coverage NDJSON export or ingest coverage from CSV and reconcile with patient slice. **Rule recorded in `dr_smith_package/tasks/TASK_service_request_coverage.md`; EOB-contained SR=14 for Abe surrogate.**
- [ ] Document counting rule (minimal vs full) and reconcile MS vs SK resource counts accordingly.

## Generic Clinic Balancing
- [ ] Map org/practitioner IDs in the generic run to clinic names for clearer tables. **Needs rerun with Organization export; see `dr_smith_package/tasks/TASK_generic_clinic.md`.**
- [ ] If desired, tune selection parameters or post-process replacement to balance encounter load across the 6 clinics (~16–20% each).

## Packaging
- [ ] Copy selected GraphViz PNGs (diabetes, hypertension, CKD) into `dr_smith_package/graphviz/` for easy sharing. **Ready to copy from `output/graphviz/`; see `dr_smith_package/tasks/TASK_graphviz.md`.**
- [ ] Include HTML test/coverage reports if needed (`build/reports/tests/test/index.html`, `build/reports/problems/problems-report.html`) in the package or link them.

## Dependencies / Environment
- Java 21 must be active for GraphViz; document in package.
