#!/usr/bin/env bash
python3 fill_dbs.py /corpus/
uwsgi --ini uwsgi.ini
