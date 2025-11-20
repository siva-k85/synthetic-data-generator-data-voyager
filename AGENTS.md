# AGENTS.md

**AI Coding Agent Reference for synthetic-data-generator-data-voyager**

This document provides comprehensive context and instructions for AI coding agents working on the Synthea-based synthetic patient population simulator repository.

---

## Table of Contents

1. [Quick Reference](#quick-reference)
2. [Project Overview](#project-overview)
3. [Development Environment](#development-environment)
4. [Project Architecture](#project-architecture)
5. [Building and Running](#building-and-running)
6. [Testing](#testing)
7. [Code Quality](#code-quality)
8. [Configuration Management](#configuration-management)
9. [Output Formats](#output-formats)
10. [Disease Modules](#disease-modules)
11. [Debugging and Troubleshooting](#debugging-and-troubleshooting)
12. [CI/CD Pipeline](#cicd-pipeline)
13. [Production Runs](#production-runs)
14. [Git Workflow](#git-workflow)
15. [Key Files and Directories](#key-files-and-directories)
16. [Common Workflows](#common-workflows)
17. [Performance Optimization](#performance-optimization)
18. [Python Analysis Scripts](#python-analysis-scripts)
19. [Important Notes for AI Agents](#important-notes-for-ai-agents)

---

## Quick Reference

### Most Common Commands

```bash
# Build the project
./gradlew build

# Run all tests and checks
./gradlew check

# Generate synthetic patients (default: 10 patients, Massachusetts)
./gradlew run
# or
./run_synthea

# Generate with options
./run_synthea -p 1000 -s 12345 Wisconsin Madison

# Generate module visualizations
./gradlew graphviz

# Run tests only
./gradlew test

# View test coverage
./gradlew jacocoTestReport
# Then open: build/reports/jacoco/test/html/index.html

# Generate concept list
./gradlew concepts

# Generate patient attributes list
./gradlew attributes

# Clean output directory
./gradlew cleanOutput
```

### Critical Environment Variables

```bash
# Set Java version (REQUIRED: Java 11-21)
export JAVA_HOME=/path/to/jdk-21

# Set max heap for generation
export MAX_HEAP_SIZE=4096m
```

---

## Project Overview

**Synthea™** is a Synthetic Patient Population Simulator that generates realistic (but not real) patient data and associated health records in multiple formats.

### Key Features

- **Birth to Death Lifecycle**: Complete patient life simulation
- **Configuration-based Demographics**: Defaults to Massachusetts Census data, customizable
- **Modular Rule System**: 24+ disease/clinical modules (JSON-based)
- **Multiple Export Formats**:
  - FHIR R4, STU3, DSTU2
  - C-CDA
  - CSV
  - CPCDS (Claims and Patient-centered Data Standard)
  - BFD (Beneficiary FHIR Data)
- **Visualization**: Graphviz-based disease module diagrams

### Technology Stack

- **Language**: Java 11+ (sourceCompatibility)
- **Build System**: Gradle 8.14+ (Wrapper provided)
- **Testing**: JUnit 4, Mockito, PowerMock
- **Healthcare Standards**: FHIR (HAPI FHIR 6.1.0), HL7, C-CDA
- **Core Libraries**:
  - Apache Commons (CSV, Math, Text, Validator)
  - Jackson (JSON/CSV processing)
  - FreeMarker (C-CDA templates)
  - Graphviz Java (visualization)
  - JSBML (physiology simulation)
  - CQL Engine (clinical quality language)

### Repository Origin

This is a fork/clone of the MITRE Synthea project (`org.mitre.synthea`) with custom configurations and production-scale data generation capabilities.

---

## Development Environment

### Java Version Requirements

**CRITICAL**: Use **Java 11, 17, or 21** (LTS releases recommended)

#### DO NOT USE:
- ❌ Java 22+
- ❌ Java 25 (causes "Unsupported class file major version 69" errors with current Gradle/Groovy setup)

#### Recommended:
- ✅ Java 11 (minimum, baseline compatibility)
- ✅ Java 17 (tested in CI)
- ✅ Java 21 (recommended for development, best compatibility)

### Setting Up Java

**macOS (Homebrew)**:
```bash
brew install openjdk@21
export JAVA_HOME=/Library/Java/JavaVirtualMachines/temurin-21.jdk/Contents/Home
```

**Linux (apt)**:
```bash
sudo apt install openjdk-21-jdk
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
```

**Verify**:
```bash
java -version
# Should show: openjdk version "21.x.x" or similar
```

### Required Tools

1. **Git**: For version control
2. **Graphviz**: Required for `./gradlew graphviz` task
   ```bash
   # macOS
   brew install graphviz

   # Ubuntu/Debian
   sudo apt install graphviz

   # Verify
   dot -V
   ```
3. **Python 3**: For analysis scripts (optional)
   ```bash
   pip install pandas
   ```

### IDE Setup

**IntelliJ IDEA**:
- Use Gradle import (auto-detected)
- Set Project SDK to Java 11/17/21
- Enable Checkstyle plugin (config: `config/checkstyle/`)

**Eclipse**:
```bash
./gradlew eclipse
```

**VS Code**:
- Install "Extension Pack for Java"
- Install "Gradle for Java"

---

## Project Architecture

### Package Structure

```
org.mitre.synthea/
├── engine/               # Core simulation engine
│   ├── Generator.java   # Main patient generation orchestrator
│   ├── Module.java      # Disease module state machine
│   ├── State.java       # Module state definitions
│   └── Logic.java       # Conditional logic for state transitions
├── world/               # Entity models
│   ├── agents/         # Person, Provider, Clinician, Payer
│   ├── concepts/       # HealthRecord, VitalSign, ClinicianSpecialty
│   └── geography/      # Location, Demographics
├── export/              # Export formatters
│   ├── FHIRExporter.java (+ STU3, DSTU2)
│   ├── CCDAExporter.java
│   ├── CSVExporter.java
│   ├── CPCDSExporter.java
│   └── Exporter.java   # Base exporter interface
├── modules/             # Module loading and management
│   ├── CardiovascularDiseaseModule.java
│   ├── DeathModule.java
│   └── EncounterModule.java
├── helpers/             # Utilities
│   ├── Config.java     # Configuration management
│   ├── Concepts.java   # Concept list generator
│   ├── Attributes.java # Attribute list generator
│   └── Utilities.java  # General utilities
└── App.java            # Main entry point
```

### Key Classes and Their Roles

| Class | Purpose |
|-------|---------|
| `App.java` | Main entry point, CLI argument parsing, simulation orchestration |
| `Generator.java` | Patient generation engine, runs modules, manages timeline |
| `Module.java` | State machine executor for disease/clinical modules |
| `Person.java` | Patient entity with attributes, vital signs, health record |
| `Provider.java` | Healthcare organization (hospital, clinic) |
| `Clinician.java` | Individual healthcare provider (PCP, specialist) |
| `HealthRecord.java` | Patient's clinical history (encounters, conditions, medications) |
| `Exporter.java` | Base class for all export formats |
| `Config.java` | Loads and provides access to synthea.properties |

### Module System

**Generic Module Framework**: JSON-based state machines defining clinical pathways

**Module Location**: `src/main/resources/modules/`

**Examples**:
- `allergies.json`
- `asthma.json`
- `covid19/diagnose_blood_clot.json`
- `heart/chf.json` (Congestive Heart Failure)
- `metabolic_syndrome_disease.json`

**Module Structure**:
```json
{
  "name": "Module Name",
  "states": {
    "Initial": {
      "type": "Initial",
      "direct_transition": "Next_State"
    },
    "Encounter": {
      "type": "Encounter",
      "encounter_class": "ambulatory",
      "codes": [...]
    },
    "Condition": {
      "type": "ConditionOnset",
      "target_encounter": "Encounter",
      "codes": [...]
    }
  }
}
```

### Design Patterns

- **State Machine**: Disease progression modeled as state machines with transitions
- **Builder**: Person and Provider entities use builder patterns
- **Factory**: Module and Exporter factories for dynamic instantiation
- **Strategy**: Export strategy pattern (FHIR, C-CDA, CSV implementations)
- **Singleton**: Config class provides singleton access to properties

---

## Building and Running

### Build Commands

```bash
# Full build (compile + test + check)
./gradlew build

# Compile only (no tests)
./gradlew assemble

# Run tests + Checkstyle + JaCoCo
./gradlew check

# Clean build artifacts
./gradlew clean

# Build shadow JAR (all dependencies included)
./gradlew shadowJar
# Output: build/libs/synthea-with-dependencies.jar
```

### Running Synthea

#### Using Gradle

```bash
# Default run (10 patients, Massachusetts)
./gradlew run

# With arguments (requires -Params property)
./gradlew run -Params="['-p', '100', '-s', '12345']"
```

#### Using Shell Script (Recommended)

```bash
# Default
./run_synthea

# Specify state and city
./run_synthea Wisconsin Madison

# Specify population size
./run_synthea -p 1000

# With seed for reproducibility
./run_synthea -s 12345 -p 100 California "Los Angeles"

# Specify gender and age range
./run_synthea -g F -a 40-65 -p 50

# Override configuration properties
./run_synthea -p 10 --exporter.fhir.export=true --exporter.csv.export=true

# Custom output directory
./run_synthea --exporter.baseDirectory="./output_custom/" Texas
```

#### Using Shadow JAR

```bash
# After building shadow JAR
java -jar build/libs/synthea-with-dependencies.jar [arguments]

# Example
java -jar build/libs/synthea-with-dependencies.jar -p 100 -s 12345
```

### Command-Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `-s seed` | Random seed for reproducibility | `-s 12345` |
| `-cs clinicianSeed` | Separate seed for clinician generation | `-cs 67890` |
| `-p populationSize` | Number of patients to generate | `-p 1000` |
| `-r referenceDate` | Reference date (YYYYMMDD) | `-r 20250101` |
| `-g gender` | Gender filter (M/F) | `-g F` |
| `-a minAge-maxAge` | Age range | `-a 18-65` |
| `-o overflowPopulation` | Allow population overflow | `-o true` |
| `-c localConfigFilePath` | Custom config file | `-c ./custom.properties` |
| `-d localModulesDirPath` | Custom modules directory | `-d ./custom_modules/` |
| `-i initialPopulationSnapshotPath` | Load population snapshot | `-i ./snapshot.json` |
| `-u updatedPopulationSnapshotPath` | Save updated snapshot | `-u ./updated.json` |
| `-t updateTimePeriodInDays` | Simulation time period | `-t 365` |
| `-f fixedRecordPath` | Fixed record template | `-f ./template.json` |
| `-k keepMatchingPatientsPath` | Filter criteria file | `-k ./filter.json` |
| `--config*=value` | Override any property | `--exporter.fhir.export=true` |
| `state [city]` | Geographic location | `Massachusetts` or `Alaska Juneau` |

### Gradle Tasks Reference

| Task | Description |
|------|-------------|
| `./gradlew tasks` | List all available tasks |
| `./gradlew build` | Compile, test, check |
| `./gradlew run` | Run main application |
| `./gradlew test` | Run unit tests |
| `./gradlew check` | Tests + Checkstyle + JaCoCo |
| `./gradlew graphviz` | Generate module visualizations |
| `./gradlew concepts` | Generate concept list (with costs) |
| `./gradlew conceptswithoutcosts` | Generate concept list (no costs) |
| `./gradlew attributes` | Generate patient attributes list |
| `./gradlew overrides` | Generate module parameter overrides |
| `./gradlew physiology` | Test physiology simulation |
| `./gradlew flexporter` | Run FHIR transformation tool |
| `./gradlew rifMinimize` | Minimize RIF exports |
| `./gradlew rif2CCW` | Convert RIF to CCW format |
| `./gradlew rifBeneSplit` | Split RIF beneficiary exports |
| `./gradlew shadowJar` | Build JAR with dependencies |
| `./gradlew cleanOutput` | Delete all output files |
| `./gradlew javadoc` | Generate API documentation |
| `./gradlew jacocoTestReport` | Generate code coverage report |
| `./gradlew checkstyleMain` | Run Checkstyle on main code |
| `./gradlew checkstyleTest` | Run Checkstyle on test code |

---

## Testing

### Running Tests

```bash
# Run all tests
./gradlew test

# Run tests with verbose output
./gradlew test --info

# Run specific test class
./gradlew test --tests "org.mitre.synthea.engine.GeneratorTest"

# Run tests matching pattern
./gradlew test --tests "*FHIR*"

# Run single test method
./gradlew test --tests "org.mitre.synthea.engine.GeneratorTest.testGeneratePerson"
```

### Test Structure

- **Location**: `src/test/java/`
- **Test Framework**: JUnit 4
- **Mocking**: Mockito, PowerMock
- **Test Fixtures**: `src/test/resources/`
- **109 test files** covering all major components

### Test Categories

1. **Unit Tests**: Individual class/method tests
2. **Integration Tests**: Module execution, export generation
3. **Mock Tests**: External dependencies (HTTP, file system)

### Code Coverage

```bash
# Generate coverage report
./gradlew jacocoTestReport

# View report
open build/reports/jacoco/test/html/index.html
# or
xdg-open build/reports/jacoco/test/html/index.html
```

**Coverage Configuration**:
- Tool: JaCoCo 0.8.7
- Includes: `org.mitre.*` packages
- Output: XML (for CI) + HTML (for local viewing)

### Test Results

```bash
# View test results
open build/reports/tests/test/index.html
```

**Test Configuration**:
- Max heap: 6144m (6GB) - required for large test suites
- Exception format: Full stack traces

### Continuous Testing

```bash
# Run tests on file changes (requires entr or similar)
find src/test/java -name "*.java" | entr -c ./gradlew test
```

---

## Code Quality

### Checkstyle

**Configuration**: `config/checkstyle/` directory

**Version**: 8.4

#### Run Checkstyle

```bash
# Check main source code
./gradlew checkstyleMain

# Check test code
./gradlew checkstyleTest

# Both (included in 'check')
./gradlew check
```

#### View Results

```bash
# Main code results
cat build/reports/checkstyle/main.xml

# Test code results
cat build/reports/checkstyle/test.xml
```

### Code Style Guidelines

1. **Indentation**: 2 spaces (not tabs)
2. **Line Length**: 100 characters max
3. **Naming Conventions**:
   - Classes: `PascalCase`
   - Methods: `camelCase`
   - Constants: `UPPER_SNAKE_CASE`
   - Packages: `lowercase.dot.separated`
4. **Documentation**: Javadoc for public classes and methods
5. **Imports**: No wildcards, organized by groups

### Pre-Commit Checklist

Before committing code, ensure:

```bash
# Run all checks
./gradlew check

# Verify no Checkstyle violations
./gradlew checkstyleMain checkstyleTest

# Ensure tests pass
./gradlew test

# Optional: Check coverage hasn't decreased
./gradlew jacocoTestReport
```

---

## Configuration Management

### Primary Configuration File

**Location**: `src/main/resources/synthea.properties`

**Size**: 17+ KB, 600+ configuration options

### Configuration Hierarchy (Priority Order)

1. **Command-line arguments**: `--property.name=value`
2. **Custom config file**: `-c /path/to/custom.properties`
3. **Environment variables**: (limited support)
4. **Default properties**: `synthea.properties`

### Key Configuration Sections

#### 1. Exporter Settings

```properties
# Base output directory
exporter.baseDirectory = ./output/

# Enable/disable exporters
exporter.fhir.export = true
exporter.ccda.export = false
exporter.csv.export = false
exporter.cpcds.export = false

# FHIR versions
exporter.fhir_stu3.export = false
exporter.fhir_dstu2.export = false

# FHIR-specific settings
exporter.fhir.use_us_core_ig = true
exporter.fhir.us_core_version = 6.1.0
exporter.fhir.transaction_bundle = true
exporter.fhir.bulk_data = false

# CSV settings
exporter.csv.append_mode = false
exporter.csv.folder_per_run = false
exporter.csv.excluded_files = patient_expenses.csv
```

#### 2. Generator Settings

```properties
# Population generation
generate.default_population = 10
generate.only_alive_patients = false
generate.only_dead_patients = false

# Demographics
generate.demographics.default_file = geography/demographics.csv
generate.geography.zipcodes.default_file = geography/zipcodes.csv

# Date ranges
generate.birthweights.default_file = birthweights.csv
generate.birthweights.logging = false
generate.grow_up.ages_to_persist = 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18
```

#### 3. Clinical Settings

```properties
# Module-specific settings
lifecycle.death_by_natural_causes = true
lifecycle.death_by_loss_of_care = false

# Physiology
physiology.generators.enabled = true

# Quality of life
lifecycle.quality_of_life.year = 2017
```

#### 4. Provider/Payer Settings

```properties
# Provider lookup
generate.providers.hospitals.default_file = providers/hospitals.csv
generate.providers.primarycare.default_file = providers/primary_care_facilities.csv

# Payer configuration
generate.payers.insurance_companies.default_file = payers/insurance_companies.csv
```

### Overriding Configuration

#### Method 1: Command Line

```bash
./run_synthea -p 100 \
  --exporter.fhir.export=true \
  --exporter.csv.export=true \
  --exporter.baseDirectory="./custom_output/"
```

#### Method 2: Custom Properties File

```bash
# Create custom.properties
cat > custom.properties <<EOF
exporter.fhir.export = true
exporter.csv.export = true
generate.default_population = 100
EOF

# Run with custom config
./run_synthea -c custom.properties
```

#### Method 3: Module Overrides

```bash
# Generate override template
./gradlew overrides

# Edit override file
# Location: src/main/resources/module_overrides.json

# Run Synthea (automatically uses overrides if present)
./run_synthea
```

---

## Output Formats

### Output Directory Structure

```
output/
├── fhir/                    # FHIR R4 resources
│   ├── Patient.ndjson      # Bulk FHIR format
│   ├── Practitioner.ndjson
│   ├── Organization.ndjson
│   ├── Encounter.ndjson
│   └── ...
├── fhir_stu3/              # FHIR STU3 (if enabled)
├── fhir_dstu2/             # FHIR DSTU2 (if enabled)
├── ccda/                   # C-CDA documents (if enabled)
│   └── [patient_id].xml
├── csv/                    # CSV format (if enabled)
│   ├── patients.csv
│   ├── encounters.csv
│   ├── conditions.csv
│   ├── medications.csv
│   └── ...
└── cpcds/                  # CPCDS format (if enabled)
```

### 1. FHIR (Fast Healthcare Interoperability Resources)

**Default Version**: R4

**Format**: NDJSON (Newline Delimited JSON) for bulk data

**US Core Profile**: 6.1.0

**Resource Types**:
- `Patient` - Demographics, identifiers
- `Practitioner` - Healthcare providers
- `Organization` - Hospitals, clinics
- `Encounter` - Healthcare visits
- `Condition` - Diagnoses
- `Observation` - Vitals, labs
- `Procedure` - Surgeries, interventions
- `MedicationRequest` - Prescriptions
- `Immunization` - Vaccines
- `AllergyIntolerance` - Allergies
- `CarePlan` - Care plans
- `Claim` - Insurance claims

**Example Reading FHIR**:
```python
import json

# Load patients
with open('output/fhir/Patient.ndjson') as f:
    for line in f:
        patient = json.loads(line)
        print(f"Patient: {patient['id']}")
        print(f"Name: {patient['name'][0]['given'][0]} {patient['name'][0]['family']}")
```

### 2. C-CDA (Consolidated Clinical Document Architecture)

**Enable**: `exporter.ccda.export = true`

**Format**: XML documents per patient

**Template**: FreeMarker templates in `src/main/resources/templates/ccda/`

**Use Cases**: EHR interoperability, document exchange

### 3. CSV (Comma-Separated Values)

**Enable**: `exporter.csv.export = true`

**Files Generated**:
- `patients.csv` - Demographics
- `encounters.csv` - Healthcare visits
- `conditions.csv` - Diagnoses
- `medications.csv` - Prescriptions
- `procedures.csv` - Interventions
- `observations.csv` - Vitals, labs
- `immunizations.csv` - Vaccines
- `allergies.csv` - Allergies
- `careplans.csv` - Care plans
- `imaging_studies.csv` - Radiology
- `devices.csv` - Implants, devices
- `supplies.csv` - Supplies used
- `payer_transitions.csv` - Insurance history

**Data Dictionary**: See [CSV File Data Dictionary](https://github.com/synthetichealth/synthea/wiki/CSV-File-Data-Dictionary)

### 4. CPCDS (Claims and Patient-centered Data Standard)

**Enable**: `exporter.cpcds.export = true`

**Format**: CSV files for claims data

**Use Cases**: Payer analytics, claims processing

---

## Disease Modules

### Module Location

`src/main/resources/modules/`

### Available Modules (24+)

| Category | Modules |
|----------|---------|
| **Cardiovascular** | `chf.json`, `cabg.json`, `mi.json`, `stroke.json` |
| **Metabolic** | `diabetes.json`, `metabolic_syndrome_disease.json` |
| **Respiratory** | `asthma.json`, `copd.json`, `lung_cancer.json` |
| **Infectious Disease** | `covid19/`, `hiv.json`, `influenza.json` |
| **Mental Health** | `depression.json`, `anxiety.json`, `opioid_addiction.json` |
| **Lifecycle** | `pregnancy.json`, `contraceptives.json`, `childcare.json` |
| **Chronic Conditions** | `ckd.json`, `lupus.json`, `osteoarthritis.json` |
| **Core** | `encounter_module.json`, `wellness_encounters.json`, `death.json` |

### Module Visualization

```bash
# Generate all module graphs
./gradlew graphviz

# Output location
ls output/graphviz/
```

**Output**: PNG images of state machine diagrams

### Creating Custom Modules

1. **Create JSON file**: `src/main/resources/modules/custom_module.json`
2. **Define states**: Initial, Encounter, Condition, Procedure, etc.
3. **Set transitions**: Direct, Conditional, Distributed, Complex
4. **Test module**: Run Synthea and verify outputs

**Example Simple Module**:
```json
{
  "name": "Simple Checkup",
  "remarks": [
    "Simple annual checkup module"
  ],
  "states": {
    "Initial": {
      "type": "Initial",
      "direct_transition": "Annual_Checkup"
    },
    "Annual_Checkup": {
      "type": "Encounter",
      "encounter_class": "ambulatory",
      "codes": [
        {
          "system": "SNOMED-CT",
          "code": "185349003",
          "display": "Encounter for check up"
        }
      ],
      "direct_transition": "Terminal"
    },
    "Terminal": {
      "type": "Terminal"
    }
  }
}
```

### Module Documentation

- **Framework Guide**: [Generic Module Framework Wiki](https://github.com/synthetichealth/synthea/wiki/Generic-Module-Framework)
- **Builder Tool**: [Module Builder](https://synthetichealth.github.io/module-builder/)

---

## Debugging and Troubleshooting

### Common Issues

#### 1. Unsupported class file major version 69

**Symptom**:
```
Unsupported class file major version 69
```

**Cause**: Using Java 25 or newer

**Fix**:
```bash
# Switch to Java 21 or earlier
export JAVA_HOME=/Library/Java/JavaVirtualMachines/temurin-21.jdk/Contents/Home
java -version
./gradlew clean build
```

#### 2. Graphviz Errors

**Symptom**:
```
guru.nidi.graphviz.engine.GraphvizException: Cannot run program "dot"
```

**Cause**: Graphviz not installed

**Fix**:
```bash
# macOS
brew install graphviz

# Ubuntu/Debian
sudo apt install graphviz

# Verify
dot -V
```

**Alternative**: Synthea will use JavaScript engine (GraalVM JS) as fallback, but native Graphviz is faster

#### 3. Out of Memory Errors

**Symptom**:
```
java.lang.OutOfMemoryError: Java heap space
```

**Fix**:
```bash
# Set max heap size
export MAX_HEAP_SIZE=8192m

# Or run with explicit memory
./gradlew run -Dorg.gradle.jvmargs="-Xmx8g"
```

#### 4. Test Failures

**Symptom**: Tests fail intermittently

**Causes**:
- Randomness in generation (use seeds)
- Insufficient memory (tests need 6GB heap)
- Date-dependent tests

**Fix**:
```bash
# Ensure sufficient memory
./gradlew test -Dorg.gradle.jvmargs="-Xmx6g"

# Run with verbose output
./gradlew test --info

# Run specific failing test
./gradlew test --tests "FullClassName.testMethodName"
```

#### 5. Module Loading Errors

**Symptom**:
```
Error loading module: [module_name]
```

**Debug Steps**:
1. Validate JSON syntax (use online validator)
2. Check module file location: `src/main/resources/modules/`
3. Verify state transitions are valid
4. Check for circular dependencies

### Debugging Tips

#### Enable Verbose Logging

```bash
# Run with debug output
./gradlew run --debug

# Specific logger (requires log4j configuration)
# Edit src/main/resources/log4j2.xml
```

#### Inspect Generated Data

```bash
# View FHIR output (formatted)
cat output/fhir/Patient.ndjson | jq .

# Count resources
wc -l output/fhir/Patient.ndjson

# Check CSV headers
head -n 1 output/csv/patients.csv
```

#### Profile Memory Usage

```bash
# Run with memory profiling
java -Xmx4g -XX:+HeapDumpOnOutOfMemoryError \
  -XX:HeapDumpPath=./heap_dump.hprof \
  -jar build/libs/synthea-with-dependencies.jar -p 1000
```

#### Validate FHIR Output

```bash
# Use FHIR validator (requires Java FHIR validator)
java -jar validator_cli.jar output/fhir/Patient.ndjson -version 4.0
```

---

## CI/CD Pipeline

### GitHub Actions Workflows

**Location**: `.github/workflows/`

### 1. CI Build and Test (`ci-build-test.yml`)

**Trigger**: Push, Pull Request

**Jobs**:

1. **Java 17 Build**:
   - Ubuntu latest
   - Zulu OpenJDK 17
   - Compile only (`./gradlew assemble`)
   - Gradle cache enabled

2. **Java 11 Build and Test**:
   - Ubuntu latest
   - Zulu OpenJDK 11
   - Full build and tests (`./gradlew check`)
   - Upload code coverage to Codecov

**Badge**: ![Build Status](https://github.com/synthetichealth/synthea/workflows/.github/workflows/ci-build-test.yml/badge.svg?branch=master)

### 2. Deployment (`deploy.yml`)

**Trigger**: Push to master branch (or configured release branches)

**Jobs**: (Implementation varies by fork)
- Build shadow JAR
- Generate sample data
- Create GitHub release
- Deploy documentation to gh-pages

### Local CI Simulation

```bash
# Run same checks as CI
./gradlew clean build check

# Check Java 11 compatibility
export JAVA_HOME=/path/to/jdk-11
./gradlew clean assemble

# Check Java 17 compatibility
export JAVA_HOME=/path/to/jdk-17
./gradlew clean assemble
```

---

## Production Runs

### Large-Scale Data Generation

For generating 1000+ patients, use optimized configurations.

### Example: Production Run Directory

**Location**: `production_run_1000/`

**Contents**:
- `inputs/` - Custom geography, providers, payers
- `outputs/` - Generated FHIR and CSV data
- `scripts/` - Analysis scripts (attribution, reporting)
- `documentation/` - Results and reports
- `synthea_production.properties` - Custom configuration
- `run_production.py` - Orchestration script

### Running Production Generation

#### Method 1: Using Python Orchestration

```bash
cd production_run_1000/
python3 run_production.py
```

#### Method 2: Direct Synthea Invocation

```bash
# Use production properties
./run_synthea -c production_run_1000/synthea_production.properties \
  -p 1000 \
  -s 12345 \
  --exporter.baseDirectory="./production_run_1000/outputs/"
```

### Production Configuration Tips

1. **Enable Required Exporters Only**:
   ```properties
   exporter.fhir.export = true
   exporter.csv.export = true
   exporter.ccda.export = false  # Disable if not needed
   ```

2. **Use Bulk FHIR for Large Populations**:
   ```properties
   exporter.fhir.bulk_data = true
   exporter.pretty_print = false  # Reduces file size
   ```

3. **Set Appropriate Memory**:
   ```bash
   export MAX_HEAP_SIZE=16384m  # 16GB for 1000+ patients
   ```

4. **Use Fixed Seed for Reproducibility**:
   ```bash
   ./run_synthea -s 12345 -cs 67890 -p 1000
   ```

5. **Custom Demographics**:
   ```properties
   generate.demographics.default_file = custom_demographics.csv
   generate.geography.zipcodes.default_file = custom_zipcodes.csv
   ```

### Performance Benchmarks

| Population Size | Execution Time | Memory Usage | Output Size (FHIR) |
|-----------------|----------------|--------------|---------------------|
| 10 patients     | ~5 seconds     | 512MB        | ~2MB                |
| 100 patients    | ~10 seconds    | 1GB          | ~20MB               |
| 1,000 patients  | ~31 seconds    | 4GB          | ~200MB              |
| 10,000 patients | ~5 minutes     | 16GB         | ~2GB                |

---

## Git Workflow

### Branch Naming Conventions

- `main` or `master` - Production-ready code
- `develop` - Development integration branch
- `feature/feature-name` - New features
- `bugfix/issue-description` - Bug fixes
- `hotfix/critical-fix` - Emergency fixes
- `release/version-number` - Release preparation

### Commit Message Guidelines

**Format**:
```
<type>: <short summary>

<detailed description>

<footer: issue references>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Build process, dependencies

**Examples**:
```
feat: Add support for FHIR R5 export

Implement FHIR R5 exporter with US Core 7.0 profile support.
Includes new resource mappings and validation.

Closes #123
```

```
fix: Resolve memory leak in long-running simulations

Fixed issue where Person objects were not being garbage collected
after generation completed.

Fixes #456
```

### Pull Request Process

1. Create feature branch from `develop`
2. Implement changes
3. Run all checks: `./gradlew check`
4. Commit with clear messages
5. Push to remote
6. Create PR with description
7. Wait for CI to pass
8. Request review
9. Address feedback
10. Merge after approval

---

## Key Files and Directories

### Root Directory

| File/Directory | Purpose |
|----------------|---------|
| `build.gradle` | Gradle build configuration |
| `settings.gradle` | Gradle project settings |
| `gradlew`, `gradlew.bat` | Gradle wrapper scripts |
| `run_synthea` | Shell script to run Synthea |
| `README.md` | Project overview |
| `LICENSE` | Apache 2.0 license |
| `CODE_OF_CONDUCT.md` | Community guidelines |

### Source Code

| Directory | Contents |
|-----------|----------|
| `src/main/java/` | Java source code (`org.mitre.synthea`) |
| `src/main/resources/` | Configuration, modules, templates |
| `src/test/java/` | JUnit test classes |
| `src/test/resources/` | Test fixtures and data |

### Configuration

| File | Purpose |
|------|---------|
| `src/main/resources/synthea.properties` | Main configuration |
| `src/main/resources/version.txt` | Build version (generated) |

### Modules

| Directory | Contents |
|-----------|----------|
| `src/main/resources/modules/` | Disease module JSON files |
| `src/main/resources/modules/covid19/` | COVID-19 specific modules |
| `src/main/resources/modules/heart/` | Cardiovascular modules |

### Templates

| Directory | Contents |
|-----------|----------|
| `src/main/resources/templates/ccda/` | C-CDA FreeMarker templates |

### Healthcare Data Files

| Directory | Contents |
|-----------|----------|
| `src/main/resources/geography/` | Demographics, zipcodes |
| `src/main/resources/providers/` | Hospitals, clinics |
| `src/main/resources/payers/` | Insurance companies |

### Build Output

| Directory | Contents |
|-----------|----------|
| `build/` | Compiled classes, test results |
| `build/libs/` | JAR files |
| `build/reports/` | Test and coverage reports |
| `output/` | Generated patient data |

### Production Runs

| Directory | Contents |
|-----------|----------|
| `production_run_1000/` | Large-scale generation example |

---

## Common Workflows

### Workflow 1: Generate Custom Patient Population

**Goal**: Generate 100 patients in California with specific demographics

```bash
# 1. Create custom properties file
cat > custom_config.properties <<EOF
generate.default_population = 100
generate.only_alive_patients = true
exporter.fhir.export = true
exporter.csv.export = true
exporter.baseDirectory = ./output_california/
EOF

# 2. Run generation
./run_synthea -c custom_config.properties \
  -s 12345 \
  California "Los Angeles"

# 3. Verify output
ls output_california/fhir/
ls output_california/csv/

# 4. Count patients
wc -l output_california/fhir/Patient.ndjson
```

### Workflow 2: Add New Disease Module

**Goal**: Create a new clinical module

```bash
# 1. Create module file
cat > src/main/resources/modules/custom_condition.json <<'EOF'
{
  "name": "Custom Condition",
  "remarks": [],
  "states": {
    "Initial": {
      "type": "Initial",
      "direct_transition": "Checkup"
    },
    "Checkup": {
      "type": "Encounter",
      "encounter_class": "ambulatory",
      "codes": [
        {
          "system": "SNOMED-CT",
          "code": "185349003",
          "display": "Encounter for check up"
        }
      ],
      "direct_transition": "Diagnosis"
    },
    "Diagnosis": {
      "type": "ConditionOnset",
      "target_encounter": "Checkup",
      "codes": [
        {
          "system": "SNOMED-CT",
          "code": "XXXXXX",
          "display": "Custom Condition"
        }
      ],
      "direct_transition": "Terminal"
    },
    "Terminal": {
      "type": "Terminal"
    }
  }
}
EOF

# 2. Build project
./gradlew build

# 3. Test module
./run_synthea -p 10

# 4. Generate visualization
./gradlew graphviz
open output/graphviz/custom_condition.png

# 5. Verify output
cat output/fhir/Condition.ndjson | jq '. | select(.code.coding[0].code == "XXXXXX")'
```

### Workflow 3: Debug Failing Test

**Goal**: Fix a failing unit test

```bash
# 1. Run specific test with details
./gradlew test --tests "org.mitre.synthea.engine.GeneratorTest.testSpecificMethod" --info

# 2. View detailed results
cat build/reports/tests/test/classes/org.mitre.synthea.engine.GeneratorTest.html

# 3. Make code changes
# ... edit source files ...

# 4. Rerun test
./gradlew test --tests "org.mitre.synthea.engine.GeneratorTest.testSpecificMethod"

# 5. Run full test suite
./gradlew test

# 6. Check coverage
./gradlew jacocoTestReport
open build/reports/jacoco/test/html/index.html
```

### Workflow 4: Prepare Release Build

**Goal**: Build production-ready JAR

```bash
# 1. Clean previous builds
./gradlew clean

# 2. Run all checks
./gradlew check

# 3. Build shadow JAR
./gradlew shadowJar

# 4. Verify JAR
ls -lh build/libs/synthea-with-dependencies.jar

# 5. Test JAR
java -jar build/libs/synthea-with-dependencies.jar -p 10

# 6. Create checksum
sha256sum build/libs/synthea-with-dependencies.jar > build/libs/synthea-with-dependencies.jar.sha256

# 7. Tag release
git tag -a v3.4.1 -m "Release version 3.4.1"
git push origin v3.4.1
```

### Workflow 5: Analyze Generated Data

**Goal**: Analyze patient population characteristics

```bash
# 1. Generate population
./run_synthea -p 1000 -s 12345

# 2. Use Python for analysis
cat > analyze.py <<'EOF'
import json
import pandas as pd
from collections import Counter

# Load patients
patients = []
with open('output/fhir/Patient.ndjson') as f:
    for line in f:
        patients.append(json.loads(line))

# Analyze gender distribution
genders = [p.get('gender') for p in patients]
print("Gender Distribution:", Counter(genders))

# Analyze birth years
birth_years = [p.get('birthDate', '')[:4] for p in patients if 'birthDate' in p]
print("Birth Year Range:", min(birth_years), "-", max(birth_years))

# Use CSV for detailed analysis
df = pd.read_csv('output/csv/patients.csv')
print("\nAge Statistics:")
print(df['AGE'].describe())
EOF

python3 analyze.py

# 3. Generate custom report
./gradlew concepts
cat concepts.txt
```

---

## Performance Optimization

### Memory Management

#### Heap Size Configuration

```bash
# Default (usually 1GB)
./gradlew run

# Increase for large populations
export MAX_HEAP_SIZE=8192m
./gradlew run

# Or set in gradle.properties
echo "org.gradle.jvmargs=-Xmx8g -XX:MaxMetaspaceSize=512m" >> gradle.properties
```

#### Memory Requirements by Population Size

| Population | Recommended Heap | Minimum Heap |
|------------|------------------|--------------|
| < 100      | 1GB              | 512MB        |
| 100-500    | 2GB              | 1GB          |
| 500-1,000  | 4GB              | 2GB          |
| 1,000-5,000| 8GB              | 4GB          |
| 5,000+     | 16GB+            | 8GB          |

### Parallel Execution

Synthea generates patients sequentially by default. For parallel generation:

```bash
# Split into batches and run in parallel
./run_synthea -p 250 -s 1000 --exporter.baseDirectory="./output/batch1/" &
./run_synthea -p 250 -s 2000 --exporter.baseDirectory="./output/batch2/" &
./run_synthea -p 250 -s 3000 --exporter.baseDirectory="./output/batch3/" &
./run_synthea -p 250 -s 4000 --exporter.baseDirectory="./output/batch4/" &
wait

# Combine outputs
mkdir output_combined
cat output/batch*/fhir/Patient.ndjson > output_combined/Patient.ndjson
```

### Output Optimization

#### Reduce File Size

```properties
# Disable pretty printing
exporter.pretty_print = false

# Use bulk data format
exporter.fhir.bulk_data = true

# Limit exported resources
exporter.fhir.included_resources = Patient,Condition,Observation
```

#### Limit Historical Data

```properties
# Keep only last 5 years
exporter.years_of_history = 5

# Or keep all
exporter.years_of_history = 0
```

### Build Performance

#### Gradle Daemon

```bash
# Enable daemon (usually on by default)
echo "org.gradle.daemon=true" >> gradle.properties

# Set parallel builds
echo "org.gradle.parallel=true" >> gradle.properties

# Configure workers
echo "org.gradle.workers.max=4" >> gradle.properties
```

#### Incremental Builds

```bash
# Only rebuild changed files
./gradlew build

# Skip tests for faster builds
./gradlew build -x test

# Skip Checkstyle
./gradlew build -x checkstyleMain -x checkstyleTest
```

---

## Python Analysis Scripts

### Available Scripts

Located in repository root:

| Script | Purpose |
|--------|---------|
| `analyze_results.py` | Analyze generated patient data |
| `fix_*.py` | Data correction utilities |
| `production_run_1000/scripts/production_attribution.py` | PCP attribution logic |

### Using Analysis Scripts

#### Prerequisites

```bash
pip install pandas
```

#### Example: Analyze Results

```bash
# After generating data
python3 analyze_results.py

# Or for production run
cd production_run_1000/scripts/
python3 production_attribution.py
```

### Creating Custom Analysis Script

```python
#!/usr/bin/env python3
import json
import pandas as pd
from pathlib import Path

def analyze_fhir(output_dir):
    """Analyze FHIR output."""
    patients = []
    patient_file = Path(output_dir) / 'fhir' / 'Patient.ndjson'

    with open(patient_file) as f:
        for line in f:
            patients.append(json.loads(line))

    print(f"Total Patients: {len(patients)}")

    # Gender distribution
    genders = {}
    for p in patients:
        gender = p.get('gender', 'unknown')
        genders[gender] = genders.get(gender, 0) + 1

    print("Gender Distribution:", genders)

    # Age distribution (requires birth date)
    from datetime import datetime
    ages = []
    for p in patients:
        if 'birthDate' in p:
            birth_year = int(p['birthDate'][:4])
            age = 2025 - birth_year
            ages.append(age)

    print(f"Age Range: {min(ages)} - {max(ages)}")
    print(f"Average Age: {sum(ages) / len(ages):.1f}")

if __name__ == '__main__':
    analyze_fhir('./output')
```

---

## Important Notes for AI Agents

### Critical Do's and Don'ts

#### ✅ DO:

1. **Always use Java 11-21** (verify with `java -version` before building)
2. **Run `./gradlew check`** before committing code changes
3. **Use seeds** (`-s`) for reproducible generation
4. **Read existing tests** before writing new ones
5. **Follow Checkstyle rules** (config in `config/checkstyle/`)
6. **Test module changes** with small populations first
7. **Validate FHIR output** when modifying exporters
8. **Check memory settings** for large populations
9. **Use Gradle wrapper** (`./gradlew`) not system Gradle
10. **Consult synthea.properties** for all configuration options

#### ❌ DON'T:

1. **Don't use Java 22+** (causes compatibility issues)
2. **Don't modify `synthea.properties`** directly (use overrides)
3. **Don't commit generated output** (`output/` directory)
4. **Don't skip tests** when making code changes
5. **Don't hardcode file paths** (use Config class)
6. **Don't modify module JSON** without understanding state machines
7. **Don't assume default configurations** (always verify)
8. **Don't ignore Checkstyle warnings**
9. **Don't use system-specific paths** in code
10. **Don't generate large populations** without memory configuration

### Understanding the Codebase

1. **Start with**:
   - `App.java` - Entry point
   - `Generator.java` - Core generation logic
   - `Person.java` - Patient model
   - `Module.java` - State machine executor

2. **Key Design Decisions**:
   - State machine-based disease progression
   - Modular architecture for exporters
   - Configuration-driven demographics
   - Reproducible generation via seeds

3. **Extension Points**:
   - New exporters: Implement `Exporter` interface
   - New modules: Create JSON state machines
   - Custom logic: Extend Java module classes
   - Custom demographics: Replace CSV files

### Testing Strategy

1. **Unit Tests**: Test individual methods/classes
2. **Integration Tests**: Test module execution end-to-end
3. **Regression Tests**: Ensure outputs remain consistent
4. **Performance Tests**: Monitor memory and execution time

### Documentation Resources

- **Official Wiki**: https://github.com/synthetichealth/synthea/wiki
- **Module Framework**: https://github.com/synthetichealth/synthea/wiki/Generic-Module-Framework
- **FAQ**: https://github.com/synthetichealth/synthea/wiki/Frequently-Asked-Questions
- **CSV Data Dictionary**: https://github.com/synthetichealth/synthea/wiki/CSV-File-Data-Dictionary

### When to Ask for Human Review

- **Architecture Changes**: Modifying core engine classes
- **Module Logic**: Complex state machine modifications
- **Export Format Changes**: Altering FHIR/C-CDA structure
- **Performance Issues**: Significant memory/speed degradation
- **Breaking Changes**: API or configuration changes
- **Security Concerns**: Handling of sensitive data patterns

### Code Navigation Tips

```bash
# Find class definition
find src -name "ClassName.java"

# Find usage of method
grep -r "methodName" src/

# Find configuration key
grep -r "property.name" src/main/resources/

# Find test for class
find src/test -name "*ClassNameTest.java"

# Find module by name
find src/main/resources/modules -name "*keyword*.json"
```

---

## Summary Checklist for AI Agents

Before starting work:
- [ ] Verify Java version (11-21)
- [ ] Understand the task scope
- [ ] Read relevant existing code
- [ ] Check existing tests

During development:
- [ ] Follow code style guidelines
- [ ] Write/update tests
- [ ] Run `./gradlew check` frequently
- [ ] Test with small populations first

Before committing:
- [ ] Run `./gradlew check` (passes)
- [ ] Run `./gradlew test` (all pass)
- [ ] Run `./gradlew checkstyleMain checkstyleTest` (no violations)
- [ ] Test manual scenarios if applicable
- [ ] Write clear commit message

---

## Version Information

- **Synthea Version**: 3.4.1-SNAPSHOT
- **Gradle**: 8.14+
- **Java**: 11+ (recommended: 21)
- **HAPI FHIR**: 6.1.0
- **JUnit**: 4.13.2
- **Last Updated**: 2025-11-20

---

## Contact and Support

- **GitHub**: https://github.com/synthetichealth/synthea
- **Issues**: https://github.com/synthetichealth/synthea/issues
- **Wiki**: https://github.com/synthetichealth/synthea/wiki
- **License**: Apache 2.0

---

*This documentation is maintained for AI coding agents working on the synthetic-data-generator-data-voyager repository. For human-readable documentation, see README.md and the project wiki.*
