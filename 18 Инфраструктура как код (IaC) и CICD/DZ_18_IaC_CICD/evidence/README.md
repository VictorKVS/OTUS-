# DZ18 Evidence

This folder intentionally starts without fabricated runtime results.

After local execution, capture:

1. terraform fmt/validate output;
2. terraform plan/apply summary;
3. `minikube status -p father-dz18`;
4. `kubectl get all -n father-dz18 -o wide`;
5. rollout status;
6. health endpoint response;
7. CI workflow result;
8. generated SBOM;
9. SAST/SCA/secret/IaC/container scan reports.

Only then should Lesson 18 be promoted from **draft/M1** to **lab/M1**.
