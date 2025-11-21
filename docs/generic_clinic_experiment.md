# Generic Clinic + Specialists Experiment

Status: Executed (p=200, seed 6201/6201) with 6 clinics + 4 specialists CSV.

## Goal
Force encounters into 6 generic clinics (East, West, North, South, Central, Suburban) with a defined specialist roster, then measure how practitioner/org assignments shift, including missingness.

## Plan
1) Create `input/refdata/generic_clinics.csv` with six clinics (name, address, lat/long, phone).
2) Create `input/refdata/specialists.csv` with NPIs and specialties (Cardiology, Endocrinology, Nephrology, etc.), each tied to one of the six clinics.
3) Update run command (p=100 or 200 for speed):
   ```bash
   SEED=6201 CLIN_SEED=6201 ./run_synthea \
     -p 200 Wisconsin \
     --generate.providers.primarycare.default_file=input/refdata/generic_clinics.csv \
     --generate.providers.selection_behavior=network \
     --exporter.baseDirectory=runs/20251120_1715_generic/output \
     --exporter.fhir.export=true --exporter.fhir.bulk_data=true \
     --exporter.csv.export=true --exporter.fhir.use_us_core_ig=true \
     --exporter.fhir.us_core_version=6.1.0
   ```
   Ensure the provider CSV pointers in `synthea.properties` reference the new clinic/specialist files.
4) Post-process:
   - Encounter practitioner/org missingness.
   - Encounter counts by clinic; practitioner counts by specialty.
   - Practitioner→organization pair distribution.
5) Document findings here with before/after tables.

## Deliverables (to fill after run)
- Run output: `runs/20251120_1715_generic/output` (257 patients total; 200 alive, 57 deceased).
- Encounters: 18,073.
- Missingness: practitioner 0%, organization 0%.
- Encounter share by top org IDs (identifier form):  
  - f763e1df… 9.4%  
  - e164b35e… 6.7%  
  - 1a243e2c… 5.9%  
  - 9a67b4bb… 3.5%  
  - a51e4c0d… 3.5%  
  - 86c3d8af… 3.1%  
  (others each <3%)
- Top practitioners mirror org shares (each tied 1:1 to above orgs), confirming consistent practitioner→organization pairing but still uneven load across the 6 clinics (one ~9%, several ~3%).
- Specialist rows added to the CSV, but org IDs in encounters reflect generated identifiers (Organization bulk NDJSON not exported in this run; mapping by identifier string only).

## Notes
- Keep seeds pinned for reproducibility.
- If Synthea still generates extra practitioners, apply the replacement mapping after the run to force all references back to the six clinics.
- To balance clinic loads closer to uniform, consider: increasing `generate.providers.maximum_search_distance`; reducing stochastic overflow (requested 200 → produced 257); and pruning non-listed providers via post-process replacement.
