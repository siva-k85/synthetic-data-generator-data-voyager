# Practitioner & Organization Analysis — Andor Wisconsin Run (p=1000)
Run: `runs/20251120_170157_andor1000` (seed 5150/5150, network=true, US Core 6.1.0, bulk NDJSON)

## Problem
We must replace all non‑Andor practitioners/organizations in Synthea output and keep references consistent across every resource type. First step: fully inventory where those references live, quantify frequencies, and surface missingness.

## Current State (what the data shows)
- Encounters: 64,614
- Practitioner reference missingness: 0%
- Organization reference missingness: 0%

### Reference path inventory (where practitioner/org refs appear)
- Practitioner refs present in: **Encounter**, DiagnosticReport, DocumentReference, CareTeam, ExplanationOfBenefit, MedicationRequest, Provenance.
- Organization refs present in: **Encounter**, Claim, DiagnosticReport, DocumentReference, CareTeam, Provenance.
- Dominant paths:
  - `Encounter.participant[0].individual.reference`
  - `Encounter.serviceProvider.reference`
  - `DiagnosticReport.performer[0].reference`
  - `DocumentReference.author[0].reference` and `DocumentReference.custodian.reference`
  - `ExplanationOfBenefit.contained[0].requester/performer[0].reference`, `ExplanationOfBenefit.provider.reference`
  - `CareTeam.participant[1..2].member.reference`, `CareTeam.managingOrganization[0].reference`

### Encounter practitioner/organization frequencies
| Metric | Value |
| --- | --- |
| Total encounters | 64,614 |
| Missing practitioner | 0 (0%) |
| Missing organization | 0 (0%) |
| Top practitioner | NPI 9999930792 (2.38% of encounters) |
| Top organization | Org 86c3d8af… (2.38% of encounters) |
| Top pair | 9999930792 → 86c3d8af… (2.38% of encounters) |

### Five‑patient drilldown (first 5 patients in Patient.ndjson)
- IDs:  
  1) Kathryne752 Hoeger474 (`6204baf2-d654-503d-247b-90c78e37aade`)  
  2) Gabriela205 Narváez57 (`97f6d744-73d6-8529-a3f4-f6fb310db997`)  
  3) Bell723 Simonis280 (`36bb7045-8cdb-bd65-bd71-577aecd1ea31`)  
  4) Almeda560 Ruecker817 (`14a70cd7-5a25-48a0-9388-47730945e75b`)  
  5) Babette571 Predovic534 (`430f6cd3-08c0-afd3-3094-653f3f8c35d7`)

| Patient | Encounters | Top practitioners (count) | Top orgs (count) |
| --- | --- | --- | --- |
| Kathryne752 | 38 | NPI 9999994590 (272), 9999946590 (268) | Org a107ecdc… (104), d3feaf97… (94) |
| Gabriela205 | 14 | NPI 9999942490 (77) | Org 1f0498f9… (34) |
| Bell723 | 16 | NPI 9999972695 (77), 9999994590 (68) | Org 173dff30… (34) |
| Almeda560 | 24 | NPI 9999962795 (84), 9999978692 (79) | Org c8f20bc2… (38), 84175f5a… (32) |
| Babette571 | 64 | NPI 9999989392 (424) | Org 62789d64… (177) |

Resource footprint examples:
- Babette571: 204 Procedures, 75 Claims/EOB, 64 Encounters → heavy specialty load.
- Gabriela205: slim profile (14 Encounters, 1 MedicationRequest) → good for spot‑checking attribution replacement logic.

## Solution (replacement & validation plan)
1) Build mapping tables: `practitioner_map.csv` and `organization_map.csv` keyed by identifier (NPI for Practitioner, synthea GUID for Organization) → Andor IDs.
2) Systematic replace (post‑process):
   - For each NDJSON resource, rewrite any `reference` starting with `Practitioner` / `Organization` using the maps; keep displays in sync.
   - Apply equally to nested refs (EOB.contained, CareTeam.participant, DocumentReference.author, Provenance.agent).
3) Validate:
   - Recompute missingness (should stay 0%).
   - Re‑run frequency table to confirm all refs are in the Andor namespace.
   - Ensure pair distribution still sums to 100% of encounters (no orphan pairs).

## Reproducible Python snippets
Inventory paths and counts:
```python
import json
from pathlib import Path
run = Path("runs/20251120_170157_andor1000/output/fhir")
pr_paths, org_paths = {}, {}
def walk(o,path=""):
    if isinstance(o,dict):
        if 'reference' in o and isinstance(o['reference'],str):
            ref=o['reference']
            if ref.startswith("Practitioner"):
                pr_paths.setdefault(path or "reference",0); pr_paths[path or "reference"]+=1
            if ref.startswith("Organization"):
                org_paths.setdefault(path or "reference",0); org_paths[path or "reference"]+=1
        for k,v in o.items(): yield from walk(v, f"{path}.{k}" if path else k)
    elif isinstance(o,list):
        for i,v in enumerate(o): yield from walk(v, f"{path}[{i}]" if path else f"[{i}]")
for f in run.glob("*.ndjson"):
    for line in f.open():
        obj=json.loads(line)
        for _ in walk(obj): pass
print(pr_paths)  # path → count
```

Encounter frequency & missingness:
```python
from collections import Counter
enc = Path(run/"Encounter.ndjson")
prac, org, pairs = Counter(), Counter(), Counter()
total=miss_p=miss_o=0
for line in enc.open():
    e=json.loads(line); total+=1
    p=None
    if e.get("participant"):
        for part in e["participant"]:
            if part.get("individual",{}).get("reference"):
                p=part["individual"]["reference"]; break
    o=e.get("serviceProvider",{}).get("reference")
    if p: prac[p]+=1
    else: miss_p+=1
    if o: org[o]+=1
    else: miss_o+=1
    if p and o: pairs[(p,o)]+=1
```

## Next steps
- Apply replacement maps, then re‑run the counters to verify 100% Andor coverage.
- Extend drilldown to 5 additional patients covering pediatrics, elderly multi‑morbid, and deceased to test edge cases.
