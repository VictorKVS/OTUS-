@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER Knowledge Factory - OTUS LOCAL INVENTORY
echo Local files -^> SHA256 -^> lesson mapping -^> processing routes
echo ============================================================
echo.

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

%PYTHON_EXE% --version
if errorlevel 1 (
  echo ERROR: Python was not found.
  pause
  exit /b 1
)

%PYTHON_EXE% knowledge_factory\scan_local_materials.py
set "RC=%ERRORLEVEL%"

echo.
echo Review package:
echo knowledge_factory\reports\LOCAL_INVENTORY.md
echo knowledge_factory\reports\local_inventory.jsonl
echo.
if "%RC%"=="0" (
  echo PASS: OTUS local inventory generated.
) else (
  echo FAIL: inventory runner returned code %RC%.
)

pause
exit /b %RC%
