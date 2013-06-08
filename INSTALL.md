## Custom headline and analytics

If you'd like to use a custom headline in the template you need to add file 
`templates/photoplanet/custom_headline.html` and specify `CUSTOM_HEADLINE = True` in you settings.

To include Google Analytics add
`templates/photoplanet/analytics.html` and specify `INCLUDE_ANALYTICS = True`.


## Loading photos with cron

Adjust necessary paths.

```crontab
* * * * * cd /path/to/manage.py/ && /where/your/envs/photoplanet/bin/python2.7 /path/to/manage.py/manage.py load_photos --settings=photoplanet.settings.correct > /tmp/cronlog.txt 2>&1
```
