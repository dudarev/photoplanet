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
