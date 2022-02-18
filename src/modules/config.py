import os

project_path= os.environ['PROJECT_PATH']
result_path= os.environ['RESULT_PATH']
templates_path= os.environ['TEMPLATES_PATH']

with open('{}/src/modules/config.json') as json_file:
    config_json = json.load(json_file)

database_info = config_json['database']