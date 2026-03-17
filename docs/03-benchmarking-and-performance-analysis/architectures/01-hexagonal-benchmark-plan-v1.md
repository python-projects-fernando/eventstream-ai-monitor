# Benchmark Plan: Hexagonal Architecture (Version 1 - Unit Tests)

## Objective

Establish a baseline for comparing the Hexagonal Architecture against other architectures (e.g., Clean, Onion) implemented in the EventStream AI Monitor project. This initial benchmark focuses on static code metrics and code coverage achieved by unit tests.

## Scope

This plan covers the analysis of the `hexagonal` architecture experiment located at `backend/experiments/architectures/hexagonal/`. It evaluates the source code under `src/` and utilizes the unit tests written under `tests/`.

## Metrics to be Collected

### 1. Code Coverage (Dynamic Metric - Requires Test Execution)

*   **Tool:** `pytest-cov`
*   **Purpose:** Measure the percentage of lines, branches, and statements in the source code executed by the unit tests.
*   **Command:** `pytest --cov=src --cov-report=term-missing`
*   **Expected Output:** Coverage percentage, detailed report showing missed lines.

### 2. Cyclomatic Complexity (Static Metric)

*   **Tool:** `radon`
*   **Purpose:** Assess the complexity of individual functions and methods, indicating potential difficulty in testing and maintenance.
*   **Command:** `radon cc src/ -s --total-average`
*   **Expected Output:** Average and total cyclomatic complexity scores per function/method/file/module.

### 3. Maintainability Index (Static Metric)

*   **Tool:** `radon`
*   **Purpose:** Evaluate how easy the code is to maintain, considering factors like complexity, size, and structure.
*   **Command:** `radon mi src/ -s`
*   **Expected Output:** Maintainability index score (higher is better) per file/module.

### 4. Code Quality and Style (Static Metric)

*   **Tools:** `ruff` (fast, modern) or `pylint` (detailed)
*   **Purpose:** Identify potential bugs, code smells, style inconsistencies (like PEP 8 violations), and adherence to best practices.
*   **Commands:**
    *   `ruff check src/`
    *   `pylint src/` (Optional, can be slower)
*   **Expected Output:** List of issues categorized by severity (error, warning, convention).

### 5. Static Type Checking (Static Metric)

*   **Tool:** `mypy`
*   **Purpose:** Verify compliance with type hints and detect potential type-related errors.
*   **Command:** `mypy src/`
*   **Expected Output:** List of type errors or confirmation of successful type-checking.

### 6. Dependency Analysis (Structural Metric)

*   **Tools:**
    *   `pipdeptree`: Show the dependency tree of installed Python packages for the project.
    *   `pydeps`: Generate a visual graph of dependencies between internal Python modules.
*   **Purpose (pipdeptree):** Understand the project's external dependencies.
*   **Purpose (pydeps):** Analyze coupling between internal modules (e.g., `core`, `adapters`).
*   **Commands:**
    *   `pipdeptree`
    *   `pydeps src/ --show --max-bacon 2` (Generates a visual output, adjust as needed for saving)
*   **Expected Output (pipdeptree):** Hierarchical list of package dependencies.
*   **Expected Output (pydeps):** Visual representation (e.g., SVG/PNG) of module relationships.

### 7. (Optional) Basic Runtime Performance Indicators

*   **Tool:** `pytest`
*   **Purpose:** Get a rough idea of test execution times, which can be a proxy for the performance of the tested logic (though not definitive for overall application performance).
*   **Command:** `pytest tests/ --durations=10`
*   **Expected Output:** List of the 10 slowest running tests.

## Execution Steps

1.  **Ensure Environment:**
    *   Navigate to the architecture directory: `cd backend/experiments/architectures/hexagonal/`
    *   Ensure the virtual environment with development dependencies (`requirements-dev.txt`) is active.
    *   Ensure `PYTHONPATH` includes `src/` (e.g., using the `run_tests.bat` strategy or setting it manually for the commands below).
2.  **Run Tools Sequentially:**
    *   Execute `pytest tests/` to confirm all unit tests pass.
    *   Execute `pytest --cov=src --cov-report=term-missing` to get coverage.
    *   Execute `radon cc src/ -s --total-average` for complexity.
    *   Execute `radon mi src/ -s` for maintainability.
    *   Execute `ruff check src/` for linting.
    *   Execute `mypy src/` for type checking.
    *   Execute `pipdeptree` for package dependencies.
    *   (Optional) Execute `pydeps src/ --show --max-bacon 2` for visual module dependencies.
    *   (Optional) Execute `pytest tests/ --durations=10` for slowest tests.
3.  **Record Results:**
    *   Capture the output of each command.
    *   Note key metrics (e.g., overall coverage %, average complexity, number of linting errors).
    *   Save command outputs to individual text/log files or summarize in a spreadsheet for comparison with other architectures.

## Notes

*   This is Version 1 of the benchmark plan, focusing on static code metrics (e.g., complexity, maintainability, dependency structure) and dynamic code coverage achieved by the current unit tests. These metrics provide a baseline for structural and testability aspects of the architecture.
*   A subsequent benchmark phase will incorporate **dynamic/runtime performance metrics**. This involves executing the application (or significant parts of it) under simulated load conditions. Dynamic tests measure how the system behaves during execution, including metrics like:
    *   **Response Time:** Average, median, and percentile (e.g., p95, p99) latency for API requests.
    *   **Throughput:** Number of requests per second (RPS/QPS) the system can handle.
    *   **Resource Utilization:** CPU, memory, and I/O consumption under load.
    *   **Stress Testing:** Identifying breaking points or degradation thresholds.
    *   These metrics will be gathered primarily using tools like `locust`, which will perform load testing against the integrated components (e.g., API endpoints connected to the database). This complements the static analysis by evaluating the architecture's performance characteristics under realistic usage scenarios.