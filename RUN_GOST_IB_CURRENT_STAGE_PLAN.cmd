@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ============================================================
echo OTUS ARCHITECT LIBRARY - VERIFIED CURRENT GOST STAGE PLAN
echo ============================================================
echo Mode: READ ONLY for source/target files; reports only.
echo.

python -m py_compile scripts\stage_verified_current_gosts.py
if errorlevel 1 goto :fail

python scripts\stage_verified_current_gosts.py
if errorlevel 1 goto :fail

echo.
echo PLAN COMPLETE. Review reports\gost_ib_inventory\LATEST_GOST_IB_CURRENT_STAGE.json
exit /b 0

:fail
echo.
echo ERROR/BLOCKED: stage plan stopped with exit code %errorlevel%.
exit /b %errorlevel%
