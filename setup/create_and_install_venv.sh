#!/bin/bash

# To be executed at root project
# Install venv
python3 -m pip install virtualenv
# Create venv
python3 -m virtualenv feeds-cheil-venv 
# Activate
source feeds-cheil-venv/bin/activate

pip install -r setup/requirements.txt

source .env
