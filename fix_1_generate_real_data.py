"""
CRITICAL: Generate ACTUAL Synthea data and analyze it
This proves to Dr. Smith you can execute, not just theorize
"""

import subprocess
import json
import os
import hashlib
from datetime import datetime
from pathlib import Path
import statistics

def generate_synthea_population():
    """Actually run Synthea and capture output"""

    # Create output directory
    output_dir = Path("actual_output_v3.4")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Run Synthea with EXACT configuration using the local wrapper
    # Note: run_synthea uses Gradle, so we pass arguments to it.
    cmd = [
        "./run_synthea",
        "-c", "synthea.properties",
        "Wisconsin"
    ]

    print(f"Executing: {' '.join(cmd)}")

    # Capture the actual generation
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Save generation log as PROOF
    with open(output_dir / "GENERATION_PROOF.txt", "w") as f:
        f.write(f"Command: {' '.join(cmd)}\n")
        f.write(f"Timestamp: {datetime.now()}\n")
        f.write(f"Output:\n{result.stdout}\n")
        f.write(f"Errors:\n{result.stderr}\n")

    if result.returncode != 0:
        print("Synthea execution failed!")
        print(result.stderr)
        return output_dir

    # Hash the output files to prove they're real
    fhir_dir = Path("output/fhir")
    file_hashes = {}

    if fhir_dir.exists():
        for json_file in fhir_dir.glob("*.ndjson"):
            with open(json_file, 'rb') as f:
                file_hashes[json_file.name] = hashlib.sha256(f.read()).hexdigest()

    # Save hashes as verification
    with open(output_dir / "FILE_VERIFICATION.json", "w") as f:
        json.dump(file_hashes, f, indent=2)

    return output_dir

def analyze_actual_output(output_dir):
    """Analyze REAL Synthea output, not theoretical"""

    analysis = {
        "generation_timestamp": datetime.now().isoformat(),
        "total_files": 0,
        "patients": {},
        "encounters": {},
        "conditions": {},
        "procedures": {},
        "observations": {}
    }

    # Count actual FHIR resources
    fhir_dir = Path("output/fhir")

    if not fhir_dir.exists():
        print("Output directory not found!")
        return analysis

    # Read actual Patient resources
    patients = []
    patient_file = fhir_dir / "Patient.ndjson"
    if patient_file.exists():
        with open(patient_file, 'r') as f:
            for line in f:
                patient = json.loads(line)
                patients.append(patient)

    analysis["total_files"] = len(list(fhir_dir.glob("*.ndjson")))
    analysis["patients"]["count"] = len(patients)

    # REAL age distribution
    ages = []
    now = datetime.now()
    for p in patients:
        birth_date_str = p.get('birthDate')
        if birth_date_str:
            birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
            age = (now - birth_date).days / 365.25
            ages.append(age)

    if ages:
        analysis["patients"]["age_distribution"] = {
            "0-18": sum(1 for a in ages if a < 18),
            "18-64": sum(1 for a in ages if 18 <= a < 65),
            "65+": sum(1 for a in ages if a >= 65),
            "mean_age": statistics.mean(ages),
            "median_age": statistics.median(ages)
        }

    # Save REAL analysis
    with open(output_dir / "ACTUAL_ANALYSIS.json", "w") as f:
        json.dump(analysis, f, indent=2)

    print(f"✅ Generated REAL data: {len(patients)} patients")
    print(f"✅ Files created: {analysis['total_files']}")
    if 'age_distribution' in analysis['patients']:
        print(f"✅ Medicare eligible (65+): {analysis['patients']['age_distribution']['65+']}")

    return analysis

if __name__ == "__main__":
    # EXECUTE NOW
    output = generate_synthea_population()
    results = analyze_actual_output(output)
