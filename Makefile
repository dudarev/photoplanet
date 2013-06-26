PROJECT_NAME=photoplanet
PYTHONPATH=$(CURDIR):$(CURDIR)/$(PROJECT_NAME)

MANAGE= PYTHONPATH=$(PYTHONPATH) python $(PROJECT_NAME)/manage.py

runserver:
	$(MANAGE) runserver --settings=photoplanet.settings.local

shell:
	$(MANAGE) shell --settings=photoplanet.settings.local

syncdb:
	$(MANAGE) syncdb --settings=photoplanet.settings.local
	$(MANAGE) migrate --settings=photoplanet.settings.local


# including necessary custom templates if they are not present in the repo
test:
	touch photoplanet/templates/photoplanet/custom_headline.html
	touch photoplanet/templates/photoplanet/analytics.html
	$(MANAGE) test photoplanet --settings=photoplanet.settings.test


load_photos:
	$(MANAGE) load_photos --settings=photoplanet.settings.local
