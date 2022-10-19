from json import dump

conllu_files = {
    "SSJ": "../../sl_ssj-ud.conllu",
    "SST": "../../sl_sst-ud.conllu",
    "ccKres": "../../cckres.conllu"
}

xpos_tags_all = dict()

for conllu_file in conllu_files:
    xpos_tags = set()

    with open(conllu_files[conllu_file], "r", encoding="utf-8") as file:
        for line in file:
            l = line.strip()
            if len(l) > 0 and l[0] in "0123456789":
                xpos_tags.add(l.split("\t")[4] + ">")


    xpos_tags_all[conllu_file] = sorted(list(xpos_tags))

with open("xpos_tags.json", "w") as out:
    dump(xpos_tags_all, out)
