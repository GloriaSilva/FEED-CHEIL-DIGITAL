import datetime
import os
from config import project_path, result_path
import sys
import argparse
from Git_utils import GitOperations

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

    if args.push:
        git = GitOperations()
        git.pull()

    begin_time = datetime.datetime.now()
    print(datetime.datetime.now())
   
    print('Updating URL dictionary')
    subprocess.run(['python3', f'{base_feed_path}/url/URL_Generator_v2.py', args.country])

    for provider in providers:
        print(f'Generating {provider} feed')
        subprocess.run(['python3', f'{base_feed_path}/providers/{provider}Feed_Cheil.py', args.country])
   
    print(datetime.datetime.now() - begin_time)
    
    if args.push:
        git.commit_and_push()
        

