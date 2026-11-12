#!/usr/bin/env python3
"""Create deterministic list of SHA-256 hashes, excluding the manifest itself."""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
files=[]
for p in sorted(ROOT.rglob('*')):
    if not p.is_file() or p.name=='MANIFEST.json' or '__pycache__' in p.parts: continue
    data=p.read_bytes()
    files.append({'path':p.relative_to(ROOT).as_posix(), 'bytes':len(data), 'sha256':hashlib.sha256(data).hexdigest()})
manifest={'name':'HARDSET Knowledge Pack','version':'1.0',
          'created':'2026-11-12','includes_personal_user_training_data':False,
          'source_type':'approved rule reconstruction/normalization + original support tooling',
          'files':files}
(ROOT/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Wrote manifest for {len(files)} files.')
