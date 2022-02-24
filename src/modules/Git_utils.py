from config import git_branch
import subprocess

class GitOperations(object):
    def __init__(self):
        self.git_branch = git_branch
        # self.version = version
    
    def checkout(self):
        print("Checking out branch")
        subprocess.run(['git','checkout', self.git_branch])

    def pull(self):
        print(f"Pulling from {self.git_branch}")
        subprocess.run(['git', 'pull', 'origin',self.git_branch])

    def add(self,folders):
        print(f'Adding to commit the folders {folders}')
        subprocess.run(['git', 'add']+folders)

    def commit_and_push(self,m='update: new feed daily Cheil execution'):
        print("Commiting to git repository")
        subprocess.run(['git', 'commit', '-m', m])
        print("Pushing to git repository")
        subprocess.run(['git', 'push', 'origin', git_branch])