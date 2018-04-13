from ConfigParser import ConfigParser
from git import Repo
import re
import os
from time import gmtime, strftime
import getpass
username = getpass.getuser()

def pin_commit_hash(package, config):
    repo = Repo('')
    value = config.get('sources', package)
    value = re.sub('branch=\w+', '',  value)
    value = value + ' ' + 'rev={}'.format(repo.head.object.hexsha)
    config.set('sources', package, value)


def create_sandbox_cfg():
    config = ConfigParser()
    config.read('profiles/sandbox.cfg')
    all_packages = dict(config.items('sources')).keys()
    pwd = os.getcwd()
    for package in all_packages:
        try:
            os.chdir(pwd + '/src/' + package)
            pin_commit_hash(package, config)
            os.chdir(pwd)
        except OSError:
            continue
    with open('profiles/sandbox.cfg', 'w') as fp:
        config.write(fp)
    with open('profiles/sandbox.cfg', 'r') as fp:
        content = fp.read().replace('+ =', '+=')
    with open('profiles/sandbox.cfg', 'w') as fp:
        fp.write("# Autogenerated at ({time}) by {user} \n{content}".format(time=strftime("%Y-%m-%d %H:%M:%S", gmtime()), user=getpass.getuser(), content=content))


if __name__ == '__main__':
    create_sandbox_cfg()