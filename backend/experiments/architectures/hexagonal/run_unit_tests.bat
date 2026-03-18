@echo off
setlocal

REM Define the directory where this script is located
set BASE_DIR=%~dp0

REM Define the PYTHONPATH to include the 'src' directory relative to this script
REM The '..' is necessary because the script is in the 'hexagonal' folder, and 'src' is at the same level
set PYTHONPATH=%BASE_DIR%src;% Display the PYTHONPATH for debugging (optional)
echo PYTHONPATH is set to: %PYTHONPATH%
echo.

REM Navigate to the directory where the script is located (extra guarantee)
cd /d "%BASE_DIR%"

REM Run pytest on the specific tests for this architecture
echo Running unit tests for Hexagonal Architecture...
python -m pytest tests\ --durations=10

REM Check the exit code of pytest
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Unit tests failed! Exit code: %errorlevel%
    echo Stopping execution due to test failures.
    REM Optional: pause
    REM exit /b %errorlevel%
) else (
    REM If tests pass
    echo.
    echo SUCCESS: All unit tests passed!
    echo.
)

REM Optional: pause
REM pause

endlocal