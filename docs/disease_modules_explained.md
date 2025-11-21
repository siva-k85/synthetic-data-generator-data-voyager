# Synthea Disease Modules — Mechanics & GraphViz Notes

## Problem
We need to show disease progressions (state machines) and explain how modules interact, while keeping tooling reproducible (GraphViz rendering failed under Java 25 in this repo).

## Current State
- GraphViz now succeeds under **Java 21**. PNG/SVG graphs emitted to `output/graphviz/`.
- Failure under Java 25 was due to Graal/Unsafe; resolved by exporting `JAVA_HOME=/Library/Java/JavaVirtualMachines/temurin-21.jdk/Contents/Home` before running `./gradlew graphviz`.

## First Principles: How Synthea modules work
- Each module is a JSON state machine:
  - **States**: clinical milestones (Initial, Onset, Follow‑up, Complication).
  - **Transitions**: probabilities or guard conditions (age, BMI, comorbid conditions).
  - **Actions**: create FHIR resources (ConditionOnset, Encounter, Procedure, MedicationRequest, Observation, CarePlanStart, etc.).
- Modules can reference patient attributes and other active conditions (e.g., diabetes module checks for hypertension to branch to combined care pathways).
- Paired modules:
  - *metabolic_syndrome_disease* generates diabetes/CKD complications.
  - *metabolic_syndrome_care* drives longitudinal management (A1c labs, eye/foot exams).
  - Similar pair: *hypertension* (disease) + downstream cardiac care modules.

## How to render module graphs (fix)
1) Switch to Java 21 for the build:
   ```bash
   export JAVA_HOME=/Library/Java/JavaVirtualMachines/temurin-21.jdk/Contents/Home
   ./gradlew --stop
   ```
2) Ensure GraphViz CLI installed and on PATH:
   ```bash
   dot -V
   ```
3) Run:
   ```bash
   ./gradlew graphviz
   ```
4) Output lands in `output/graphviz/*.png` and `*.svg`. Include key PNGs (diabetes/metabolic_syndrome_disease, hypertension, chronic_kidney_disease) in GitBook.

## What to document (for GitBook)
- Diagram snapshots of the three critical modules (diabetes/metabolic syndrome, hypertension, CKD).
- Call out interaction points:
  - Diabetes → neuropathy/retinopathy/kidney branches.
  - Hypertension → cardiac risk pathways.
  - CKD progression stages and mortality guard.
- Execution order: Synthea evaluates all active modules each timestep; state entry/exit can set patient attributes consumed by other modules (e.g., “has_hypertension”).

## Validation steps after rendering
- Confirm state counts match JSON (e.g., metabolic_syndrome_disease has 32 states).
- Check transitions with guards (age/BMI/comorbidity) appear in the graph.
- Verify terminal and loopback states are present (e.g., Delay + counter loops).

## If GraphViz still fails
- Run with `./gradlew graphviz --info` to confirm JAVA_HOME in use.
- As fallback, manually render with `dot`:
  ```bash
  python scripts/export_module_dot.py modules/metabolic_syndrome_disease.json > /tmp/ms.dot
  dot -Tpng /tmp/ms.dot -o /tmp/ms.png
  ```
- If Graal errors persist, add `--enable-native-access=ALL-UNNAMED` to Gradle JVM args (only after confirming Java 21).
