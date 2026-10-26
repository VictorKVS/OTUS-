# FTH-CMP-CONNECTIVITY-001

Pre-flight network route checker for FATHER products.

Current status: **DESIGN / implementation present / runtime validation pending**.

Example:

```powershell
python .\factory\components\connectivity-check\check.py --output .\connectivity-evidence.json
```

With an HTTP proxy:

```powershell
python .\factory\components\connectivity-check\check.py --proxy http://127.0.0.1:8080 --output .\connectivity-proxy-evidence.json
```

This does not start or configure a VPN. It only proves whether the required endpoints are reachable over the selected direct/proxy route.
