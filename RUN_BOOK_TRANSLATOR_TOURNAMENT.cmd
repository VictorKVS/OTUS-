@echo off
setlocal EnableExtensions
cd /d "%~dp0"

set "PY=python"

echo ============================================================
echo FATHER Architecture Book - translator tournament
echo ============================================================
%PY% --version
if errorlevel 1 exit /b %errorlevel%
echo.

%PY% tools\book_translation_tournament.py --samples 5 --max-models 5
if errorlevel 1 (
  echo.
  echo Tournament did not complete. Ensure at least two suitable text models are exposed.
  exit /b %errorlevel%
)

echo.
echo Tournament complete.
echo If decision=AUTO_SELECTED, the winner is already saved locally.
echo If decision=HUMAN_REVIEW_REQUIRED, open the local translation_tournament_report.md
echo and select a rank with:
echo   python tools\book_translation_select.py 1
echo.
echo To translate with the selected winner:
echo   python tools\book_translate_selected.py
exit /b 0
