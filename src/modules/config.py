import os
import json

project_path= os.environ['PROJECT_PATH']
result_path= os.environ['RESULT_PATH']
templates_path= os.environ['TEMPLATES_PATH']
git_branch=os.environ['GIT_BRANCH']

with open('{}/config.json'.format(project_path)) as json_file:
    config_json = json.load(json_file)

database_info = config_json['database']