@echo off
setlocal

REM Set the PYTHONPATH to include the src directory of the hexagonal architecture
set PYTHONPATH=%~dp0backend\experiments\architectures\hexagonal\src;%PYTHONPATH%

REM Run pytest on the hexagonal architecture tests with verbose output and short traceback
REM python -m pytest backend\experiments\architectures\hexagonal\tests\ -v --tb=short
python -m pytest backend\experiments\architectures\hexagonal\tests\ --durations=10

REM Pause to view the result (optional, remove if you want it to close automatically)
pause

endlocal