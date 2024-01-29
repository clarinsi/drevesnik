from os import system, mkdir, path
from json import load
from sys import argv
import logging
from shutil import rmtree

root = "/corpora/"

if path.exists(root + "indexes/"):
    rmtree(root + "indexes/")
mkdir(root + "indexes/")

with open(root + "db_metadata.json", "r") as metadata_file:
    metadata = load(metadata_file)
    for db in metadata:
        logging.info(f"Started building index for corpus: {db}")
        system(f"cd ..; cat {root}{metadata[db]['db_path']} | python3 build_index.py --lang {metadata[db]['db_lang']} -d {root}indexes/{db}")
        logging.info(f"Finished building index for corpus: {db}")
