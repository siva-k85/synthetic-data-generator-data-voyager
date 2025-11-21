#!/usr/bin/env python3
"""
Compute basic frequency metrics for Synthea runs.
Outputs go into the package: siva_synthea_andor_phase1_v1.0_20251121/02_outputs/<run>/analysis
"""
import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

PACKAGE = Path('siva_synthea_andor_phase1_v1.0_20251121').resolve()


def write_csv(path, rows, header):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def analyze_default():
    base = PACKAGE / '02_outputs/default_100_run/csv'
    conditions = base / 'conditions.csv'
    encounters = base / 'encounters.csv'
    providers = base / 'providers.csv'
    orgs = base / 'organizations.csv'
    outdir = PACKAGE / '02_outputs/default_100_run/analysis'

    if providers.exists():
        prac_counts = Counter()
        with providers.open() as f:
            for row in csv.DictReader(f):
                spec = row.get('SPECIALITY') or row.get('SPECIALTY') or 'unknown'
                prac_counts[spec] += 1
        rows = sorted(prac_counts.items(), key=lambda x: (-x[1], x[0]))
        write_csv(outdir/'practitioners_by_specialty.csv', rows, ['specialty','count'])

    if orgs.exists():
        org_counts = Counter()
        with orgs.open() as f:
            for row in csv.DictReader(f):
                typ = row.get('TYPE') or row.get('ORG_TYPE') or 'unknown'
                org_counts[typ] += 1
        rows = sorted(org_counts.items(), key=lambda x:(-x[1], x[0]))
        write_csv(outdir/'organizations_by_type.csv', rows, ['type','count'])

    if conditions.exists():
        disease_counts = Counter()
        with conditions.open() as f:
            for row in csv.DictReader(f):
                desc = row.get('DESCRIPTION') or row.get('CODE') or 'unknown'
                disease_counts[desc] += 1
        rows = sorted(disease_counts.items(), key=lambda x:(-x[1], x[0]))
        write_csv(outdir/'disease_counts.csv', rows, ['disease','count'])

    if encounters.exists():
        enc_by_patient = defaultdict(list)
        with encounters.open() as f:
            for row in csv.DictReader(f):
                pid = row.get('PATIENT') or row.get('PATIENT_ID')
                prov = row.get('PROVIDER')
                if pid and prov:
                    enc_by_patient[pid].append(prov)
        pcp_counts = Counter()
        for pid, provs in enc_by_patient.items():
            if not provs:
                continue
            top = Counter(provs).most_common(1)[0][0]
            pcp_counts[top] += 1
        rows = sorted(pcp_counts.items(), key=lambda x:(-x[1], x[0]))
        write_csv(outdir/'patients_per_pcp.csv', rows, ['provider_id','patient_count'])


def analyze_andor():
    base = PACKAGE / '02_outputs/andor_1000_run/fhir'
    prac_file = base/'Practitioner.ndjson'
    org_file = base/'Organization.ndjson'
    enc_file = base/'Encounter.ndjson'
    cond_file = base/'Condition.ndjson'
    outdir = PACKAGE / '02_outputs/andor_1000_run/analysis'

    if prac_file.exists():
        prac_counts = Counter()
        with prac_file.open() as f:
            for line in f:
                obj=json.loads(line)
                spec='unknown'
                qual=obj.get('qualification') or []
                if qual:
                    code=qual[0].get('code') or {}
                    coding=code.get('coding') or []
                    if coding:
                        spec=coding[0].get('display') or coding[0].get('code') or 'unknown'
                    else:
                        spec=code.get('text') or 'unknown'
                prac_counts[spec]+=1
        rows=sorted(prac_counts.items(), key=lambda x:(-x[1], x[0]))
        write_csv(outdir/'practitioners_by_specialty.csv', rows, ['specialty','count'])

    if org_file.exists():
        org_counts=Counter()
        with org_file.open() as f:
            for line in f:
                obj=json.loads(line)
                typ='unknown'
                types=obj.get('type') or []
                if types:
                    coding=types[0].get('coding') or []
                    if coding:
                        typ=coding[0].get('display') or coding[0].get('code') or 'unknown'
                    else:
                        typ=types[0].get('text') or 'unknown'
                org_counts[typ]+=1
        rows=sorted(org_counts.items(), key=lambda x:(-x[1], x[0]))
        write_csv(outdir/'organizations_by_type.csv', rows, ['type','count'])

    if cond_file.exists():
        disease_counts=Counter()
        with cond_file.open() as f:
            for line in f:
                obj=json.loads(line)
                code=obj.get('code',{})
                text=code.get('text')
                coding=code.get('coding') or []
                name=text or (coding[0].get('display') if coding else None) or 'unknown'
                disease_counts[name]+=1
        rows=sorted(disease_counts.items(), key=lambda x:(-x[1], x[0]))
        write_csv(outdir/'disease_counts.csv', rows, ['disease','count'])

    if enc_file.exists():
        enc_by_patient=defaultdict(list)
        with enc_file.open() as f:
            for line in f:
                obj=json.loads(line)
                patient_ref=(obj.get('subject') or obj.get('patient') or {}).get('reference','')
                if not patient_ref:
                    continue
                pid=patient_ref.split('/')[-1]
                participants=obj.get('participant') or []
                if not participants:
                    continue
                ind=participants[0].get('individual',{}).get('reference')
                if not ind:
                    continue
                prov_id=ind.split('/')[-1]
                enc_by_patient[pid].append(prov_id)
        pcp_counts=Counter()
        for pid, provs in enc_by_patient.items():
            top=Counter(provs).most_common(1)[0][0]
            pcp_counts[top]+=1
        rows=sorted(pcp_counts.items(), key=lambda x:(-x[1], x[0]))
        write_csv(outdir/'patients_per_pcp.csv', rows, ['practitioner_id','patient_count'])


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--run', choices=['default100','andor1000'], required=True)
    args=ap.parse_args()
    if args.run=='default100':
        analyze_default()
    else:
        analyze_andor()

if __name__=='__main__':
    main()
