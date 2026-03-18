@echo off
setlocal enabledelayedexpansion

REM Define the base directory (where this .bat is located)
set BASE_DIR=%~dp0

echo [START] Static Benchmark Suite v1 - Hexagonal Architecture
echo.

REM ==============================================================================
REM STEP 1: RUN UNIT TESTS
REM ==============================================================================
echo [1/2] Running unit tests...
call run_unit_tests.bat

if !errorlevel! neq 0 (
    echo.
    echo FATAL ERROR: Unit tests failed. Stopping benchmark.
    pause
    exit /b !errorlevel!
)

echo Unit tests passed. Proceeding to code coverage...
echo.

REM ==============================================================================
REM STEP 2: CODE COVERAGE (pytest-cov)
REM ==============================================================================
echo [2/2] Running Code Coverage Analysis...

REM Ensure you are in the correct directory (the directory containing src/, tests/, and pytest.ini/)
cd /d "%BASE_DIR%"

REM Echo the current directory for debugging
echo Current directory: %cd%
echo.

REM Execute pytest with coverage, relying on pytest.ini for PYTHONPATH
REM The 'src' directory should be added to sys.path via pytest.ini
python -m pytest --cov=src --cov-report=term-missing > "01-v1-code-coverage.txt" 2>&1

REM Capture the exit code *after* the python command finishes
set PYTEST_EXIT_CODE=!errorlevel!

echo Exit code from pytest: !PYTEST_EXIT_CODE!
echo.

REM Check the exit code and react accordingly
if !PYTEST_EXIT_CODE! neq 0 (
    echo WARNING: Coverage command (pytest) exited with code !PYTEST_EXIT_CODE!.
    echo Full output saved to: 01-v1-code-coverage.txt
    REM Optional: Print the first few lines of the output file to see the error quickly
    echo First few lines of output file:
    powershell -command "& {Get-Content -Path '01-v1-code-coverage.txt' -TotalCount 20}"
) else (
    echo ✅ Code coverage analysis completed successfully.
    echo Results saved to: 01-v1-code-coverage.txt
    REM Optional: Print the last few lines containing the coverage summary
    echo Last few lines of output file (coverage summary):
    powershell -command "& {Get-Content -Path '01-v1-code-coverage.txt' -Tail 15}"
)
echo.