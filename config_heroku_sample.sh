#!/bin/bash

heroku config:set DJANGO_SETTINGS_MODULE=photoplanet.settings.heroku
heroku config:set INSTAGRAM_CLIENT_ID=YOUR_INSTAGRAM_CLIENT_ID
heroku config:set INSTAGRAM_CLIENT_SECRET=YOUR_INSTAGRAM_CLIENT_SECRET
