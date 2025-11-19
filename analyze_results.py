import csv
import collections
import os

def analyze_csvs():
    print("--- Analysis Report ---")

    # 0. Load Payer Names
    payer_names = {}
    try:
        with open('output/csv/payers.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                payer_names[row['Id']] = row['NAME']
    except Exception as e:
        print(f"Error reading payers.csv: {e}")

    # 1. Payer Mix (Latest)
    latest_payer = {} # Patient ID -> (Start Date, Payer ID)
    try:
        with open('output/csv/payer_transitions.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                pid = row['PATIENT']
                start_date = row['START_DATE']
                payer_id = row['PAYER']

                if pid not in latest_payer or start_date > latest_payer[pid][0]:
                    latest_payer[pid] = (start_date, payer_id)

        payer_counts = collections.Counter()
        for pid, (date, payer_id) in latest_payer.items():
            payer_name = payer_names.get(payer_id, payer_id)
            payer_counts[payer_name] += 1

        print("\nPayer Mix (Latest):")
        for payer, count in payer_counts.most_common():
            print(f"{payer}: {count}")
    except Exception as e:
        print(f"Error reading payer_transitions.csv: {e}")

    # 2. Provider Utilization
    provider_counts = collections.Counter()
    try:
        with open('output/csv/encounters.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                provider_counts[row['PROVIDER']] += 1

        print("\nTop 10 Providers by Encounters:")
        for provider, count in provider_counts.most_common(10):
            print(f"{provider}: {count}")
    except Exception as e:
        print(f"Error reading encounters.csv: {e}")

    # 3. Diabetes Prevalence
    diabetes_patients = set()
    try:
        with open('output/csv/conditions.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'Diabetes' in row['DESCRIPTION']:
                    diabetes_patients.add(row['PATIENT'])

        print(f"\nPatients with Diabetes: {len(diabetes_patients)}")
    except Exception as e:
        print(f"Error reading conditions.csv: {e}")

    # 4. Total Patients
    try:
        with open('output/csv/patients.csv', 'r') as f:
            # Subtract header
            total_patients = sum(1 for line in f) - 1
        print(f"\nTotal Patients: {total_patients}")
    except Exception as e:
        print(f"Error reading patients.csv: {e}")

if __name__ == "__main__":
    analyze_csvs()
