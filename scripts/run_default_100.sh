#!/usr/bin/env bash
# Deterministic 100‑patient vanilla Synthea run (no custom CSVs)
# Output, logs, and proofs are isolated under runs/<timestamp>_default100/

set -euo pipefail

SEED=${SEED:-4242}
CLIN_SEED=${CLIN_SEED:-4242}
STAMP=$(date +"%Y%m%d_%H%M%S")
RUN_DIR="runs/${STAMP}_default100"
OUT_DIR="${RUN_DIR}/output"

mkdir -p "${OUT_DIR}/hashes" "${RUN_DIR}/logs"

CMD=(./run_synthea
  -p 100
  -s "${SEED}"
  -cs "${CLIN_SEED}"
  --exporter.baseDirectory="${OUT_DIR}"
  --exporter.fhir.export=true
  --exporter.fhir.bulk_data=true
  --exporter.csv.export=true
  --exporter.fhir.use_us_core_ig=true
  --exporter.fhir.us_core_version=6.1.0
)

{
  echo "Command: ${CMD[*]}"
  echo "Timestamp: $(date -Is)"
  echo "Seeds: patient=${SEED}, clinician=${CLIN_SEED}"
} > "${RUN_DIR}/GENERATION_PROOF.txt"

echo "⏳ Running default Synthea 100…"
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
