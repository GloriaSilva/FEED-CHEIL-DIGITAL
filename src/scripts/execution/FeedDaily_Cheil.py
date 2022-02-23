import datetime
import os
from config import project_path, result_path
import subprocess
import sys
import argparse

base_feed_path = f'{project_path}/src/scripts/data'
providers = ['Facebook','Criteo', 'Google', 'AWIN', 'KuantoKusta']


def get_args():
    parser = argparse.ArgumentParser(description='Daily Cheil feed generation')
    parser.add_argument('country', type=str,
                    help='String with the code for a country')
    parser.add_argument('--push', action='store_true',
                    help='Flag to push to git repository')

    return parser.parse_args()


if __name__ == '__main__':

    args = get_args()

    begin_time = datetime.datetime.now()
    print(datetime.datetime.now())
   
    print('Updating URL dictionary')
    subprocess.run(['python3', f'{base_feed_path}/url/URL_Generator_v2.py', args.country])

    for provider in providers:
        print(f'Generating {provider} feed')
        subprocess.run(['python3', f'{base_feed_path}/providers/{provider}Feed_Cheil.py', args.country])
   
    print(datetime.datetime.now() - begin_time)
    
    if args.push:
        print("Adding to git commit")
        subprocess.run(['git','add', result_path, f'{project_path}/src/dictionaries'])
        print("Commiting to git repository")
        subprocess.run(['git', 'commit', '-m', 'update: new feed daily Cheil execution'])
        print("Pushing to git repository")
        subprocess.run(['git', 'push', 'origin', 'main'])

