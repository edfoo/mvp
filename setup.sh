#!/bin/bash

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

echo -e "Now you can run \n\npython portfolio.py -c example.json"
