import os
import glob
import time
import json

# hour
# limit = time.time() - 60*60
# day
# limit = time.time() - 60*60*24
# week
# limit = time.time() - 60*60*24*7
# month
# limit = time.time() - 60*60*24*7*4

config_folder = os.getenv('CONFIG_FOLDER', '/configs/')
with open(config_folder + 'config.json', 'r') as f:
    config = json.load(f)

ttl = config.get('result_ttl_seconds', 2419200) #2419200 -> month
limit = time.time() - ttl

skip_cleaning = set()

try:
    with open("skip_cache_clean.txt", "r") as skip_clean_file:
        for line in skip_clean_file:
            skip_cleaning.add(line.strip())
except:
    pass

print(skip_cleaning)

for f in glob.glob('./res/*'):
    tmp_f = f[5:]
    print(tmp_f)
    skip = False
    for name in tmp_f[:tmp_f.rfind(".")].split("_"):
        if name.replace("/","") in skip_cleaning:
            skip = True
            break
    if not skip and os.stat(f).st_mtime < limit:
        print("cleaned",  tmp_f)
        os.remove(f)