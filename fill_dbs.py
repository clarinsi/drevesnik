from pathlib import Path
import json
import sys
import os

output_folder = os.getenv('output_folder')
if not output_folder.endswith("/"):
    output_folder += "/"

dd = dict()
for path in Path(output_folder).rglob('db_config.json'):
    dx = dd
    for p in str(path).lstrip(output_folder).split('/')[:-2]:
        if p not in dx.keys():
            dx[p] = {}
        dx = dx[p]
    dx[str(path).lstrip(output_folder).split('/')[-2]] = os.path.abspath(str(path).rstrip('db_config.json'))
    
ff = open(output_folder + 'dbs.json','wt')
json.dump(dd, ff)
ff.close()
