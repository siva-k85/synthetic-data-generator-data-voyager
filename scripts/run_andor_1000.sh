#!/usr/bin/env bash
# Wisconsin/Andor 1000‑patient run with network=true and US Core 6.1.0
# Uses existing CSVs in payers/, providers/, geography/ as configured.

set -euo pipefail

SEED=${SEED:-5150}
CLIN_SEED=${CLIN_SEED:-5150}
STAMP=$(date +"%Y%m%d_%H%M%S")
RUN_DIR="runs/${STAMP}_andor1000"
OUT_DIR="${RUN_DIR}/output"

mkdir -p "${OUT_DIR}/hashes" "${RUN_DIR}/logs"

CMD=(./run_synthea
  -p 1000
  -s "${SEED}"
  -cs "${CLIN_SEED}"
  Wisconsin
  --exporter.baseDirectory="${OUT_DIR}"
  --exporter.fhir.export=true
  --exporter.fhir.bulk_data=true
  --exporter.csv.export=true
  --exporter.fhir.use_us_core_ig=true
  --exporter.fhir.us_core_version=6.1.0
  --generate.providers.selection_behavior=network
)

{
  echo "Command: ${CMD[*]}"
  echo "Timestamp: $(date -Is)"
  echo "Seeds: patient=${SEED}, clinician=${CLIN_SEED}"
  echo "Note: relies on geography/payers/providers CSVs already set in synthea.properties"
} > "${RUN_DIR}/GENERATION_PROOF.txt"

echo "⏳ Running Andor Wisconsin 1000…"
"${CMD[@]}" | tee "${RUN_DIR}/logs/gradle.log"

echo "🔒 Hashing NDJSON outputs…"
if compgen -G "${OUT_DIR}/fhir/*.ndjson" > /dev/null; then
  find "${OUT_DIR}/fhir" -maxdepth 1 -name "*.ndjson" -print0 \
    | sort -z \
    | xargs -0 sha256sum > "${OUT_DIR}/hashes/sha256.txt"
else
  echo "No NDJSON files found in ${OUT_DIR}/fhir; hash file not created." | tee -a "${RUN_DIR}/GENERATION_PROOF.txt"
fi

echo "✅ Done. Outputs: ${OUT_DIR}"
