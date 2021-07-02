#!/usr/bin/env bash

python3 -m venv virtualenv
./virtualenv/bin/pip install -r requirements.txt
./virtualenv/bin/pip install -r dev-requirements.txt
