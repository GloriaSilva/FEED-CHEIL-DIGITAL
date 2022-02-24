#!/bin/bash
# Change to project directory
cd $1

# Activate virtualenv
source feeds-cheil-venv/bin/activate 

# Source env variables
source .env

# Execute python process
python3 src/scripts/execution/pyscripts/FeedDaily_Cheil.py $2 --push


