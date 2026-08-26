@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ============================================================
echo OTUS ARCHITECT LIBRARY - VERIFIED CURRENT GOST STAGE APPLY
echo ============================================================
echo Copy-only. No source file is moved or deleted.
echo Apply is blocked if one designation has multiple distinct SHA-256 files.
echo.

python -m py_compile scripts\stage_verified_current_gosts.py
if errorlevel 1 goto :fail

python scripts\stage_verified_current_gosts.py --apply --confirm COPY_VERIFIED_CURRENT_GOSTS
if errorlevel 1 goto :fail

echo.
echo APPLY COMPLETE. Review reports\gost_ib_inventory\LATEST_GOST_IB_CURRENT_STAGE.json
exit /b 0

:fail
echo.
echo ERROR/BLOCKED: stage apply stopped with exit code %errorlevel%.
exit /b %errorlevel%
