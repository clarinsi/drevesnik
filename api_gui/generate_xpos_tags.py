from json import dump, load
from sys import argv


conllu_files = dict()

with open("/corpora/db_metadata.json", "r") as metadata_file:
    metadata = load(metadata_file)
    for db in metadata:
        conllu_files[db] = "/corpora/" + metadata[db]["db_path"]


xpos_tags_all = dict()

for conllu_file in conllu_files:
    xpos_tags = set()

    with open(conllu_files[conllu_file], "r", encoding="utf-8") as file:
        for line in file:
            l = line.strip()
            if len(l) > 0 and l[0] in "0123456789":
                xpos_tags.add(l.split("\t")[4] + ">")


    xpos_tags_all[conllu_file] = sorted(list(xpos_tags))

with open("/corpora/xpos_tags.json", "w") as out:
    dump(xpos_tags_all, out)
