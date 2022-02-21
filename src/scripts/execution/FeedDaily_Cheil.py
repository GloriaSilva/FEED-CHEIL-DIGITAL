import datetime
import os
from config import project_path

base_feed_path = f'{project_path}/src/scripts/data'
providers = ['Facebook','Criteo', 'Google', 'AWIN', 'KuantoKusta']
run = os.system

if __name__ == '__main__':
    begin_time = datetime.datetime.now()
    print(datetime.datetime.now())
   
    print('Updating URL dictionary')
    run (f'python3 {base_feed_path}/url/URL_Generator_v2.py')

    for provider in providers:
        print(provider)
        run(f'python3 {base_feed_path}/providers/{provider}Feed_Cheil.py')
   

    print(datetime.datetime.now() - begin_time)