# AGENTS.md

This file provides context and instructions for AI coding agents working on the `synthetic-data-generator-data-voyager` repository.

## Project Overview
This project is a synthetic patient population simulator (Synthea). It generates realistic (but synthetic) patient data in various formats (FHIR, C-CDA, CSV, etc.). It is a Java-based project managed by Gradle.

## Development Environment
-   **Java Version**: **CRITICAL**: Use **Java 21**.
    -   Do **NOT** use Java 25 (or newer) as it causes `Unsupported class file major version 69` errors with the current Gradle/Groovy setup.
    -   Set `JAVA_HOME` explicitly if needed: `export JAVA_HOME=/Library/Java/JavaVirtualMachines/temurin-21.jdk/Contents/Home` (or appropriate path).
-   **Build System**: Gradle (use the provided `./gradlew` wrapper).
-   **Dependencies**:
    -   **Graphviz**: Required for generating disease module graphs. Ensure `dot` is in the PATH.

## Building and Running
-   **Build Project**: `./gradlew build`
-   **Run Application**: `./gradlew run`
    -   Arguments can be passed via properties if configured, but standard usage is often headless or via specific run configurations.
-   **Generate Module Graphs**: `./gradlew graphviz`
    -   Outputs to `output/graphviz/`.
    -   Requires Graphviz installed.

## Testing Instructions
-   **Run All Tests**: `./gradlew test`
-   **Run Full Checks (Tests + Style)**: `./gradlew check`
    -   This runs unit tests, Checkstyle, and JaCoCo code coverage.
-   **Code Coverage**:
    -   Reports are generated at `build/reports/jacoco/test/html/index.html`.
    -   Run `./gradlew jacocoTestReport` to generate them manually if needed.
-   **Test Results**:
    -   HTML reports: `build/reports/tests/test/index.html`.

## Code Style & Quality
-   **Checkstyle**: The project uses Checkstyle.
    -   Config location: `config/checkstyle/`.
    -   Run checks: `./gradlew checkstyleMain` and `./gradlew checkstyleTest`.
-   **Linting**: Ensure code passes `gradle check` before committing.

## Key Directories
-   `src/main/java`: Main Java source code.
-   `src/test/java`: Unit tests.
-   `build.gradle`: Main build configuration.
-   `production_run_1000/`: Directory containing artifacts from a large-scale production run (inputs, scripts, outputs).
-   `output/`: Default output directory for generated data.

## Common Issues & Fixes
-   **"Unsupported class file major version 69"**:
    -   **Cause**: Running with Java 25.
    -   **Fix**: Switch to Java 21.
-   **Graphviz errors**:
    -   **Cause**: Missing Graphviz installation or incompatible `graphviz-java` library with very new Java versions.
    -   **Fix**: Ensure Graphviz is installed (`dot -V`) and use Java 21.

## Python Scripts
There are several Python scripts in the root for analysis and fixes (e.g., `analyze_results.py`, `fix_*.py`).
-   Run these with `python3 <script_name>`.
-   Ensure required packages (pandas, etc.) are installed.
