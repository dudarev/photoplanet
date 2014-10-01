Deploy
=======

On Heroku
----------

Assuming you followed :ref:`starting-on-localhost`, check the steps below for starting the web app on Heroku
(see `Getting Started with Django on Heroku <https://devcenter.heroku.com/articles/django>`__ for more details).

Create a new Heroku app::

    heroku create

Rename the app to what seems more appropriate::

    heroku apps:rename newname

Set up the database (for more details see `Heroku documentation <https://devcenter.heroku.com/articles/heroku-postgresql>`__)::

    heroku addons:add heroku-postgresql:dev
    heroku pg:promote YOUR_DATABSE_URL (generated and shown during previous step)

Add necessary settings to environment variables::

    heroku config:add PYTHONPATH=/photoplanet
    heroku config:add DJANGO_SETTINGS_MODULE=photoplanet.settings.heroku

Check a `blog post <http://tomatohater.com/2012/01/17/custom-django-management-commands-on-heroku/>`__ explaining the first command.
See `Django documentation <https://docs.djangoproject.com/en/1.5/topics/settings/#envvar-DJANGO_SETTINGS_MODULE>`__ for using environment variables
to store location of the settings module.

Set up a **different** app at `Instagram developers page <http://instagram.com/developer/clients/register/>`__.
Specify the following parameters there: 
``WEBSITE URL: http://your-app-name.herokuapp.com/`` and ``REDIRECT URI: http://your-app-name.herokuapp.com/complete/instagram/``::

    heroku config:set INSTAGRAM_CLIENT_ID=YOUR_INSTAGRAM_CLIENT_ID
    heroku config:set INSTAGRAM_CLIENT_SECRET=YOUR_INSTAGRAM_CLIENT_SECRET

Sync the database::

    heroku run photoplanet/manage.py syncdb
    heroku run photoplanet/manage.py migrate

Now you can do a simple ``git push`` to deploy the application::

    git push heroku master

Open the app in your browser::

    heroku apps:open

You may want to change search term which is for now is hardcoded in the settings (grep code for ``MEDIA_TAG``).
You need to commit this to master and push to Heroku.
This will change in the future versions.

The simplest approach to update recent photos on Heroku is to use ``cron`` from some external host::

* * * * * curl http://your-app-name.herokuapp.com/load_photos > /tmp/cronlog.txt 2>&1

Heroku has a periodic task scheduler with which you may set up a command similar to what is described at :ref:`loading-photos-with-cron`,
but for that you need to activate payments.

On DigitalOcean 
----------------

Create a new droplet in DigitalOcean and install Ubuntu.
Generating your SSH Public Key and add to the droplet::

    ssh-keygen -t rsa -b 4096
    cat id_rsa.pub | ssh user@droplet_ip "cat >> ~/.ssh/authorized_keys"

Install the local computer Ansible (see `Ansible Docs <http://docs.ansible.com/intro_installation.html>`__ for more details or 
`How to Install and Configure Ansible on an Ubuntu 12.04 VPS <https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-ansible-on-an-ubuntu-12-04-vps>`__)::

    sudo apt-get update
    sudo apt-get install python-software-properties
    sudo add-apt-repository ppa:rquillo/ansible
    sudo apt-get update
    sudo apt-get install ansible

Copy the local computer Ansible config files https://github.com/dudarev/photoplanet/tree/dev/dev

    env_vars
      base.yml
      dev.yml
    roles
      base/tasks
        main.yml
    db
      handlers
        main.yml
      tasks
        main.yml
    web
      handlers
        main.yml
      tasks
        create_user_group.yml
        main.yml
        set_perm.yml
        setup_django_app.yml
        setup_git_repo.yml
        setup_nginx.yml
        setup_uwsgi.yml
        setup_virtualenv.yml
      templates
        django.ini
        photoplanet.conf
      vars
        main.yml
    Vagrantfile
    hosts
    vagrant.yml

In the file host you need to specify ip addresses of the servers on which to deploy.
(see `Ansible Docs Hosts and Groups <http://docs.ansible.com/intro_inventory.html>`__ for more details)
In the file env_vars/dev.yml you need set::


db_user: ""
db_name: ""
db_password:


Deploy PhotoPlanet on you DigitalOcean server::


    ansible-playbook -i vagrant.yml


After installation it is necessary to set some variables.
In file settings/base.py set SECRET_KEY
File settings/instagram.sample.py should be replaced with the file settings/instagram.py set variables::

INSTAGRAM_CLIENT_ID=YOUR_INSTAGRAM_CLIENT_ID
INSTAGRAM_CLIENT_SECRET=YOUR_INSTAGRAM_CLIENT_SECRET

Sync the database::

    manage.py syncdb
    manage.py migrate






