from pathlib import Path
import json
import sys
import os

root = "/corpora/indexes/"
dd = dict()
for path in Path(root).rglob('db_config.json'):
    dx = dd
    for p in str(path).lstrip(root).split('/')[:-2]:
        if p not in dx.keys():
            dx[p] = {}
        dx = dx[p]
    dx[str(path).lstrip(root).split('/')[-2]] = os.path.abspath(str(path).rstrip('db_config.json'))
    
ff = open('/corpora/dbs.json','wt')
json.dump(dd, ff)
ff.close()
