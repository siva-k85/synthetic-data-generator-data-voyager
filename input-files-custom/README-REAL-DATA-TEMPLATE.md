# Payers – Real Data Replacement Template

Use this template to replace synthetic payers with real Wisconsin insurers. Keep this file in the same folder as the active mixed file so the pathing in docs stays consistent.

## Files
- `payers_wisconsin_REAL_TEMPLATE.csv` – Empty CSV with required columns. Fill it with verified real data and then point `generate.payers.insurance_companies.default_file` in `02_CONFIGURATION/synthea.properties` to your completed file.

## Required Columns (in order)
- `Id` – Stable identifier (string). Use a consistent scheme (e.g., NAIC code prefixed or a local ID).
- `Name` – Legal plan/insurer name.
- `Address`, `City`, `State Headquartered`, `Zip` – Headquarters postal address.
- `Phone` – Main contact in `###-###-####` format.
- `States Covered` – Pipe- or comma-separated list. Use `WI` at minimum.
- `Ownership` – One of: `Government`, `Private`, `Nonprofit`, `Self-Pay`.
- `Plan_Type` – Medicare/Medicaid/Commercial/Exchange/MA/HMO/PPO as applicable.
- `NAIC_Code` – Official NAIC code or `N/A-Federal` for CMS programs.
- `Market_Share` – Decimal proportion (0–1). All rows must sum to 1.0.
- `Default_Deductible`, `Default_Coinsurance`, `Default_Copay`, `Monthly_Premium` – Typical plan-level defaults for simulation (use 0 if not applicable).
- `Notes` – Free text for provenance and QA reminders.

## Completion Checklist
1. All rows use real, verified names and addresses (no placeholders).
2. `Phone` fields are real numbers (no `SYNTHETIC-XXXX`).
3. `NAIC_Code` values are real or `N/A-Federal` for CMS.
4. `Market_Share` sums to exactly 1.0.
5. Document sources (OCI filings, CMS, plan websites) in `Notes` and/or commit message.
6. Update `02_CONFIGURATION/synthea.properties` to point to your completed CSV and record the change in `04_VALIDATION_REPORTS/INPUT_VALIDATION_CHECKLIST.md`.

## Validation Snippets
```python
# Sum of Market_Share must be 1.0
import csv
rows=list(csv.DictReader(open('payers_wisconsin_REAL_TEMPLATE.csv')))
assert abs(sum(float(r['Market_Share']) for r in rows) - 1.0) < 1e-9

# Phone format check
import re
assert all(re.match(r'^\d{3}-\d{3}-\d{4}$', r['Phone']) for r in rows)
```

## Activation
Once populated and validated, set in `02_CONFIGURATION/synthea.properties`:
```
generate.payers.insurance_companies.default_file = .../payers_wisconsin_REAL_TEMPLATE.csv
```

