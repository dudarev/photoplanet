from fabric.api import local
from fabric.api import run, env, cd

env.hosts = ['donetskogram.com']
env.user = 'dudarev'
env.path = '/sites/photoplanet/'

ENV_COMMAND = 'source .env/bin/activate'

 
def push():
    local('git push origin master')  # push local to repository


def pull():
    with cd(env.path):
        run('git pull origin master')
        run('touch /etc/uwsgi/vassals/django.ini')
