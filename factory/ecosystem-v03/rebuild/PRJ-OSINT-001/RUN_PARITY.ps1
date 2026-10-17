param(
    [string]$ReferenceRoot = "G:\\1\\OSINT_TRICOLOR"
)

$ErrorActionPreference = "Stop"

function Header([string]$Text) {
    Write-Host ""
    Write-Host "=====================================================================" -ForegroundColor DarkCyan
    Write-Host (" FATHER :: OSINT REBUILD · " + $Text) -ForegroundColor Cyan
    Write-Host "=====================================================================" -ForegroundColor DarkCyan
}

$CaseRoot = $PSScriptRoot
$Runtime  = Join-Path $CaseRoot "runtime"
$Parity   = Join-Path $CaseRoot "parity\\run_parity.py"
$Evidence = Join-Path $CaseRoot "evidence\\generated\\parity-report.json"

Header "REFERENCE CHECK"

if (-not (Test-Path -LiteralPath $ReferenceRoot)) {
    throw "Reference repository not found: $ReferenceRoot"
}

$ReferenceAgent = Join-Path $ReferenceRoot "agent.py"
if (-not (Test-Path -LiteralPath $ReferenceAgent)) {
    throw "Reference agent.py not found: $ReferenceAgent"
}

Write-Host "REFERENCE: $ReferenceRoot" -ForegroundColor Green
Write-Host "READ-ONLY: original source is not modified." -ForegroundColor Yellow

Header "REFERENCE TESTS"
Push-Location $ReferenceRoot
try {
    python -B -m unittest discover -s tests -v
    if ($LASTEXITCODE -ne 0) { throw "Reference tests failed. Golden baseline is not green." }
}
finally { Pop-Location }

Header "FATHER REBUILD TESTS"
Push-Location $Runtime
try {
    python -B -m unittest discover -s tests -v
    if ($LASTEXITCODE -ne 0) { throw "FATHER rebuild unit tests failed." }
}
finally { Pop-Location }

Header "REFERENCE VS FATHER PARITY"
python -B $Parity --reference-root $ReferenceRoot --output $Evidence
$ParityExit = $LASTEXITCODE

if ($ParityExit -eq 0) {
    Write-Host ""
    Write-Host "PARITY GATE: PASS" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "PARITY GATE: FAIL" -ForegroundColor Red
}

Write-Host "Evidence: $Evidence" -ForegroundColor Cyan
if (Test-Path -LiteralPath $Evidence) {
    Write-Host ""
    Get-Content -LiteralPath $Evidence -Raw | ConvertFrom-Json | Select-Object -ExpandProperty gate | Format-List
}

exit $ParityExit