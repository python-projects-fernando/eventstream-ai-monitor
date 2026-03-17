# Benchmark Summary: Hexagonal Architecture (Version 1 - Unit Tests Only)

## Overview

This document summarizes the results of the initial benchmark for the Hexagonal Architecture experiment. The benchmark focuses on static code metrics and code coverage achieved by unit tests only. It serves as a baseline for comparison with other architectural styles.

## Results

### 1. Code Coverage (Dynamic Metric - Requires Test Execution)

*   **Tool:** `pytest-cov`
*   **Command:** `pytest --cov=src --cov-report=term-missing tests/`
*   **Overall Coverage:** **67%** (145 statements covered out of 216 total, 71 missing).
*   **Key Observations:**
    *   The `main.py` file has 0% coverage (33/33 statements missed). This is expected as it likely contains the application startup logic not covered by unit tests.
    *   The `postgresql_event_repository.py` has low coverage at 46% (21/46 statements missed), indicating areas for improvement in repository tests.
    *   Core domain entities (`event.py`) and use cases (`process_event_use_case.py`) show higher coverage (87% and 100% respectively).
    *   The API controller (`event_controller.py`) shows moderate coverage at 78% (4/18 statements missed).

### 2. Cyclomatic Complexity (Static Metric)

*   **Tool:** `radon`
*   **Command:** `radon cc src/ -s --total-average`
*   **Average Complexity:** **A (1.52)** across 33 analyzed blocks (functions, methods, classes).
*   **Key Observations:**
    *   The average complexity is low, indicating relatively simple and well-structured code.
    *   The most complex function is `Event.__post_init__` in `event.py` with a complexity of **5**. The rest of the blocks have complexities of **3 or lower**.
    *   All blocks are rated as 'A' (very low complexity).

### 3. Maintainability Index (Static Metric)

*   **Tool:** `radon`
*   **Command:** `radon mi src/ -s`
*   **Key Observations:**
    *   The majority of files score very high ('A' grade, 100. good maintainability.
    *   Notable exceptions:
        *   `postgresql_event_repository.py`: Score of **A (81.41)**. Still good, but lower than others.
        *   `event.py`: Score of **A (81.89)**. Still good, but lower than others.
        *   `main.py`: Score of **A (61.86)**. Lower due to complexity or lack of test coverage for initialization logic.

### 4. Linting (Static Metric)

*   **Tool:** `ruff`
*   **Command:** `ruff check src/`
*   **Result:** **All checks passed!**
*   **Key Observations:**
    *   The codebase adheres well to the linting rules configured for Ruff.

### 5. Type Checking (Static Metric)

*   **Tool:** `mypy`
*   **Command:** `MYPYPATH=src mypy --explicit-package-bases src/`
*   **Result:** **Found 10 errors in 3 files.**
*   **Key Observations:**
    *   There are type mismatches between SQLAlchemy `Column` types and the expected types for the `Event` entity in `postgresql_event_repository.py`.
    *   There's an issue with the from SQLAlchemy in `event_model.py` regarding type aliases.
    *   There's an incompatibility between `async_sessionmaker` and `sessionmaker` types when instantiating the repository`.
    *   These errors indicate potential runtime issues if not addressed.

### 6. Dependency Tree (Static Metric - External)

*   **Tool:** `pipdeptree`
*   **Command:** `pipdeptree`
*   **Key Observations:**
    *   The dependency tree shows the installed packages and their hierarchical relationships. The project uses common libraries like `fastapi`, `sqlalchemy`, `pydantic`, `pytest`, etc.

### 7. Dependency Graph (Static Metric - Internal Structure)

*   **Tool:** `pydeps`
*   **Command:** `MYPYPATH=src pydeps src/ --show-dot --max-bacon 2`
*   **Result:** Generated DOT code for the dependency graph (see `08-v1-dependency-graph-dot.txt`).
*   **Key Observations:**
    *   The graph visually confirms the separation of concerns typical of Hexagonal Architecture.
    *   `src.core.domain` and `src.core.application` are at the center, with dependencies flowing outward towards `src.adapters`.
    *   `src.adapters.input.api` depends on core application ports and use cases.
    *   `src.adapters.output.database` depends on core application ports and domain entities.
    *   External libraries like `fastapi`, `pydantic`, `sqlalchemy` are correctly depended upon by the relevant adapter layers.

### 8. (Optional) Test Durations (Dynamic Metric)

*   **Tool:** `pytest` (with `--durations` flag)
*   **Command:** `pytest tests/ --durations=10`
*   **Key Observations:**
    *   The tests execute very quickly (overall duration ~0.09s to 0.10s).
    *   The slowest reported durations are related to test setup (`0.02s` to `0.03s`) rather than the actual test logic (`call` time is much lower, e.g., `0.01s`).

## Conclusion (Version 1)

*   The unit tests provide a solid foundation, achieving **67% overall code coverage**. Coverage is strong in core business logic but lower in infrastructure layers like the repository and main application entry point.
*   The code exhibits **low cyclomatic complexity** and **high maintainability scores**, suggesting good structural health.
*   **Linting** passes without issues.
*   **Type checking** reveals several critical errors related to data mapping and dependency injection, requiring immediate attention.
*   The **dependency graph** confirms the intended architectural structure of the Hexagonal Architecture.
*   This baseline provides metrics for comparison with other architectural implementations (e.g., Clean, Onion) in future benchmarking phases (Version 2, incorporating integration/E2E tests and performance analysis).