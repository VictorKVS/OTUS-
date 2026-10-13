$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$Required = @("docker", "terraform", "minikube", "kubectl", "python")
foreach ($cmd in $Required) {
    if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) {
        throw "Required command not found in PATH: $cmd"
    }
}

docker info *> $null
if ($LASTEXITCODE -ne 0) {
    throw "Docker is not available. Start Docker Desktop first."
}

if (-not $env:TF_VAR_minio_root_user) {
    $env:TF_VAR_minio_root_user = "fatherlab"
}
if (-not $env:TF_VAR_minio_root_password) {
    $env:TF_VAR_minio_root_password = [guid]::NewGuid().ToString("N")
}

Write-Host "== Terraform init/validate/apply ==" -ForegroundColor Cyan
Push-Location ".\terraform\local-lab"
terraform init
terraform fmt -check
terraform validate
terraform apply -auto-approve
Pop-Location

Write-Host "== Build local agent image ==" -ForegroundColor Cyan
docker build -t father-dz18-agent:local .

Write-Host "== Load image into Minikube ==" -ForegroundColor Cyan
minikube image load father-dz18-agent:local -p father-dz18

Write-Host "== Select Minikube context ==" -ForegroundColor Cyan
kubectl config use-context father-dz18

Write-Host "== Apply Kubernetes manifests ==" -ForegroundColor Cyan
kubectl apply -f ".\k8s\namespace.yaml"
kubectl apply -f ".\k8s\deployment.yaml"
kubectl apply -f ".\k8s\service.yaml"
kubectl apply -f ".\k8s\networkpolicy.yaml"

Write-Host "== Wait for rollout ==" -ForegroundColor Cyan
kubectl rollout status deployment/father-agent -n father-dz18 --timeout=120s

Write-Host ""
Write-Host "DZ18 lab deployed into the shared Minikube runtime." -ForegroundColor Green
Write-Host "MinIO API:     http://127.0.0.1:9000"
Write-Host "MinIO Console: http://127.0.0.1:9001"
Write-Host ""
Write-Host "Run in a separate PowerShell:"
Write-Host "kubectl port-forward -n father-dz18 svc/father-agent 8089:8080"
Write-Host "Then:"
Write-Host "Invoke-RestMethod http://127.0.0.1:8089/health"
