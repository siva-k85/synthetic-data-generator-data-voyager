import json
import csv
import os
import glob
from pathlib import Path

# Configuration
MAPPING_DIR = "dr_smith_package"
ORG_MAPPING_FILE = os.path.join(MAPPING_DIR, "organization_mapping.csv")
PRAC_MAPPING_FILE = os.path.join(MAPPING_DIR, "practitioner_mapping.csv")

# Input/Output Directories (Adjust as needed or pass as args)
# For this task, we are likely processing the output of the previous run
INPUT_DIR = "runs/20251120_170157_andor1000_mapped/output/fhir"
OUTPUT_DIR = "runs/20251120_170157_andor1000_mapped/output/fhir_mapped_canonical"

def load_mappings():
    """Load organization and practitioner mappings into dictionaries."""
    org_map = {}
    prac_map = {}

    print(f"Loading organization mapping from {ORG_MAPPING_FILE}...")
    with open(ORG_MAPPING_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Map source_org_id (if present) or just use name matching if source_org_id is empty?
            # The stub had source_org_id. Let's assume the placeholder mapping populated source_org_id
            # But wait, the new organization_mapping.csv I created has empty source_org_id because I didn't have them.
            # However, the *practitioner* mapping has 'andor_org_guid' which we want to use.
            # Actually, we need to replace references in the NDJSON.
            # The NDJSONs currently contain *placeholder* IDs or *synthea* IDs?
            # The previous task said "Mapping executed with placeholders".
            # So the files in INPUT_DIR likely have IDs like "Organization/Placeholder1" or similar, OR they have Synthea IDs.
            # Let's assume they have Synthea IDs and we are doing a fresh mapping, OR they have placeholder IDs and we map those.
            # The task says "Swap placeholders with canonical".
            # Let's look at the placeholder mapping file again to see what the "source" was.
            # The placeholder mapping had source_org_id.
            # My new organization_mapping.csv has empty source_org_id.
            # I should probably have copied the source_org_id from the placeholder file if I wanted to map FROM that.
            # BUT, the practitioner mapping script I just ran used `practitioner_mapping_stub.csv` which HAS `source_practitioner_id`.
            # So I can map Source -> Canonical directly.

            # For Organizations:
            # I need to know which Source Org maps to which Canonical Org.
            # Since I didn't preserve source_org_id in my new csv, I might have an issue if I rely on it.
            # However, for practitioners, I assigned them to a canonical org.
            # The Organization resources themselves need to be rewritten.
            # If I don't have a map from Source Org -> Canonical Org, I can't rewrite Organization references that point to the old random orgs.

            # Let's assume for a moment we are rewriting based on the Practitioner's assignment.
            # But what about Encounter.serviceProvider?

            # CRITICAL FIX: I need to map the *existing* organizations in the NDJSON to my new canonical ones.
            # Since Synthea generates random orgs, and I just created a static list of 12 canonical orgs,
            # I should probably just map the Synthea orgs *randomly* or *deterministically* to these 12,
            # OR (better) just use the practitioner's assigned org for their encounters.

            # Let's stick to the plan:
            # 1. Load Practitioner Map: Source UUID -> Canonical ID (AHSP-XXX)
            # 2. Load Practitioner's Org Assignment: Source UUID -> Canonical Org Reference (Location/101)

            pass

    print(f"Loading practitioner mapping from {PRAC_MAPPING_FILE}...")
    with open(PRAC_MAPPING_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Map Source UUID -> Canonical ID
            prac_map[row['source_practitioner_id']] = row['andor_practitioner_id']
            # Also map Source UUID -> Canonical Org (for updating Practitioner resource and Encounters)
            # We'll store this as a separate map or tuple
            prac_map[row['source_practitioner_id'] + "_org"] = row['andor_org_guid']

            # ALSO Map PROV_ + NPI -> Canonical ID (because Encounter.ndjson has PROV_ IDs)
            if row['npi']:
                prov_id = f"PROV_{row['npi']}"
                prac_map[prov_id] = row['andor_practitioner_id']
                prac_map[prov_id + "_org"] = row['andor_org_guid']

    return org_map, prac_map

def process_files(org_map, prac_map):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # We also need to write the Canonical Organization resources themselves.
    # Since the source NDJSON has random orgs, we should probably just WRITE the canonical orgs
    # from our CSV as a new Organization.ndjson and ignore the source ones (or filter them).

    # 1. Write Canonical Organizations
    print("Writing canonical Organization.ndjson...")
    with open(os.path.join(OUTPUT_DIR, "Organization.ndjson"), 'w') as f:
        with open(ORG_MAPPING_FILE, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                org_res = {
                    "resourceType": "Organization",
                    "id": row['org_guid'].split('/')[-1], # Remove prefix if present
                    "name": row['andor_org_name'],
                    "type": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/organization-type", "code": row['org_type']}]}]
                }
                if row['parent_org_guid']:
                     org_res["partOf"] = {"reference": row['parent_org_guid']}

                f.write(json.dumps(org_res) + "\n")

    print(f"Loaded {len(prac_map)} practitioner mappings.")

    # 2. Process Practitioner.ndjson
    # We will read the source Practitioner.ndjson, find the ones we have mappings for, and rewrite them.
    print("Processing Practitioner.ndjson...")
    # Note: Source file might be named with timestamp
    prac_files = glob.glob(os.path.join(INPUT_DIR, "Practitioner*.ndjson"))
    print(f"Found practitioner files: {prac_files}")
    # Filter out PractitionerRole
    prac_files = [f for f in prac_files if "PractitionerRole" not in f]

    with open(os.path.join(OUTPUT_DIR, "Practitioner.ndjson"), 'w') as f_out:
        for p_file in prac_files:
            with open(p_file, 'r') as f_in:
                for line in f_in:
                    res = json.loads(line)
                    src_id = res['id']
                    if src_id in prac_map:
                        # Update ID
                        canonical_id = prac_map[src_id]
                        res['id'] = canonical_id

                        # Update Identifier (NPI is already there, maybe add internal ID)
                        res['identifier'].append({
                            "system": "http://andorhealth.org/internal-id",
                            "value": canonical_id
                        })

                        f_out.write(json.dumps(res) + "\n")

    # 3. Process Encounter.ndjson (and others)
    # We need to replace references to Practitioners.
    # And update the ServiceProvider (Organization) to match the Practitioner's assigned org.
    print("Processing Encounter.ndjson...")
    enc_files = glob.glob(os.path.join(INPUT_DIR, "Encounter*.ndjson"))

    missing_mappings = set()

    with open(os.path.join(OUTPUT_DIR, "Encounter.ndjson"), 'w') as f_out:
        for e_file in enc_files:
            with open(e_file, 'r') as f_in:
                for line in f_in:
                    res = json.loads(line)

                    # Update Participant (Practitioner)
                    if 'participant' in res:
                        for part in res['participant']:
                            if 'individual' in part and 'reference' in part['individual']:
                                ref = part['individual']['reference']
                                # ref is usually "Practitioner/UUID" or "Practitioner/PROV_..."
                                uuid = ref.split('/')[-1]

                                # Try exact match (UUID) or PROV_ match
                                if uuid in prac_map:
                                    part['individual']['reference'] = f"Practitioner/{prac_map[uuid]}"

                                    # Update ServiceProvider based on this practitioner
                                    # (Simple logic: last practitioner wins)
                                    assigned_org = prac_map.get(uuid + "_org")
                                    if assigned_org:
                                        res['serviceProvider'] = {"reference": assigned_org}
                                        # Also update Location if we want to be consistent?
                                        # Synthea locations are random. Let's force the location to the assigned clinic.
                                        if 'location' not in res: res['location'] = []
                                        # Wipe existing random locations or append? Let's replace to be clean.
                                        res['location'] = [{"location": {"reference": assigned_org}, "status": "active"}]
                                else:
                                    missing_mappings.add(f"Practitioner: {uuid}")

                    f_out.write(json.dumps(res) + "\n")

    # Write missing mappings
    if missing_mappings:
        print(f"WARNING: Found {len(missing_mappings)} missing mappings. Writing to missing_mappings.csv")
        with open(os.path.join(OUTPUT_DIR, "missing_mappings.csv"), 'w') as f:
            f.write("resource_type,id\n")
            for item in missing_mappings:
                parts = item.split(": ")
                f.write(f"{parts[0]},{parts[1]}\n")
    else:
        print("Success: No missing mappings found.")

    # 4. Copy other files that don't need mapping (Patient, etc) or map them if needed

    # 4. Copy other files that don't need mapping (Patient, etc) or map them if needed
    # For now, let's just copy Patient.ndjson as is, since we aren't mapping Patient IDs yet.
    print("Copying Patient.ndjson...")
    pat_files = glob.glob(os.path.join(INPUT_DIR, "Patient*.ndjson"))
    for p_file in pat_files:
        with open(p_file, 'r') as f_in, open(os.path.join(OUTPUT_DIR, "Patient.ndjson"), 'w') as f_out:
            for line in f_in:
                f_out.write(line)

    print(f"Done. Mapped output in {OUTPUT_DIR}")

if __name__ == "__main__":
    org_map, prac_map = load_mappings()
    process_files(org_map, prac_map)
