$ErrorActionPreference = "Continue"

$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

kubectl delete namespace father-dz18 --ignore-not-found=true

Push-Location ".\terraform\local-lab"
if (-not $env:TF_VAR_minio_root_user) { $env:TF_VAR_minio_root_user = "fatherlab" }
if (-not $env:TF_VAR_minio_root_password) { $env:TF_VAR_minio_root_password = "destroy-only-placeholder" }
terraform destroy -auto-approve
Pop-Location

kind delete cluster --name father-dz18

Write-Host "DZ18 local lab destroyed."
