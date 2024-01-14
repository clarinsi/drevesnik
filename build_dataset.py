import os
from json import load, dump
from sys import argv, maxsize
from pathlib import Path

root = os.getenv('CORPORA_FOLDER', '/corpora_folder/')
if not root.endswith('/'):
    root += '/'
indexes_folder = os.getenv('INDEXES_FOLDER', '/indexes_folder/')
if not indexes_folder.endswith('/'):
    indexes_folder += '/'

####### build indexes from conllu
   
conllu_files = [f for f in os.listdir(root) if f.endswith('.conllu')]

for conllu_file in conllu_files:
    with open(root + conllu_file[:-6] + "json", "r") as metadata_file:
        metadata = load(metadata_file)
        if (os.path.exists(indexes_folder + metadata["name"] + "/")):
            raise Exception(metadata["name"] + " is already present in the output map")

for conllu_file in conllu_files:
    with open(root + conllu_file[:-6] + "json", "r") as metadata_file:
        metadata = load(metadata_file)
        print(f"Started building index for corpus: {metadata['name']}")
        os.system(f"cd ..; cat {root}{conllu_file} | python build_index.py --lang sl -d {indexes_folder}{metadata['name']}")
        print(f"Finished building index for corpus: {metadata['name']}")


####### build xpos_tags from indexes

conllu_files = dict()

conllu_file_names = [f for f in os.listdir(root) if f.endswith('.conllu')]

for conllu_file_name in conllu_file_names:
    with open(root + conllu_file_name[:-6] + "json", "r") as metadata_file:
        metadata = load(metadata_file)
        conllu_files[metadata["name"]] = root + conllu_file_name

xpos_tags_all = dict()
if os.path.exists(indexes_folder + "xpos_tags.json"):
    with open(indexes_folder + "xpos_tags.json", "r") as xpos_file:
        xpos_tags_all = load(xpos_file)
    

for conllu_file in conllu_files:
    xpos_tags = set()

    with open(conllu_files[conllu_file], "r", encoding="utf-8") as file:
        for line in file:
            l = line.strip()
            if len(l) > 0 and l[0] in "0123456789":
                xpos_tags.add(l.split("\t")[4] + ">")


    xpos_tags_all[conllu_file] = sorted(list(xpos_tags))

with open(indexes_folder + "xpos_tags.json", "w") as out:
    dump(xpos_tags_all, out)


####### fill dbs.json metadata

dd = dict()
if os.path.exists(indexes_folder + "dbs.json"):
    with open(indexes_folder + "dbs.json", "r") as dd_file:
        dd = load(dd_file)

conllu_files = [f for f in os.listdir(root) if f.endswith('.conllu')]

for conllu_file in conllu_files:
    with open(root + conllu_file[:-6] + "json", "r") as metadata_file:
        metadata = load(metadata_file)
        if "priority" not in metadata:
            metadata["priority"] = maxsize
        metadata["priority"] = int(metadata["priority"])
        dd[metadata["name"]] = metadata
    
with open(indexes_folder + 'dbs.json','wt') as metadata_file:
    dump(dd, metadata_file)
