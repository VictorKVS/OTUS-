@echo off
setlocal EnableExtensions

cd /d "%~dp0"
set "PY=python"

echo ============================================================
echo FATHER Architecture Book - blind translator jury
echo ============================================================
%PY% --version
if errorlevel 1 goto :fail
echo.

%PY% tools\book_translation_jury.py --finalists 2 --judges 2
if errorlevel 1 goto :fail

echo.
echo Jury complete.
echo If decision=AUTO_SELECTED, run:
echo   python tools\book_translate_selected.py
echo.
echo If decision=HUMAN_REVIEW_REQUIRED, inspect translation_jury_report.md
echo and translation_tournament_report.md before manual selection.
exit /b 0

:fail
echo.
echo ERROR: jury stopped with exit code %errorlevel%.
exit /b %errorlevel%
