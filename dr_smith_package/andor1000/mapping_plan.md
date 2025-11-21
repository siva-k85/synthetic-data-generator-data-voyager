# Practitioner & Organization Mapping Plan (Implementation-Ready)

Source context used:
- `input-files-custom/ANDOR_SYSTEM_SUMMARY.md` (org structure, payer mix, attribution priorities)
- `input-files-custom/Andor_Health_System_v5e.md` (profiles, measures, attribution hierarchy)
- `input-files-custom/WISCONSIN_BASELINE_V3.0_PRODUCTION_DATA_DICTIONARY.md` (CSV columns, export settings)

## Practitioner mapping (practitioner_mapping.csv)

Schema
| column | type | description |
| --- | --- | --- |
| source_practitioner_id | string | Practitioner.id from NDJSON |
| source_system | string | `synthea_andor_1000` or `synthea_generic_6_clinic` |
| npi | string | 10-digit NPI from NDJSON Practitioner.identifier |
| andor_practitioner_id | string | `Id` from `providers__wi__template__real__v3_0.csv` |
| andor_practitioner_name | string | `NAME` from providers CSV |
| andor_specialty_nucc | string | `NUCC` |
| andor_specialty_text | string | `SPECIALTY` |
| andor_org_guid | string | target Andor org (links to organization_mapping.csv) |
| notes | string | mapping method (exact NPI, manual override) |

Inputs confirmed
- `providers__wi__template__real__v3_0.csv` columns: Id, NPI, NAME, SPECIALTY, NUCC, ADDRESS, CITY, STATE, ZIP (Wisconsin dictionary §2.4).
- US Core profile target: US Core 4.0.0 (dictionary shows `exporter.fhir.us_core_version` used = 4.0.0).

Join logic
1) Exact NPI match (canonical); normalize by stripping spaces.  
2) If multiple Practitioner resources share same NPI, keep first, log duplicates -> `notes="duplicate NPI"`.  
3) If NDJSON missing NPI, attempt parse from display; else mark `notes="manual override needed"` and add task.  
4) If NPI not in providers CSV, map to a generic Andor PCP of matching specialty; log as override.  
5) Persist CSV in repo under version control; include `source_system` to keep run-specific mappings.

## Organization mapping (organization_mapping.csv)

Schema
| column | type | description |
| --- | --- | --- |
| source_org_id | string | Organization.id from NDJSON |
| source_system | string | `synthea_andor_1000` or `synthea_generic_6_clinic` |
| org_guid | string | Canonical Andor org id (from Andor v5e hierarchy) |
| andor_org_name | string | Org name (system / hospital / clinic) |
| org_type | string | `system` \| `hospital` \| `clinic` \| `department` \| `service_line` |
| parent_org_guid | string | Parent org (e.g., all clinics -> health system) |
| notes | string | mapping comment |

Expected Andor hierarchy (from System Summary):  
- System: Andor Health System (AHS)  
- Hospitals: Tertiary 350-bed, Community 150-bed, Critical Access 25-bed  
- 400-provider multi-specialty group practice with clinics/departments.  
Action: extract real IDs/names from `Andor_Health_System_v5e.md` media or section listing orgs; populate org_guid and parent_org_guid accordingly.

Join logic
- Primary key: `source_org_id` -> org_guid (mapping table).  
- Fallback: infer org via practitioner’s mapped org if none present; otherwise flag missing.

## Replacement rules (per resource)

Replace references using practitioner_mapping and organization_mapping:
- Encounter: participant.individual (Practitioner), serviceProvider (Org), location.location (Org/Location link).
- DiagnosticReport: performer[], resultsInterpreter[] (Practitioner/Org).
- DocumentReference: author[], authenticator (Pract/Org), custodian (Org).
- CareTeam: participant.member (Pract/Org), managingOrganization (Org).
- MedicationRequest: requester, performer (Pract/Org).
- ServiceRequest: requester, performer[] (Pract/Org).
- Claim: provider (Org per Andor billing policy), careTeam[].provider, facility (Org).
- ExplanationOfBenefit: provider, contained.performer/requester, careTeam[].provider, facility (Org).
- Provenance: agent.who, agent.onBehalfOf (Pract/Org).

Validation after replacement
- 100% Encounters: serviceProvider mapped; ≥1 participant mapped.  
- Zero unmapped Practitioner/Organization references in target fields across all resources.  
- Emit `missing_mappings.csv` with resource id/type/path where mapping absent or ambiguous.

Data structures
- Hash maps: `npi -> practitioner mapping row`, `source_org_id -> org mapping row`.  
- Streaming transformer reads NDJSON, rewrites references, writes new NDJSON, then runs frequency/missingness counters.

## Practitioner↔Organization pairs (practitioner_org_pairs.csv)

| col | description |
| --- | --- |
| andor_practitioner_id | Canonical practitioner |
| andor_practitioner_name | Display |
| andor_org_guid | Org id |
| andor_org_name | Org display |
| encounter_count | # Encounters with this pair |
| run_id | e.g., `andor_1000_v5e` |

Checks: Σ encounter_count = total Encounters; flag nonsensical specialty-org pairings.

## Drilldowns (selection filters to apply after mapping)
- Pediatric/teen: already captured (Gabriela205, Bell723).  
- Elderly: Timothy142 Hyatt152 (82, deceased).  
- Multi-morbid adult: Edelmira985 Herzog843 (303 conditions, heavy utilization).  
- Deceased adult: Cristina921 Suárez24 (~67, deceased).  
- **Add** Specialist-heavy adult and Low-utilization adult using filters in `docs/todo_final.md`.

## ServiceRequest counting rule
- Minimal: standalone ServiceRequest only.  
- Full: standalone + `EOB.contained[*].resourceType=='ServiceRequest'`.  
Default: Full (Synthea EOB-only services observed: 14 contained SR for “Abe”).

## Coverage handling
- Wisconsin data dictionary includes Coverage NDJSON (Section 3.2).  
- If absent in a run, enable `exporter.fhir.included_resources` to include Coverage or synthesize from payer/plan CSVs; validate payor identifiers against `payers__andor__n8__v3_0__prod.csv` and `insurance_plans__andor__v3_0__prod.csv`.

## Generic clinic dimension
Use `generic_clinics.csv` rows 930001–930006 (primary care) and 930101–930104 (specialty) to build `generic_clinic_dimension.csv` with columns: org_guid, clinic_code, npi, clinic_name, clinic_type, city, zip. Link via Organization.identifier.value (provider_num or NPI) and Encounter.serviceProvider.

## Alignment with Andor v5e
- Profiles: US Core 4.0.0 (per data dictionary used value).  
- Attribution: PCP/clinic/service line/hospital/health system per v5e hierarchy.  
- Measures: prioritize Phase 1 gap measures listed in System Summary.
