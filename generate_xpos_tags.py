from json import dump, load
from sys import argv
import os

root = os.getenv('corpora_folder')
if not root.endswith("/"):
    root += "/"
output_folder = os.getenv('output_folder')
if not output_folder.endswith("/"):
    output_folder += "/"

conllu_files = dict()

conllu_file_names = [f for f in os.listdir(root) if f.endswith('.conllu')]

for conllu_file_name in conllu_file_names:
    with open(root + conllu_file_name[:-6] + "json", "r") as metadata_file:
        metadata = load(metadata_file)
        conllu_files[metadata["name"]] = "/corpora/" + metadata["db_path"]

xpos_tags_all = dict()

for conllu_file in conllu_files:
    xpos_tags = set()

    with open(conllu_files[conllu_file], "r", encoding="utf-8") as file:
        for line in file:
            l = line.strip()
            if len(l) > 0 and l[0] in "0123456789":
                xpos_tags.add(l.split("\t")[4] + ">")


    xpos_tags_all[conllu_file] = sorted(list(xpos_tags))

with open(output_folder + "xpos_tags.json", "w") as out:
    dump(xpos_tags_all, out)
