# AGENTS.md - Synthetic Data Generator Data Voyager
*AI Agent Development Guide for Synthea-based Healthcare Data Simulation*

## 🎯 Project Mission
Generate high-fidelity synthetic patient populations for healthcare analytics, quality measurement, and clinical decision support systems. This project extends Synthea's capabilities for enterprise healthcare systems with focus on temporal analysis, care attribution, and quality metric calculation.

## 📋 Quick Start Checklist
```bash
# Environment Setup (CRITICAL - Use Java 21 ONLY)
export JAVA_HOME=/Library/Java/JavaVirtualMachines/temurin-21.jdk/Contents/Home
java -version  # Must show Java 21

# Build & Verify
./gradlew clean build
./gradlew test
./gradlew graphviz  # Requires Graphviz installed

# Run Standard Generation
./gradlew run -Pargs="-p 1000 Wisconsin"
```

## 🏗️ Architecture Overview

### Core Components
```
synthetic-data-generator-data-voyager/
├── src/
│   ├── main/java/org/mitre/synthea/
│   │   ├── engine/           # Core simulation engine
│   │   ├── modules/          # Disease & care modules
│   │   ├── world/            # Population & geography
│   │   ├── export/           # FHIR/HL7/CSV exporters
│   │   └── helpers/          # Utility functions
│   └── test/java/            # Unit & integration tests
├── src/main/resources/
│   ├── modules/              # JSON disease modules
│   ├── templates/            # Export templates
│   └── geography/            # Geographic data
├── production_run_1000/      # Production configurations
│   ├── 00_GLOBAL_CONFIG/     # Master configuration
│   ├── 01_SCRIPTS/           # Automation scripts
│   ├── 02_INPUTS/            # Input CSVs
│   └── 03_OUTPUTS_COMPLETE/  # Generated data
└── build.gradle              # Build configuration
```

## 🔧 Development Environment

### Java Configuration (CRITICAL)
```bash
# ⚠️ MANDATORY: Java 21 (NOT Java 25+)
# Java 25+ causes: "Unsupported class file major version 69"

# macOS/Linux
export JAVA_HOME=/Library/Java/JavaVirtualMachines/temurin-21.jdk/Contents/Home
export PATH=$JAVA_HOME/bin:$PATH

# Windows
set JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-21.0.1.12-hotspot
set PATH=%JAVA_HOME%\bin;%PATH%

# Verify
java -version  # Should show: openjdk version "21.x.x"
```

### Dependencies & Tools
```bash
# Required System Dependencies
brew install graphviz         # macOS
apt-get install graphviz      # Ubuntu
choco install graphviz        # Windows

# Python Environment (for analysis scripts)
python3 -m venv venv
source venv/bin/activate     # Unix/macOS
venv\Scripts\activate         # Windows
pip install pandas numpy matplotlib seaborn

# IDE Setup
# IntelliJ IDEA: File > Project Structure > Project SDK > Java 21
# VS Code: Install Extension Pack for Java, configure java.home
```

## 🏃 Build & Execution Commands

### Core Operations
```bash
# Clean Build
./gradlew clean build

# Run with Custom Population
./gradlew run -Pargs="-p 10000 -s 42 Wisconsin"
# -p: population size
# -s: random seed (reproducibility)

# Generate with Specific Configuration
./gradlew run -Pargs="-c production_run_1000/00_GLOBAL_CONFIG/wisconsin_baseline.properties"

# Export Formats
./gradlew run -Pargs="--exporter.fhir.export=true --exporter.csv.export=true -p 100"

# Module Visualization
./gradlew graphviz
# Output: output/graphviz/*.png
```

### Testing & Quality
```bash
# Full Test Suite
./gradlew test

# Specific Test Class
./gradlew test --tests "org.mitre.synthea.engine.GeneratorTest"

# Code Coverage
./gradlew jacocoTestReport
# Report: build/reports/jacoco/test/html/index.html

# Style Checks
./gradlew checkstyleMain checkstyleTest

# All Quality Checks
./gradlew check
```

## 📊 Production Configuration

### Wisconsin Baseline v3.0 Structure
```properties
# wisconsin_baseline.properties
# Population Configuration
generate.default_population = 10000
generate.demographics.default_file = ./02_INPUTS/demographics__wi_8counties__synthea_ready__y2022__complete__v3_0__prod.csv

# Geography
generate.geography.zipcodes.default_file = ./02_INPUTS/zipcodes__wi__zcta__y2020__real__n140__v3_0__prod.csv

# Providers
generate.providers.hospitals.default_file = ./02_INPUTS/hospitals__andor__n3__v3_0__prod.csv
generate.providers.primarycare.default_file = ./02_INPUTS/providers__wi__template__real__v3_0.csv

# Payers
generate.payers.insurance_plans.default_file = ./02_INPUTS/insurance_plans__andor__v3_0__prod.csv
generate.payers.default_file = ./02_INPUTS/payers__andor__n8__v3_0__prod.csv

# Export Settings
exporter.fhir.export = true
exporter.fhir.use_us_core_ig = true
exporter.fhir.us_core_version = 6.1.0
exporter.csv.export = true
exporter.csv.append_mode = false

# Reproducibility
seed = 12345
```

## 🔬 Temporal Analysis Framework

### Patient Timeline Extraction
```python
# analyze_temporal.py - Extract longitudinal patient events
import pandas as pd
from datetime import datetime

def extract_patient_timeline(patient_id, data_path):
    """
    Extract comprehensive temporal sequence for patient analysis
    Following Dr. Smith's first-principles approach
    """
    
    # Load all relevant resource types
    resources = ['encounters', 'conditions', 'procedures', 
                 'observations', 'medications', 'payer_transitions']
    
    timeline = []
    
    for resource in resources:
        df = pd.read_csv(f"{data_path}/{resource}.csv")
        
        # Filter for specific patient
        patient_data = df[df['PATIENT'] == patient_id]
        
        # Extract temporal markers
        for _, row in patient_data.iterrows():
            event_date = row.get('START') or row.get('DATE')
            if pd.notna(event_date):
                timeline.append({
                    'date': pd.to_datetime(event_date),
                    'resource_type': resource,
                    'description': row.get('DESCRIPTION', ''),
                    'value': row.get('VALUE', ''),
                    'code': row.get('CODE', '')
                })
    
    # Sort chronologically
    timeline_df = pd.DataFrame(timeline)
    timeline_df.sort_values('date', inplace=True)
    
    return timeline_df
```

### Care Gap Detection
```python
def identify_care_gaps(timeline_df):
    """
    Identify gaps in care continuity
    Based on CMS quality measures
    """
    gaps = []
    
    # Group encounters by year
    encounters = timeline_df[timeline_df['resource_type'] == 'encounters']
    encounters['year'] = pd.to_datetime(encounters['date']).dt.year
    
    # Check for annual wellness visits (AWV)
    for year in encounters['year'].unique():
        year_encounters = encounters[encounters['year'] == year]
        awv_present = year_encounters['description'].str.contains('wellness|annual', case=False).any()
        
        if not awv_present:
            gaps.append({
                'type': 'Missing AWV',
                'year': year,
                'impact': 'Preventive care gap'
            })
    
    # Check for HbA1c monitoring (diabetes patients)
    if 'diabetes' in timeline_df['description'].str.lower().values:
        hba1c_tests = timeline_df[
            timeline_df['description'].str.contains('A1c|HbA1c', case=False, na=False)
        ]
        
        # Should have at least 2 per year
        for year in encounters['year'].unique():
            year_tests = hba1c_tests[pd.to_datetime(hba1c_tests['date']).dt.year == year]
            if len(year_tests) < 2:
                gaps.append({
                    'type': 'Insufficient HbA1c monitoring',
                    'year': year,
                    'tests_found': len(year_tests),
                    'tests_required': 2
                })
    
    return pd.DataFrame(gaps)
```

## 🏥 Attribution Logic

### Primary Care Provider Assignment
```java
// PCPAttributor.java
public class PCPAttributor {
    
    /**
     * Attribute patient to PCP using plurality logic
     * Per Dr. Smith's first-principles approach
     */
    public Provider attributePCP(Person patient, List<Encounter> encounters) {
        Map<Provider, Integer> providerCounts = new HashMap<>();
        Map<Provider, LocalDateTime> lastVisit = new HashMap<>();
        
        // Count qualifying encounters per provider
        for (Encounter enc : encounters) {
            if (isQualifyingEncounter(enc)) {
                Provider provider = enc.provider;
                providerCounts.merge(provider, 1, Integer::sum);
                lastVisit.merge(provider, enc.start, 
                    (old, new) -> new.isAfter(old) ? new : old);
            }
        }
        
        // Apply plurality logic with recency tiebreaker
        return providerCounts.entrySet().stream()
            .max(Map.Entry.<Provider, Integer>comparingByValue()
                .thenComparing(e -> lastVisit.get(e.getKey())))
            .map(Map.Entry::getKey)
            .orElse(null);
    }
    
    private boolean isQualifyingEncounter(Encounter enc) {
        // Primary care encounter types
        return enc.type.equals("ambulatory") || 
               enc.type.equals("wellness") ||
               enc.type.equals("urgentcare");
    }
}
```

## 📈 Quality Measure Calculation

### eCQM Implementation
```java
// QualityMeasureEngine.java
public class QualityMeasureEngine {
    
    /**
     * Calculate CMS122 - Diabetes HbA1c Poor Control
     */
    public MeasureResult calculateCMS122(List<Person> population) {
        int eligible = 0;
        int numerator = 0;
        
        for (Person patient : population) {
            // Check eligibility
            if (hasDiabetes(patient) && age(patient) >= 18 && age(patient) <= 75) {
                eligible++;
                
                // Check most recent HbA1c
                Observation lastA1c = getMostRecentHbA1c(patient);
                if (lastA1c != null && lastA1c.value > 9.0) {
                    numerator++;  // Poor control
                }
            }
        }
        
        return new MeasureResult("CMS122", eligible, numerator);
    }
}
```

## 🐛 Debugging & Troubleshooting

### Common Issues & Solutions

#### Issue: "Unsupported class file major version 69"
```bash
# CAUSE: Using Java 25+ instead of Java 21
# FIX:
java -version  # Check current version
sdk use java 21.0.1-tem  # If using SDKMAN
# OR manually set JAVA_HOME to Java 21 installation
```

#### Issue: Graphviz Generation Fails
```bash
# CAUSE: Missing Graphviz or PATH issue
# FIX:
dot -V  # Should show version
which dot  # Should show path
# If missing:
brew install graphviz  # macOS
apt-get install graphviz  # Linux
```

#### Issue: Out of Memory During Large Generation
```bash
# CAUSE: Insufficient heap space
# FIX: Increase JVM memory
export GRADLE_OPTS="-Xmx8g -XX:MaxPermSize=2g"
./gradlew run -Pargs="-p 100000"
```

#### Issue: Module Not Found
```bash
# CAUSE: Module JSON syntax error
# FIX: Validate JSON
python -m json.tool src/main/resources/modules/my_module.json
# Check for missing commas, brackets
```

## 📝 Code Style Guidelines

### Java Standards
```java
/**
 * Class-level JavaDoc required
 * @author Your Name
 * @since 2025-11-21
 */
public class PatientGenerator {
    
    // Constants in UPPER_CASE
    private static final int MAX_ATTEMPTS = 3;
    
    // Member variables with meaningful names
    private final Random random;
    private List<Person> population;
    
    /**
     * Method JavaDoc for public methods
     * @param seed Random seed for reproducibility
     * @return Generated patient population
     */
    public List<Person> generate(long seed) {
        // Single responsibility per method
        initializeRandom(seed);
        createPopulation();
        assignProviders();
        return population;
    }
}
```

### Python Analysis Scripts
```python
"""
Module docstring required
Author: Your Name
Date: 2025-11-21
"""

def analyze_population(data_path: str) -> pd.DataFrame:
    """
    Analyze synthetic population characteristics.
    
    Args:
        data_path: Path to CSV output directory
        
    Returns:
        DataFrame with population statistics
    """
    # Use type hints
    # Follow PEP 8
    # Document complex logic
    pass
```

## 🚀 Performance Optimization

### Large-Scale Generation
```bash
# Parallel generation for large populations
./gradlew run -Pargs="-p 100000 --generate.thread_pool_size=8"

# Batch processing
for i in {1..10}; do
    ./gradlew run -Pargs="-p 10000 -s $i" &
done
wait

# Memory-efficient export
./gradlew run -Pargs="--exporter.csv.folder_per_run=true"
```

### Profiling
```bash
# Enable JVM profiling
export JAVA_OPTS="-XX:+FlightRecorder -XX:StartFlightRecording=filename=recording.jfr"
./gradlew run

# Analyze with JDK Mission Control
jmc recording.jfr
```

## 📚 Additional Resources

- [Synthea Wiki](https://github.com/synthetichealth/synthea/wiki)
- [FHIR R4 Specification](https://hl7.org/fhir/R4/)
- [US Core 6.1.0 IG](https://hl7.org/fhir/us/core/STU6.1/)
- [CMS eCQM Specifications](https://ecqi.healthit.gov/ecqms)
- [Project Documentation](./docs/)

## 🤝 Contribution Guidelines

1. **Branch Strategy**: Feature branches from `develop`
2. **Commit Messages**: Conventional commits (feat:, fix:, docs:)
3. **Testing**: Minimum 80% coverage for new code
4. **Review**: PR requires approval from code owner
5. **Documentation**: Update relevant docs with changes

## 📞 Support & Contact

- **Technical Issues**: Create GitHub issue with reproduction steps
- **Architecture Questions**: Refer to design docs in `/docs/architecture/`
- **Data Questions**: Check `/docs/data-dictionary/`

---
*Last Updated: November 21, 2025*
*Version: 3.0.0*
*Maintainer: Data Voyager Team*
