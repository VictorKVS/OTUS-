@echo off
setlocal EnableExtensions

cd /d "%~dp0"

set "PRIVATE_ROOT=%~dp0_PRIVATE_BOOK_CORPUS"
set "INVENTORY_OUT=%~dp0knowledge\library_inventory\generated"

echo ============================================================
echo FATHER Architecture Library - local intake
echo ============================================================
echo Repo root: %~dp0
echo.

where py >nul 2>nul
if %errorlevel%==0 (
    set "PY=py -3"
) else (
    set "PY=python"
)

echo [1/3] Scanning local library...
rem Do not place the Cyrillic library folder name in this CMD file.
rem Python 3 reads its UTF-8 source correctly and owns the Unicode default path.
%PY% tools\library_scan.py --output "%INVENTORY_OUT%"
if errorlevel 1 goto :fail

echo.
echo [2/3] Extracting selected pilot book...
%PY% tools\book_extract.py --private-root "%PRIVATE_ROOT%"
if errorlevel 6 goto :ocr
if errorlevel 1 goto :fail

echo.
echo [3/3] Preparing translation units...
%PY% tools\book_prepare_translation.py --private-root "%PRIVATE_ROOT%"
if errorlevel 1 goto :fail

echo.
echo DONE.
echo Inventory: %INVENTORY_OUT%
echo Private corpus: %PRIVATE_ROOT%
echo Next: translate translation_units.jsonl and feed the aligned corpus to Knowledge Analyst.
exit /b 0

:ocr
echo.
echo The selected PDF does not contain enough machine-readable text.
echo Extraction stopped safely with NEEDS_OCR. No semantic analysis was started.
exit /b 6

:fail
echo.
echo ERROR: pipeline stopped with exit code %errorlevel%.
exit /b %errorlevel%
