# Default Synthea 100‑Patient Baseline (Training Module)

## Problem
New analysts need a reproducible, “plain vanilla” Synthea baseline plus a clear view of what resources appear, how time flows, and where common pitfalls (nested resources, temporal anomalies) occur. Dr. Smith also wants a side‑by‑side against her MS review of patient “Abe”.

## Current State (Run: `runs/20251120_165927_default100`, seed 4242/4242, bulk NDJSON)
- Patients: 111 total (100 alive, 11 deceased) – Synthea’s stochastic overrun above requested 100 is normal.
- Encounters: 6,898 (mean 62.1/patient, median 36, range 6–535; 106/111 patients have >1‑year gaps).
- Temporal checks: 0 encounters before birth; 11 encounters after death (see anomalies below).
- First patient (used as “Abe” surrogate): `bd347326-671c-4cdb-470b-62b3049ed377` (Dorthy94 Bogan287).

### MS vs SK Resource Inventory for first patient
| Resource type | MS expected | SK observed (this run) | Notes |
| --- | --- | --- | --- |
| Patient | 1 | 1 | matches |
| Encounter | 12 | 13 | +1 extra follow‑up |
| Condition | 5 | 7 | extra HTN/DM complications |
| Observation | 23 | 135 | SK counted all vitals/labs; MS likely counted only key labs |
| Procedure | 3 | 7 | includes vaccines counted as procedures |
| MedicationRequest | 4 | 1 | Meds mostly administered/claims; requests sparse |
| Coverage | 2 | 0 (NDJSON not exported in this run) | Coverage not present in bulk NDJSON; present in CSV payer files instead |
| ExplanationOfBenefit | 15 | 14 | near match |
| ServiceRequest | 2 (nested in EOB) | 14 (contained in EOB) | counted inside ExplanationOfBenefit.contained; no standalone ServiceRequest.ndjson |
| CarePlan | 1 | 1 | matches |

### Per‑resource temporal envelope for first patient
| Resource | Count | Earliest | Latest | Comment |
| --- | ---:| --- | --- | --- |
| Encounter | 13 | 2022‑09‑30 | 2025‑09‑05 | spans ~3 years |
| Observation | 135 | 2022‑09‑30 | 2025‑09‑05 | aligned to encounter dates |
| DiagnosticReport | 14 | 2022‑09‑30 | 2025‑09‑05 | mirrors observations |
| CarePlan/CareTeam | 1 each | 2023‑08‑27 | 2023‑09‑10 | short episode |
| Immunization | 26 | 2022‑09‑30 | 2025‑09‑05 | preventive + boosters |
| Condition | 7 | 2022‑09‑30 | 2025‑09‑05 | chronic, no abatement dates |

### Cohort temporal anomalies
- Encounters after death: 11 (e.g., patient `6f8dac68-9750-12bb-b2e8-49dd30f08ccb` death 2025‑04‑15, encounter 2025‑04‑19). Action: filter out post‑death events in downstream QA.
- No encounters before birth detected.

## Solution Approach
1) Pin seeds and isolate outputs (done): `runs/20251120_165927_default100/output/fhir/*.ndjson`, hashes in `output/hashes/sha256.txt`.
2) Parse per‑patient resources with Python to avoid missing nested references (see snippet).
3) When comparing to MS counts, decide your “counting rule”:  
   - **Minimal** (MS style): top-level plus clinically salient nested (EOB→ServiceRequest).  
   - **Full** (SK style): all generated resources (vitals, diagnostic reports, claims, supply deliveries, etc.).
4) Flag temporal paradoxes (post‑death) and document for QA suppression.

### Reproducible Python snippets
Extract first patient and counts (run inside repo root):
```python
from pathlib import Path
import json, datetime
run = Path("runs/20251120_165927_default100/output/fhir")
first = json.loads((run/"Patient.ndjson").open().readline())
pid = first["id"]

# resource counts for that patient
from collections import Counter
counts = Counter()
for ndjson in run.glob("*.ndjson"):
    rtype = ndjson.stem
    for line in ndjson.open():
        obj = json.loads(line)
        ref = obj.get("subject", obj.get("patient", obj.get("beneficiary", {}))).get("reference","")
        if rtype == "Patient":
            ref = "Patient/"+obj["id"]
        if ref.endswith(pid):
            counts[rtype]+=1
print(counts)
```

Check encounters after death:
```python
import datetime, json
run = Path("runs/20251120_165927_default100/output/fhir")
birth = {}; death = {}
for line in (run/"Patient.ndjson").open():
    p=json.loads(line); birth[p["id"]] = datetime.date.fromisoformat(p["birthDate"])
    if "deceasedDateTime" in p:
        death[p["id"]] = datetime.date.fromisoformat(p["deceasedDateTime"][:10])

anomalies=[]
for line in (run/"Encounter.ndjson").open():
    e=json.loads(line)
    pid=e["subject"]["reference"].split("/")[-1]
    ds=datetime.date.fromisoformat(e["period"]["start"][:10])
    if pid in death and ds>death[pid]:
        anomalies.append((pid, death[pid], ds))
print(len(anomalies), anomalies[:5])
```

## Recommended next step
Double‑check EOB‑nested ServiceRequests and Coverage counts if you need exact MS parity: scan `ExplanationOfBenefit.item[*].encounter` and `ExplanationOfBenefit.careTeam[].role` for implied service requests and count them explicitly.
