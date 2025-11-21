import json
import os
import glob
import csv
from datetime import datetime
from collections import defaultdict

# Configuration
INPUT_DIR = "runs/20251120_170157_andor1000_mapped/output/fhir_mapped_canonical"
OUTPUT_DIR = "runs/20251120_170157_andor1000_mapped/output/drilldowns"
MAPPING_DIR = "dr_smith_package"

TARGET_PATIENTS = [
    {"id": "ab4a622d-fecf-7852-bc88-6371a067070f", "label": "Specialist-heavy Adult"},
    {"id": "06ca6d0f-2c77-654d-4690-88feb73a0330", "label": "Low-utilization Adult"}
]

def load_mappings():
    """Loads practitioner and organization mappings for name resolution."""
    prac_names = {}
    org_names = {}

    # Practitioner Names from CSV
    with open(os.path.join(MAPPING_DIR, "practitioner_mapping.csv"), 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            prac_names[row['andor_practitioner_id']] = row['andor_practitioner_name']

    # Organization Names from NDJSON
    org_file = os.path.join(INPUT_DIR, "Organization.ndjson")
    if os.path.exists(org_file):
        with open(org_file, 'r') as f:
            for line in f:
                res = json.loads(line)
                # Map both "Organization/ID" and just "ID"
                org_names[res['id']] = res['name']
                org_names[f"Organization/{res['id']}"] = res['name']
                # Also handle Location/ID if we can infer it?
                # Actually, Location resources are not in Organization.ndjson.
                # But our mapping CSV had Location/ID.
                # For now, let's just use the ID itself if name not found.

    return prac_names, org_names

def load_patient_data(patient_id):
    """Extracts all resources for a specific patient."""
    data = {
        "Patient": None,
        "Encounter": [],
        "Condition": [],
        "Procedure": [],
        "Immunization": []
    }

    # Patient
    with open(os.path.join(INPUT_DIR, "Patient.ndjson"), 'r') as f:
        for line in f:
            res = json.loads(line)
            if res['id'] == patient_id:
                data["Patient"] = res
                break

    # Other resources
    for r_type in ["Encounter", "Condition", "Procedure", "Immunization"]:
        files = glob.glob(os.path.join(INPUT_DIR, f"{r_type}*.ndjson"))
        for file in files:
            with open(file, 'r') as f:
                for line in f:
                    res = json.loads(line)
                    # Check subject reference
                    if 'subject' in res and res['subject']['reference'] == f"Patient/{patient_id}":
                        data[r_type].append(res)
                    elif 'patient' in res and res['patient']['reference'] == f"Patient/{patient_id}": # Immunization uses patient
                        data[r_type].append(res)

    return data

def build_timeline(data):
    """Constructs a chronological timeline of events."""
    timeline = []

    for enc in data["Encounter"]:
        start = enc['period']['start']
        timeline.append({
            "date": start,
            "type": "Encounter",
            "description": enc['type'][0]['text'] if 'type' in enc else "Encounter",
            "resource": enc
        })

    for cond in data["Condition"]:
        date = cond.get('onsetDateTime', cond.get('recordedDate'))
        if date:
            timeline.append({
                "date": date,
                "type": "Condition",
                "description": cond['code']['text'] if 'code' in cond else "Condition",
                "resource": cond
            })

    for proc in data["Procedure"]:
        date = proc.get('performedDateTime')
        if date:
            timeline.append({
                "date": date,
                "type": "Procedure",
                "description": proc['code']['text'] if 'code' in proc else "Procedure",
                "resource": proc
            })

    # Sort by date
    timeline.sort(key=lambda x: x['date'])
    return timeline

def calculate_attribution(encounters, prac_names):
    """Calculates PCP attribution based on plurality."""
    scores = defaultdict(int)

    for enc in encounters:
        # Check if ambulatory
        is_amb = False
        if 'class' in enc and enc['class']['code'] == 'AMB':
            is_amb = True

        if is_amb and 'participant' in enc:
            for part in enc['participant']:
                if 'individual' in part:
                    ref = part['individual']['reference'] # Practitioner/AHSP-XXXX
                    pid = ref.split('/')[-1]
                    scores[pid] += 1

    if not scores:
        return "None"

    top_doc_id = max(scores, key=scores.get)
    doc_name = prac_names.get(top_doc_id, top_doc_id)
    return f"{doc_name} ({top_doc_id}) - {scores[top_doc_id]} visits"

def detect_care_gaps(timeline):
    """Detects gaps > 365 days between ambulatory encounters."""
    gaps = []
    last_date = None

    for event in timeline:
        if event['type'] == 'Encounter':
            # Check if ambulatory
            is_amb = False
            enc = event['resource']
            if 'class' in enc and enc['class']['code'] == 'AMB':
                is_amb = True

            if is_amb:
                current_date = datetime.fromisoformat(event['date'].replace('Z', '+00:00'))
                if last_date:
                    delta = (current_date - last_date).days
                    if delta > 365:
                        gaps.append({
                            "start": last_date.strftime('%Y-%m-%d'),
                            "end": current_date.strftime('%Y-%m-%d'),
                            "days": delta
                        })
                last_date = current_date

    return gaps

def generate_report(patient_info, data, prac_names, org_names):
    """Generates Markdown report."""
    pid = patient_info['id']
    label = patient_info['label']
    patient = data['Patient']

    if not patient:
        return f"Error: Patient {pid} not found."

    name = f"{patient['name'][0]['given'][0]} {patient['name'][0]['family']}"
    dob = patient['birthDate']
    gender = patient['gender']

    timeline = build_timeline(data)
    attribution = calculate_attribution(data['Encounter'], prac_names)
    gaps = detect_care_gaps(timeline)

    md = f"# Patient Drilldown: {label}\n\n"
    md += f"**Patient**: {name}\n"
    md += f"**ID**: `{pid}`\n"
    md += f"**DOB**: {dob} ({gender})\n"
    md += f"**Attributed PCP**: {attribution}\n\n"

    md += "## Care Gaps (>365 days)\n"
    if gaps:
        for gap in gaps:
            md += f"- **{gap['days']} days** from {gap['start']} to {gap['end']}\n"
    else:
        md += "- No significant care gaps detected.\n"

    md += "\n## Clinical Timeline\n\n"
    md += "| Date | Type | Description | Provider/Org |\n"
    md += "|---|---|---|---|\n"

    for event in timeline:
        date_str = event['date'][:10]
        desc = event['description']

        prov_str = ""
        if event['type'] == 'Encounter':
            enc = event['resource']
            if 'participant' in enc:
                ref = enc['participant'][0]['individual']['reference']
                pid = ref.split('/')[-1]
                prov_str = prac_names.get(pid, pid)
            if 'serviceProvider' in enc:
                org_ref = enc['serviceProvider']['reference']
                oid = org_ref.split('/')[-1]
                # Try full ref first, then ID
                org_name = org_names.get(org_ref, org_names.get(oid, oid))
                prov_str += f" @ {org_name}"

        md += f"| {date_str} | {event['type']} | {desc} | {prov_str} |\n"

    return md

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print("Loading mappings...")
    prac_names, org_names = load_mappings()

    for target in TARGET_PATIENTS:
        print(f"Processing {target['label']} ({target['id']})...")
        data = load_patient_data(target['id'])
        report = generate_report(target, data, prac_names, org_names)

        filename = f"drilldown_{target['id']}.md"
        with open(os.path.join(OUTPUT_DIR, filename), 'w') as f:
            f.write(report)
        print(f"Generated {filename}")

if __name__ == "__main__":
    main()
