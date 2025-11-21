# Runbook: Default 100 & Andor 1000 Synthea Runs

This runbook locks down seeds, folders, and commands so every run is isolated and reproducible.

## Prereqs
- Java 21 (`export JAVA_HOME=/Library/Java/JavaVirtualMachines/temurin-21.jdk/Contents/Home`)
- Graphviz installed (`dot -V`) if you plan to render modules
- Repo root: `synthetic-data-generator-data-voyager`

## Foldering
Each run lives under `runs/<timestamp>_default100/` or `runs/<timestamp>_andor1000/` with:
- `output/` (FHIR/CSV)
- `logs/gradle.log`
- `GENERATION_PROOF.txt` (command + seeds)
- `output/hashes/sha256.txt` (NDJSON hashes)

## Default 100‑patient vanilla run
Seeds default to 4242; override with `SEED=... CLIN_SEED=...`.
```bash
chmod +x scripts/run_default_100.sh
SEED=4242 CLIN_SEED=4242 scripts/run_default_100.sh
```
Outputs at `runs/<stamp>_default100/output`.

## Wisconsin/Andor 1000‑patient run
Uses Andor geography/payer/provider CSVs already referenced in `synthea.properties`; forces `network=true`; seeds default to 5150.
```bash
chmod +x scripts/run_andor_1000.sh
SEED=5150 CLIN_SEED=5150 scripts/run_andor_1000.sh
```
Outputs at `runs/<stamp>_andor1000/output`.

## Referral toggle
Leave referrals off unless you explicitly need referral artifacts; turning them on adds complexity to replacement logic. If needed, add:
```
--generate.referrals=true
```
to the command and note it in `GENERATION_PROOF.txt`.

## After each run
1) Verify `output/fhir/*.ndjson` exists; hashes are in `output/hashes/sha256.txt`.
2) Capture anomalies (missing practitioner/org references, temporal issues) and note them in the run’s `analysis/` folder.
3) For GitBook deliverables, copy findings into:
   - `docs/default_synthea_training.md`
   - `docs/andor_practitioner_org_analysis.md`
   - `docs/disease_modules_explained.md`
   - `docs/generic_clinic_experiment.md`
