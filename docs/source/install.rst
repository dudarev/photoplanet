Installation
============

Starting on localhost
----------------------------------

Clone repository::

    git clone https://github.com/dudarev/photoplanet.git
    cd photoplanet

You may also just take one of the latest tags `from Github <https://github.com/dudarev/photoplanet/tags>`__.

Create virtualenv and install dependencies. For instance with `virtualenvwrapper`_::

    mkvirtualenv photoplanet
    pip install -r requirements/local.txt

Check that tests pass (this also creates custom headline and analytics files, see section below)::

    make test

Run the commands necessary for creating of the database (see ``Makefile`` for more details).
As of version 0.1 the command creates SQLite database::

    make syncdb

Launch instance of development server with::

    make runserver

Navigate to `http://127.0.0.1:8000/ <http://127.0.0.1:8000/>`__ to see the running site.

Create an app at `Instagram developers page <http://instagram.com/developer/clients/register/>`__.
Specify the following parameters there: 
``WEBSITE URL: http://127.0.0.1:8000/`` and ``REDIRECT URI: http://127.0.0.1:8000/complete/instagram/``.

Copy Instagram settings file and updated variables with what you have obtain from Instagram::

    cp photoplanet/photoplanet/settings/instagram.sample.py photoplanet/photoplanet/settings/instagram.py

At the moment there is a utility view that loads recent photos from Instagram: 
`http://127.0.0.1:8000/load_photos/ <http://127.0.0.1:8000/load_photos/>`__. 
The photos may also be loaded with custom management command::

    make load_photos


Custom headline and analytics
------------------------------

If you'd like to use a custom headline in the template you need to add file 
``templates/photoplanet/custom_headline.html`` and specify ``CUSTOM_HEADLINE = True`` in you settings.

To include Google Analytics add
``templates/photoplanet/analytics.html`` and specify ``INCLUDE_ANALYTICS = True``.


Loading photos with cron
-------------------------

Adjust necessary paths

.. code-block::  crontab

    * * * * * cd /path/to/manage.py/ && /where/your/envs/photoplanet/bin/python2.7 /path/to/manage.py/manage.py load_photos --settings=photoplanet.settings.correct > /tmp/cronlog.txt 2>&1


.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/en/latest/
