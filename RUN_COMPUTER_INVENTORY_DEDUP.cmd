@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================================
echo OTUS / FATHER - COMPUTER STORAGE INVENTORY
ECHO READ ONLY SOURCE SCAN + SHA-256 FOR DUPLICATE CANDIDATES
ECHO ============================================================

python -m py_compile scripts\build_storage_inventory.py
if errorlevel 1 exit /b %errorlevel%

python scripts\build_storage_inventory.py --config data\computer_inventory_roots.json --hash duplicate-candidates
exit /b %errorlevel%
