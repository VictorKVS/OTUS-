@echo off
setlocal EnableExtensions

cd /d "%~dp0"

set "LIBRARY_ROOT=G:\1\OTUS\Библиотека"
set "PRIVATE_ROOT=G:\1\OTUS\_PRIVATE_BOOK_CORPUS"
set "INVENTORY_OUT=G:\1\OTUS\knowledge\library_inventory\generated"

echo ============================================================
echo FATHER Architecture Library - local intake
echo ============================================================
echo Library: %LIBRARY_ROOT%
echo.

where py >nul 2>nul
if %errorlevel%==0 (
    set "PY=py -3"
) else (
    set "PY=python"
)

%PY% tools\library_scan.py "%LIBRARY_ROOT%" --output "%INVENTORY_OUT%"
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
