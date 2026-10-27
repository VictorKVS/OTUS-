#!/usr/bin/env python3
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REGISTRY=ROOT/"factory"/"data"/"trace-registry.json"
OUTPUT=ROOT/"factory"/"data"/"runtime-traces.json"

def safe_metadata(meta):
    data=dict(meta or {})
    for key in list(data):
        if key.lower() in {"text","token","secret","password","authorization","bot_token"}:
            data[key]="[REDACTED]"
    return data

def main():
    registry=json.loads(REGISTRY.read_text(encoding="utf-8"))
    groups=defaultdict(list)
    for source in registry.get('sources',[]):
        path=ROOT/source['jsonl_path']
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                event=json.loads(line)
            except json.JSONDecodeError:
                continue
            event['metadata']=safe_metadata(event.get('metadata'))
            groups[event.get('trace_id','unknown')].append(event)

    runs=[]
    for trace_id,events in groups.items():
        events.sort(key=lambda x:x.get('timestamp',''))
        final=events[-1] if events else {}
        runs.append({
            'trace_id':trace_id,
            'kind':'RUNTIME',
            'agent_id':final.get('agent_id'),
            'status':final.get('status'),
            'started_at':events[0].get('timestamp') if events else None,
            'events':events,
        })
    runs.sort(key=lambda x:x.get('started_at') or '',reverse=True)
    payload={'schema_version':'father-runtime-traces.v1','generated_at':datetime.now(timezone.utc).isoformat(),'runs':runs[:100]}
    OUTPUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"EXPORTED traces={len(runs[:100])} -> {OUTPUT}")

if __name__=='__main__':
    main()