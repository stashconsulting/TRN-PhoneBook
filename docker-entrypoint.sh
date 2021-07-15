#!/bin/sh
python migration.py engine init
python migration.py engine migrate
python migration.py engine upgrade

python app.py