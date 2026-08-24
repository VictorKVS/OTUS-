@echo off
setlocal EnableExtensions

cd /d "%~dp0"
set "PY=python"

echo ============================================================
echo FATHER Architecture Book - translation smoke test
echo ============================================================
%PY% --version
if errorlevel 1 goto :fail
echo.

echo [1/3] Detecting local OpenAI-compatible translation endpoint...
%PY% tools\book_translate.py --probe-only
if errorlevel 1 goto :no_server

echo.
echo [2/3] Translating only 3 remaining units...
%PY% tools\book_translate.py --limit 3
set "TR_RC=%errorlevel%"
rem Exit code 7 means translation is intentionally incomplete after a limited smoke run.
if not "%TR_RC%"=="0" if not "%TR_RC%"=="7" goto :fail_code

echo.
echo [3/3] Showing local EN/RU preview...
%PY% tools\book_translation_preview.py --count 3 --chars 700
if errorlevel 1 goto :fail

echo.
echo SMOKE TEST DONE.
echo Review the 3 EN/RU samples above before translating the rest of the book.
exit /b 0

:no_server
echo.
echo No local OpenAI-compatible LLM server was detected.
echo Supported automatic probes: 127.0.0.1 ports 8080, 1234, 11434.
echo You can also set BOOK_LLM_BASE_URL and BOOK_LLM_MODEL explicitly.
exit /b 2

:fail_code
echo.
echo ERROR: translation command stopped with exit code %TR_RC%.
exit /b %TR_RC%

:fail
echo.
echo ERROR: smoke pipeline stopped with exit code %errorlevel%.
exit /b %errorlevel%
