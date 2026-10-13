$ErrorActionPreference = "Stop"

Write-Host "== Cluster ==" -ForegroundColor Cyan
kind get clusters

Write-Host "== Namespace objects ==" -ForegroundColor Cyan
kubectl get all -n father-dz18 -o wide

Write-Host "== Deployment rollout ==" -ForegroundColor Cyan
kubectl rollout status deployment/father-agent -n father-dz18 --timeout=60s

Write-Host "== Pod security/runtime summary ==" -ForegroundColor Cyan
kubectl get pod -n father-dz18 -l app=father-agent -o jsonpath="{range .items[*]}{.metadata.name}{'  image='}{.spec.containers[0].image}{'  ready='}{.status.containerStatuses[0].ready}{'\n'}{end}"

Write-Host ""
Write-Host "For HTTP evidence run:" -ForegroundColor Yellow
Write-Host "kubectl port-forward -n father-dz18 svc/father-agent 8089:8080"
Write-Host "Invoke-RestMethod http://127.0.0.1:8089/health"
