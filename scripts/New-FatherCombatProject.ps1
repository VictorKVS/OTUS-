param(
  [Parameter(Mandatory=$true)][string]$ProjectName,
  [string]$RootBase = 'G:\1',
  [string]$GitHubOwner = 'VictorKVS',
  [ValidateSet('private','public')][string]$Visibility = 'private',
  [switch]$Force
)

$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path $PSScriptRoot -Parent
$TemplatePath = Join-Path $RepoRoot 'factory\data\combat-template-c00-c99.json'
if (-not (Test-Path $TemplatePath)) { throw "Template not found: $TemplatePath" }

$Template = Get-Content $TemplatePath -Raw -Encoding UTF8 | ConvertFrom-Json
$Root = Join-Path $RootBase $ProjectName

Write-Host "[A00] PROJECT: $ProjectName" -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path $Root | Out-Null
Set-Location $Root

$BaseDirs = @(
  'docs','src','tests','config','scripts','runtime','runtime\traces',
  '.github','.github\workflows','dossier'
)
foreach ($d in $BaseDirs) { New-Item -ItemType Directory -Force -Path (Join-Path $Root $d) | Out-Null }

Write-Host '[A02] C00-C99 DOSSIER' -ForegroundColor Cyan
foreach ($stage in $Template.stages) {
  $dir = Join-Path $Root ('dossier\' + $stage.directory)
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
  $readme = Join-Path $dir 'README.md'
  if ($Force -or -not (Test-Path $readme)) {
    $next = if ($stage.next) { $stage.next } else { 'CLOSE' }
    @"
# $($stage.code) · $($stage.name)

Origin: $($stage.origin)
Gate: $($stage.gate)
Next: $next

## INPUT

## DEPENDENCIES

## PROCESS

## ARTIFACTS

## VALIDATION

## EVIDENCE

## GATE

## FAIL ACTION

## OUTPUT

## NEXT

> NO EVIDENCE -> NO PROMOTION
"@ | Set-Content -Encoding UTF8 $readme
  }
}

$readmePath = Join-Path $Root 'README.md'
if ($Force -or -not (Test-Path $readmePath)) {
@"
# $ProjectName

FATHER Combat Project

Lifecycle: C00 -> C99
Rule: NO EVIDENCE -> NO PROMOTION

Start: dossier/C00_INTAKE/README.md
"@ | Set-Content -Encoding UTF8 $readmePath
}

$gitignore = Join-Path $Root '.gitignore'
if ($Force -or -not (Test-Path $gitignore)) {
@'
.env
.venv/
venv/
__pycache__/
*.pyc
.pytest_cache/
runtime/traces/*.jsonl
runtime/tmp/
*.log
.idea/
.vscode/
Thumbs.db
.DS_Store
'@ | Set-Content -Encoding UTF8 $gitignore
}

$envExample = Join-Path $Root '.env.example'
if ($Force -or -not (Test-Path $envExample)) {
  "# Secrets must never be committed`n" | Set-Content -Encoding UTF8 $envExample
}

Write-Host '[A04] GIT INIT' -ForegroundColor Cyan
if (-not (Test-Path (Join-Path $Root '.git'))) { git init -b main | Out-Host }

git add .
if (git ls-files --error-unmatch .env 2>$null) { throw '.env is tracked. Remove it before continuing.' }
git diff --cached --check

$hasHead = $true
git rev-parse --verify HEAD *> $null
if ($LASTEXITCODE -ne 0) { $hasHead = $false }

$changes = git status --porcelain
if ($changes) {
  $msg = if ($hasHead) { 'chore: apply FATHER combat project template' } else { "chore: bootstrap $ProjectName" }
  git commit -m $msg | Out-Host
}

Write-Host '[A07-A08] GITHUB' -ForegroundColor Cyan
$FullRepo = "$GitHubOwner/$ProjectName"
$repoExists = $true
gh repo view $FullRepo *> $null
if ($LASTEXITCODE -ne 0) { $repoExists = $false }

if (-not $repoExists) {
  if ($Visibility -eq 'private') {
    gh repo create $FullRepo --private --source . --remote origin | Out-Host
  } else {
    gh repo create $FullRepo --public --source . --remote origin | Out-Host
  }
} else {
  $url = "https://github.com/$FullRepo.git"
  $origin = git remote get-url origin 2>$null
  if ($LASTEXITCODE -ne 0) { git remote add origin $url }
  elseif ($origin -ne $url) { git remote set-url origin $url }
}

git branch -M main
git push -u origin main | Out-Host

Write-Host '[A09] VERIFY' -ForegroundColor Cyan
git status --short --branch | Out-Host
git remote -v | Out-Host
git log --oneline -3 | Out-Host
gh repo view $FullRepo --json nameWithOwner,visibility,url,defaultBranchRef | Out-Host

Write-Host "READY: $Root -> $FullRepo" -ForegroundColor Green
Write-Host 'NEXT: open dossier\C00_INTAKE\README.md' -ForegroundColor Green