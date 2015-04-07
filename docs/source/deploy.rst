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

Create a new droplet in `DigitalOcean`_ and install Ubuntu 14.04.

Generate your SSH Public Key and add it to the droplet::

    ssh-keygen -t rsa -b 4096
    cat id_rsa.pub | ssh user@droplet_ip "cat >> ~/.ssh/authorized_keys"


Install Ansible locally (see `Ansible Docs`_ for more details).
To install on Ubuntu you may follow the guide from DigitalOcean 
"`How to Install and Configure Ansible on an Ubuntu 12.04 VPS`_"::

    sudo apt-get update
    sudo apt-get install python-software-properties
    sudo add-apt-repository ppa:rquillo/ansible
    sudo apt-get update
    sudo apt-get install ansible

Get ansible config files::

    mkdir deploy
    cd deploy/
    apt-get install git
    git clone https://github.com/dudarev/photoplanet.git
    cd photoplanet
    git checkout --track origin/dev
    cd dev/

Make sure that the following two files exists and are modified::
    
    cp hosts.sample hosts
    cp env_vars/dev.sample.yml env_vars/dev.yml    

In ``hosts`` you need to specify IP address of the server on which to deploy.
See `Ansible Docs Hosts and Groups <http://docs.ansible.com/intro_inventory.html>`__ for more details.

In the file ``env_vars/dev.yml`` you need to set secret variables.

Deploy PhotoPlanet on you DigitalOcean server::
    
    ansible-playbook vagrant.yml -i hosts


After installation log into the droplet via ssh and it is necessary to set some variables::

    su photoplanet
    cd /home/photoplanet/photoplanet/photoplanet/photoplanet/settings/

Copy file ``secret.sample.py`` to ``secret.py`` and update the following variables:
``DB_NAME``, ``DB_USER``, ``DB_PASSWORD``, ``SECRET_KEY``. Use the values you used in
``env_vars/dev.yml`` above.

Similarly, copy file ``instagram.sample.py`` to ``instagram.py`` and set variables:
``INSTAGRAM_CLIENT_ID`` and ``INSTAGRAM_CLIENT_SECRET``.

Sync and migrate the database::
	
    cd /home/photoplanet/venv
    source bin/activate
    cd ../photoplanet/photoplanet
    ./manage.py syncdb --settings=photoplanet.settings.web
    ./manage.py migrate --settings=photoplanet.settings.web

And restart uwsgi::

    killall -9 uwsgi
    sudo uwsgi --ini /etc/uwsgi/apps-enabled/django.ini


.. _DigitalOcean: https://www.digitalocean.com/
.. _Ansible Docs: http://docs.ansible.com/intro_installation.html
.. _How to Install and Configure Ansible on an Ubuntu 12.04 VPS: https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-ansible-on-an-ubuntu-12-04-vps
