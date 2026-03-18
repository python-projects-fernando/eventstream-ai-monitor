@echo off
setlocal enabledelayedexpansion

REM Define the base directory (where this .bat is located)
set BASE_DIR=%~dp0

echo [START] Static Benchmark Suite v1 - Hexagonal Architecture
echo.

REM ==============================================================================
REM STEP 1: RUN UNIT TESTS
REM ==============================================================================
echo [1/9] Running unit tests...
call run_unit_tests.bat

if !errorlevel! neq 0 (
    echo.
    echo FATAL ERROR: Unit tests failed. Stopping benchmark.
    pause
    exit /b !errorlevel!
)

echo Unit tests passed. Proceeding to static analysis...
echo.

REM ==============================================================================
REM STEP 2: CODE COVERAGE (pytest-cov) - Simplified, NO IF CHECK
REM ==============================================================================
echo [2/9] Running Code Coverage Analysis...

REM Ensure you are in the correct directory (the directory containing src/, tests/, and pytest.ini/)
REM cd /d "%BASE_DIR%" (Should already be there from script start)

REM Execute pytest with coverage, relying on pytest.ini for PYTHONPATH
REM The 'src' directory should be added to sys.path via pytest.ini
REM DO NOT attempt to check %errorlevel% or !errorlevel! here.
echo Executing pytest for coverage...
python -m pytest --cov=src --cov-report=term-missing > "01-v1-code-coverage.txt" 2>&1
echo Command finished. Output saved to 01-v1-code-coverage.txt.
echo.

REM ==============================================================================
REM STEP 3: CYCLOMATIC COMPLEXITY (radon cc) - Simplified, NO IF CHECK
REM ==============================================================================
echo [3/9] Running Cyclomatic Complexity Analysis...

REM Ensure you are in the correct directory (should already be there from STEP 2)
REM cd /d "%BASE_DIR%" (Uncomment if needed, but likely redundant here)

REM Execute radon cc on the src directory and save output to file
REM DO NOT attempt to check %errorlevel% or !errorlevel! here.
echo Executing radon cc for complexity...
python -m radon cc src\ -s --total-average > "02-v1-complexity-cc.txt" 2>&1
echo Command finished. Output saved to 02-v1-complexity-cc.txt.
echo.

REM ==============================================================================
REM STEP 4: MAINTAINABILITY INDEX (radon mi) - Simplified, NO IF CHECK
REM ==============================================================================
echo [4/9] Running Maintainability Index Analysis...

REM Ensure you are in the correct directory (should already be there from STEP 3)
REM cd /d "%BASE_DIR%" (Uncomment if needed, but likely redundant here)

REM Execute radon mi on the src directory and save output to file
REM DO NOT attempt to check %errorlevel% or !errorlevel! here.
echo Executing radon mi for maintainability...
python -m radon mi src\ -s > "03-v1-maintainability-index.txt" 2>&1
echo Command finished. Output saved to 03-v1-maintainability-index.txt.
echo.

REM ==============================================================================
REM STEP 5: LINTING (ruff) - Simplified, NO IF CHECK
REM ==============================================================================
echo [5/9] Running Linting Analysis (Ruff)...

REM Ensure you are in the correct directory (should already be there from STEP 4)
REM cd /d "%BASE_DIR%" (Uncomment if needed, but likely redundant here)

REM Execute ruff check on the src directory and save output to file
REM DO NOT attempt to check %errorlevel% or !errorlevel! here.
echo Executing ruff check...
python -m ruff check src\ > "04-v1-linting-ruff.txt" 2>&1
echo Command finished. Output saved to 04-v1-linting-ruff.txt.
echo.

REM ==============================================================================
REM STEP 6: TYPE CHECKING (mypy) - Simplified, NO IF CHECK
REM ==============================================================================
echo [6/9] Running Type Checking Analysis (MyPy)...

REM Ensure you are in the correct directory (should already be there from STEP 5)
REM cd /d "%BASE_DIR%" (Uncomment if needed, but likely redundant here)

REM Execute mypy on the src directory.
REM It relies on the PYTHONPATH set by pytest.ini being effective in the environment
REM or potentially needing MYPYPATH explicitly set.
REM Using --explicit-package-bases as in your manual command.
REM DO NOT attempt to check %errorlevel% or !errorlevel! here.
echo Executing mypy for type checking...
REM Option 1: Rely on PYTHONPATH from environment (set by pytest.ini when pytest runs)
REM python -m mypy --explicit-package-bases src\ > "05-v1-type-checking-mypy.txt" 2>&1

REM Option 2: Explicitly set MYPYPATH for this command (recommended for clarity)
set "MYPYPATH=%BASE_DIR%src;%MYPYPATH%"
python -m mypy --explicit-package-bases src\ > "05-v1-type-checking-mypy.txt" 2>&1
REM Reset MYPYPATH if needed afterwards (optional, depends on scope)
REM set "MYPYPATH=" (Unsets it only for this script's environment after this point)

echo Command finished. Output saved to 05-v1-type-checking-mypy.txt.
echo.

REM ==============================================================================
REM STEP 7: PACKAGE DEPENDENCIES (pipdeptree) - Simplified, NO IF CHECK
REM ==============================================================================
echo [7/9] Running Package Dependencies Analysis (pipdeptree)...

REM Ensure you are in the correct directory (should already be there from STEP 6)
REM cd /d "%BASE_DIR%" (Uncomment if needed, but likely redundant here)

REM Execute pipdeptree and save output to file
REM DO NOT attempt to check %errorlevel% or !errorlevel! here.
echo Executing pipdeptree for package dependencies...
pipdeptree > "06-v1-dependencies-pipdeptree.txt" 2>&1
echo Command finished. Output saved to 06-v1-dependencies-pipdeptree.txt.
echo.

REM ==============================================================================
REM STEP 8: TEST DURATIONS (pytest) - Simplified, NO IF CHECK
REM ==============================================================================
echo [8/9] Running Test Durations Analysis (pytest --durations)...

REM Ensure you are in the correct directory (should already be there from STEP 7)
REM cd /d "%BASE_DIR%" (Uncomment if needed, but likely redundant here)

REM Execute pytest on tests directory with --durations flag to get slowest tests
REM DO NOT attempt to check %errorlevel% or !errorlevel! here.
echo Executing pytest for test durations...
python -m pytest tests\ --durations=10 > "07-v1-test-durations.txt" 2>&1
echo Command finished. Output saved to 07-v1-test-durations.txt.
echo.

REM ==============================================================================
REM STEP 9: MODULE DEPENDENCY GRAPH (pydeps) - Simplified, NO IF CHECK
REM ==============================================================================
echo [9/9] Running Module Dependency Graph Analysis (pydeps - DOT output)...

REM Ensure you are in the correct directory (should already be there from STEP 8)
REM cd /d "%BASE_DIR%" (Uncomment if needed, but likely redundant here)

REM Execute pydeps as a module to generate the DOT code for the dependency graph of the 'src' package.
REM The --show-dot flag tells pydeps to output the DOT code to stdout.
REM We redirect this output to the .dot file.
REM DO NOT attempt to check %errorlevel% or !errorlevel! here.
echo Executing pydeps to generate DOT code for dependency graph...
python -m pydeps src\ --show-dot --max-bacon 2 > "08-v1-dependency-graph-dot.txt" 2>&1
echo Command finished. DOT code saved to 08-v1-dependency-graph-dot.txt.
echo.

REM Simple end message before pause
echo [FINISH] Static Benchmark Suite v1 completed (commands executed).
echo Check 01-v1-code-coverage.txt through 08-v1-dependency-graph-dot.txt for results/errors.
echo.

pause

endlocal