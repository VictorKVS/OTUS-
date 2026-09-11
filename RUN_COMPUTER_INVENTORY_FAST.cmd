@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================================
echo OTUS / FATHER - COMPUTER STORAGE INVENTORY FAST
ECHO READ ONLY SOURCE SCAN / NO FILE HASHING
ECHO ============================================================

python -m py_compile scripts\build_storage_inventory.py
if errorlevel 1 exit /b %errorlevel%

python scripts\build_storage_inventory.py --config data\computer_inventory_roots.json --hash none
exit /b %errorlevel%
