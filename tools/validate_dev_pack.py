#!/usr/bin/env python3
import argparse, json, re, sys
from pathlib import Path

try:
    import yaml
    import jsonschema
except ImportError as e:
    print(f"Missing dependency: {e}. Install pyyaml jsonschema.", file=sys.stderr)
    sys.exit(2)

REQUIRED = [
    "DEV_PACK_MANIFEST.json",
    "DEV_TASK.md",
    "REQUIREMENTS_SLICE.yaml",
    "ACCEPTANCE_CRITERIA.md",
    "LLD_COMPONENT.md",
    "SEQUENCE.md",
    "openapi.yaml",
    "DATA_MODEL_SLICE.md",
    "SECURITY_CONSTRAINTS.md",
    "OBSERVABILITY_REQUIREMENTS.md",
    "QUALITY_GATES.yaml",
    "TEST_PLAN.md",
    "CONFIG_CONTRACT.yaml",
    "MIGRATION_PLAN.md",
    "ROLLBACK_PLAN.md",
    "RELATED_ADR.md",
    "TRACEABILITY_SLICE.json",
]
PLACEHOLDER = re.compile(r"(TODO|TBD|\?\?\?|<[^>]+>)", re.I)

def read(path):
    return path.read_text(encoding="utf-8")

def check_keywords(text, words):
    low=text.lower()
    return all(w.lower() in low for w in words)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("pack")
    ap.add_argument("--report", default="PRE_DEV_VALIDATION_REPORT.md")
    args=ap.parse_args()
    root=Path(args.pack)
    results=[]

    def add(cid, ok, evidence, owner):
        results.append((cid, "PASS" if ok else "FAIL", evidence, "" if ok else owner))

    # P0 completeness
    missing=[p for p in REQUIRED if not (root/p).exists() or (root/p).stat().st_size==0]
    schemas=list((root/"schemas").glob("*.schema.json")) if (root/"schemas").exists() else []
    if not schemas: missing.append("schemas/*.schema.json")
    add("P0", not missing, "all required files present" if not missing else "missing: "+", ".join(missing), "Analyst/Architect")

    manifest={}
    try:
        manifest=json.loads(read(root/"DEV_PACK_MANIFEST.json"))
        sign=(manifest.get("analyst_signoff",{}).get("status")=="approved" and
              manifest.get("architect_signoff",{}).get("status")=="approved")
        add("P1", sign, "analyst + architect approved" if sign else "sign-off not approved", "Analyst/Architect")
    except Exception as e:
        add("P1", False, f"manifest error: {e}", "Analyst/Architect")

    # P2 requirements
    req_ids=[]
    ac_ids=set()
    try:
        req=yaml.safe_load(read(root/"REQUIREMENTS_SLICE.yaml")) or {}
        items=req.get("requirements",[])
        req_ids=[x.get("id") for x in items]
        ok=bool(items) and len(req_ids)==len(set(req_ids)) and all(
            x.get("id") and x.get("status")=="baselined" and x.get("acceptance_ids") for x in items)
        for x in items:
            for ac in x.get("acceptance_ids") or []: ac_ids.add(ac)
        add("P2", ok, f"{len(items)} requirements; unique/baselined/linked={ok}", "Analyst")
    except Exception as e:
        add("P2", False, f"requirements parse error: {e}", "Analyst")

    # P3 acceptance
    try:
        acc=read(root/"ACCEPTANCE_CRITERIA.md")
        found_ac=set(re.findall(r"\bAC-\d+\b", acc))
        found_req=set(re.findall(r"\bREQ-\d+\b", acc))
        ok=bool(ac_ids) and ac_ids.issubset(found_ac) and set(req_ids).issubset(found_req) and            check_keywords(acc,["Given","When","Then","Negative","Evidence"])
        add("P3", ok, f"AC refs={sorted(found_ac)} REQ refs={sorted(found_req)}", "Analyst/QA")
    except Exception as e:
        add("P3", False, f"acceptance error: {e}", "Analyst/QA")

    # P4 API + schemas
    try:
        api=yaml.safe_load(read(root/"openapi.yaml")) or {}
        api_ok=bool(api.get("openapi") and api.get("info",{}).get("version") and
                    "paths" in api and "components" in api)
        schema_ok=True
        for p in schemas:
            obj=json.loads(read(p))
            jsonschema.Draft202012Validator.check_schema(obj)
        add("P4", api_ok and schema_ok, f"openapi={api_ok}; schemas={len(schemas)} valid", "Architect")
    except Exception as e:
        add("P4", False, f"contract error: {e}", "Architect")

    # P5 data
    try:
        txt=read(root/"DATA_MODEL_SLICE.md")
        ok=check_keywords(txt,["Entities","Keys","Relations","Retention","Owner","classification","Migration"])
        add("P5", ok, "data contract fields present" if ok else "data contract incomplete", "Architect/Data")
    except Exception as e: add("P5",False,str(e),"Architect/Data")

    # P6 security
    try:
        txt=read(root/"SECURITY_CONSTRAINTS.md")
        ok=check_keywords(txt,["Authentication","Authorization","Input validation","Data classification","Secrets","Audit","Negative"])
        add("P6",ok,"security contract fields present" if ok else "security contract incomplete","Security")
    except Exception as e: add("P6",False,str(e),"Security")

    # P7 observability
    try:
        txt=read(root/"OBSERVABILITY_REQUIREMENTS.md")
        ok=check_keywords(txt,["correlation","Metrics","Logs","Traces","SLI/SLO","Alert owner"])
        add("P7",ok,"observability contract fields present" if ok else "observability contract incomplete","SRE/Architect")
    except Exception as e: add("P7",False,str(e),"SRE/Architect")

    # P8 tests
    try:
        txt=read(root/"TEST_PLAN.md")
        ok=check_keywords(txt,["Unit","Integration","Contract","Negative","Security","Observability","Rollback"])
        add("P8",ok,"test categories present" if ok else "test plan incomplete","QA/Architect")
    except Exception as e: add("P8",False,str(e),"QA/Architect")

    # P9 ops
    try:
        cfg=yaml.safe_load(read(root/"CONFIG_CONTRACT.yaml"))
        mig=read(root/"MIGRATION_PLAN.md")
        rb=read(root/"ROLLBACK_PLAN.md")
        ok=bool(cfg and cfg.get("config")) and check_keywords(rb,["Trigger","Target version","Owner","recovery"]) and            ("N/A" in mig or check_keywords(mig,["forward","verification","rollback"]))
        add("P9",ok,"config/migration/rollback defined" if ok else "operations pack incomplete","Architect/SRE")
    except Exception as e: add("P9",False,str(e),"Architect/SRE")

    # P10 traceability
    try:
        tr=json.loads(read(root/"TRACEABILITY_SLICE.json"))
        links=tr.get("links",[])
        by_req={x.get("requirement_id"):x for x in links}
        ok=bool(req_ids) and all(r in by_req for r in req_ids)
        for r in req_ids:
            x=by_req.get(r,{})
            ok=ok and all(x.get(k) for k in ["design_refs","control_refs","test_refs","acceptance_refs","telemetry_refs"])
        add("P10",ok,f"trace links={len(links)} requirements={len(req_ids)}","Analyst/Architect")
    except Exception as e: add("P10",False,f"traceability error: {e}","Analyst/Architect")

    # P11 hygiene
    hits=[]
    for p in root.rglob("*"):
        if p.is_file() and p.name!="PRE_DEV_VALIDATION_REPORT.md":
            try:
                for m in PLACEHOLDER.finditer(read(p)):
                    hits.append(f"{p.relative_to(root)}:{m.group(0)}")
            except UnicodeDecodeError:
                pass
    critical=manifest.get("critical_open_questions",[]) if isinstance(manifest,dict) else ["manifest invalid"]
    secclass=manifest.get("security_classification") if isinstance(manifest,dict) else None
    ok=not hits and not critical and secclass not in (None,"","TBD")
    add("P11",ok,"no unresolved placeholders/open critical questions" if ok else
        f"placeholders={hits[:10]}; critical={critical}; security_classification={secclass}","Pack owner")

    passed=all(r[1]=="PASS" for r in results)
    report=root/args.report
    lines=["# PRE-DEV VALIDATION REPORT","",f"Status: {'PASS' if passed else 'FAIL'}","",
           "| Check | Result | Evidence | Owner if FAIL |","|---|---|---|---|"]
    for cid,status,evidence,owner in results:
        lines.append(f"| {cid} | {status} | {evidence.replace('|','/')} | {owner} |")
    lines += ["",f"Handoff to programmer: {'ALLOWED' if passed else 'BLOCKED'}."]
    report.write_text("\n".join(lines)+"\n",encoding="utf-8")

    for r in results: print(*r,sep=" | ")
    print(f"RESULT={'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1

if __name__=="__main__":
    raise SystemExit(main())
