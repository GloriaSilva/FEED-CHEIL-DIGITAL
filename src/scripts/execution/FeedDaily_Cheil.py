import datetime
import os
from config import project_path
import subprocess
import sys

base_feed_path = f'{project_path}/src/scripts/data'
providers = ['Facebook','Criteo', 'Google', 'AWIN', 'KuantoKusta']

country = sys.argv[1]


if __name__ == '__main__':
    begin_time = datetime.datetime.now()
    print(datetime.datetime.now())
   
    print('Updating URL dictionary')
    subprocess.run(['python3', f'{base_feed_path}/url/URL_Generator_v2.py', country])

    for provider in providers:
        print(f'Generating {provider} feed')
        subprocess.run(['python3', f'{base_feed_path}/providers/{provider}Feed_Cheil.py', country])
   

    print(datetime.datetime.now() - begin_time)