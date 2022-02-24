from Git_utils import GitOperations
from config import project_path, result_path

if __name__ == '__main__':

    try:
        git = GitOperations()
        git.pull()
    except:
        print('Unable/errors pulling from git')


    try:
        git.add([result_path,f'{project_path}/src/dictionaries'])
        git.commit_and_push()
    except:
        print('Unable/errors pushing to git')
        