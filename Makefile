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
	PYTHONPATH=$(PYTHONPATH) \
	DJANGO_SETTINGS_MODULE=photoplanet.settings.test \
	coverage run --source=$(PROJECT_NAME) $(PROJECT_NAME)/manage.py test $(PROJECT_NAME)
	coverage html

load_photos:
	$(MANAGE) load_photos --settings=photoplanet.settings.local

serve_coverage:
	@echo "Browse to http://localhost:4567/"
	@cd htmlcov; \
	python -m SimpleHTTPServer 4567
