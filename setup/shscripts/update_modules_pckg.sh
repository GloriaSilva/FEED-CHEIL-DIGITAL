#!/bin/bash
# Install local folder in editing mode
pip install -e src/modules/
# Update the git reference
pip freeze > setup/requirements.txt 
# Change the user for DataAndPerformance