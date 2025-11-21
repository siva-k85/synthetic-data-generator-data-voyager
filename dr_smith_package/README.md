# Dr. Smith Delivery Package (Snapshot: 2025-11-20)

This folder outlines where to find every run, input, output, and documentation artifact. Paths are relative to the project root.

## Contents
- `default100/` — Vanilla 100-patient run (seed 4242/4242)
  - Inputs: default Synthea (no custom CSVs)
  - Outputs: `runs/20251120_165927_default100/output/` (bulk NDJSON + CSV, hashes in `output/hashes/sha256.txt`)
  - Metrics: see `docs/default_synthea_training.md`
- `andor1000/` — Wisconsin/Andor 1000-patient run (seed 5150/5150, network=true)
  - Inputs: Andor geography/payer/provider CSVs (as configured in `synthea.properties`)
  - Outputs: `runs/20251120_170157_andor1000/output/` (bulk NDJSON + CSV, hashes in `output/hashes/sha256.txt`)
  - Metrics & practitioner/org analysis: `docs/andor_practitioner_org_analysis.md`
- `generic_clinic/` — 6-clinic + specialists experiment (seed 6201/6201, p=200)
  - Inputs: `input/refdata/generic_clinics.csv`
  - Outputs: `runs/20251120_1715_generic/output/`
  - Findings: `docs/generic_clinic_experiment.md`
- `graphviz/` — Disease module diagrams (rendered under Java 21)
  - Location: `output/graphviz/*.png` (include metabolic_syndrome_disease, hypertension, CKD)
  - How-to: `docs/disease_modules_explained.md`
- `docs/` — Key narratives
  - `docs/default_synthea_training.md`
  - `docs/andor_practitioner_org_analysis.md`
  - `docs/generic_clinic_experiment.md`
  - `docs/disease_modules_explained.md`
  - `docs/change_log_core_edits.md` (no core Java changes)
  - `docs/mapping_plan.md` (mapping schemas and replacement rules grounded in Andor System Summary and WI data dictionary)

## Open Tasks / Gaps
- Practitioner/organization replacement maps **not yet applied**: build NPI → Andor and Org GUID → Andor tables (see `docs/mapping_plan.md`), apply to NDJSON, then rerun counters in `docs/andor_practitioner_org_analysis.md`.
- Extend drilldown: we now have five (pediatric, teen, elderly, multi-morbid adult, deceased adult). Add specialist-heavy and low-utilization adult after mappings.
- EOB nested ServiceRequests & Coverage: default NDJSON lacked Coverage; enable Coverage export or synthesize from payer/plan CSVs. Count EOB-contained ServiceRequests for “full” mode (14 observed for Abe surrogate).

## How to Reproduce
See `docs/runbook.md` for exact commands, seeds, and environment notes (Java 21, bulk NDJSON).
