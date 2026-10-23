#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"factory"/"data"/"combat-template-c00-c99.json"

def main():
    data=json.loads(PATH.read_text(encoding="utf-8"))
    stages=data.get("stages",[])
    errors=[]
    if len(stages)!=100:
        errors.append(f"expected 100 stages, got {len(stages)}")
    expected=[f'C{i:02d}' for i in range(100)]
    actual=[x.get("code") for x in stages]
    if actual!=expected:
        errors.append("stage codes are not contiguous C00..C99")
    if data.get('legacy_recovered_range')!='C00-C20':
        errors.append("legacy range must remain C00-C20")
    for i,s in enumerate(stages):
        if not s.get('directory') or not s.get('gate'):
            errors.append(f"{s.get('code')}: missing directory/gate")
        want=expected[i+1] if i<99 else None
        if s.get('next')!=want:
            errors.append(f"{s.get('code')}: next={s.get('next')} expected={want}")
    print(f'CHECKED combat template stages={len(stages)} errors={len(errors)}')
    for e in errors: print('FAIL:',e)
    return 1 if errors else 0

if __name__=='__main__':
    sys.exit(main())