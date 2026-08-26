@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ============================================================
echo OTUS ARCHITECT LIBRARY - GOST IB SAFE COPY
echo ============================================================
echo Source: .\Библиотека\разобрать
echo Target: .\Библиотека\Архитектор\ИБ\ГОСТ\_CURRENTNESS_PENDING
echo Action: COPY ONLY, SHA-256 verified, no delete/move.
echo Currentness is NOT asserted until Rosstandart verification.
echo.

python -m py_compile scripts\inventory_gost_ib_library.py
if errorlevel 1 goto :fail

python scripts\inventory_gost_ib_library.py --apply
if errorlevel 1 goto :fail

echo.
echo APPLY COMPLETE. Review reports\gost_ib_inventory\LATEST_GOST_IB_INVENTORY.json
exit /b 0

:fail
echo.
echo ERROR: GOST IB safe copy stopped with exit code %errorlevel%.
exit /b %errorlevel%
