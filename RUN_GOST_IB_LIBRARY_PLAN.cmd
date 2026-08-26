@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ============================================================
echo OTUS ARCHITECT LIBRARY - GOST IB INVENTORY PLAN
echo ============================================================
echo Source: %%USERPROFILE%%\Downloads
echo Target: .\Библиотека\Архитектор\ИБ\ГОСТ
echo Mode: READ ONLY for source/target files; reports only.
echo.

python -m py_compile scripts\inventory_gost_ib_library.py
if errorlevel 1 goto :fail

python scripts\inventory_gost_ib_library.py
if errorlevel 1 goto :fail

echo.
echo PLAN COMPLETE. Review reports\gost_ib_inventory\LATEST_GOST_IB_INVENTORY.json
exit /b 0

:fail
echo.
echo ERROR: GOST IB inventory PLAN stopped with exit code %errorlevel%.
exit /b %errorlevel%
