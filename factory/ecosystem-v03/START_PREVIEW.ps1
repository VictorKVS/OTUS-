$ErrorActionPreference = "Stop"

param(
    [int]$Port = 8093
)

function Write-FatherHeader([string]$Title) {
    Write-Host ""
    Write-Host "=====================================================================" -ForegroundColor DarkCyan
    Write-Host (" FATHER :: " + $Title) -ForegroundColor Cyan
    Write-Host "=====================================================================" -ForegroundColor DarkCyan
}

$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path

Write-FatherHeader "ECOSYSTEM WORKSPACE PREVIEW"
Write-Host ("Root: " + $Root)

$Commit = git -C $Root rev-parse --short HEAD
Write-Host ("Commit: " + $Commit) -ForegroundColor Green

Write-FatherHeader "HTTP SERVER"
$Listener = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue

if (-not $Listener) {
    Start-Process powershell -ArgumentList @(
        "-NoExit",
        "-Command",
        ('Set-Location "' + $Root + '"; python -m http.server ' + $Port)
    )
    Start-Sleep -Seconds 2
}

$Url = "http://localhost:$Port/factory/ecosystem-v03/"
Write-Host ("Open: " + $Url) -ForegroundColor Green
Start-Process $Url

Write-FatherHeader "READY"
Write-Host "This preview runs from the dedicated FATHER worktree." -ForegroundColor Green
Write-Host "The primary G:\1\OTUS working tree is not modified." -ForegroundColor Yellow
