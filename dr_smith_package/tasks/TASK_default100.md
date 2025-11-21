# Task: Default 100-Patient Baseline (seed 4242/4242)

Status: **Completed**

What we did
- Ran vanilla Synthea with bulk NDJSON + CSV (`runs/20251120_165927_default100/output/`).
- Temporal QA: 0 encounters before birth; 11 after death. Gaps >1y in 106/111 pts.
- “Abe” surrogate: rich resource set (Obs 135, Enc 13, EOB 14, SR contained 14).
- ServiceRequest counting (full mode): 14 contained in EOB; no standalone SR.ndjson.
- Documentation: `docs/default_synthea_training.md` (MS vs SK table, temporal envelopes, Python snippets).

Files to show Dr. Smith
- Output: `runs/20251120_165927_default100/output/fhir/*.ndjson` (+ hashes).
- Narrative: `docs/default_synthea_training.md`.
- This task sheet: `dr_smith_package/tasks/TASK_default100.md`.

Next (if needed)
- Enable Coverage export for parity (current default run lacks Coverage NDJSON).
