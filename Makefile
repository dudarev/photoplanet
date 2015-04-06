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

tags:
	ctags -R .

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

rank_photos:
	$(MANAGE) rank_photos 200 --settings=photoplanet.settings.local

serve_coverage:
	@echo "Browse to http://localhost:4567/"
	@cd htmlcov; \
	python -m SimpleHTTPServer 4567

backup:
	$(MANAGE) dbbackup --settings=photoplanet.settings.local

restore:
	$(MANAGE) dbrestore --settings=photoplanet.settings.local

dump_to_json:
	$(MANAGE) dumpdata social_auth > social_auth.json --settings=photoplanet.settings.local
	$(MANAGE) dumpdata photoplanet > photoplanet.json --settings=photoplanet.settings.local 
	$(MANAGE) dumpdata auth > auth.json --settings=photoplanet.settings.local

load_from_json:
	$(MANAGE) loaddata auth.json --settings=photoplanet.settings.local
	$(MANAGE) loaddata social_auth.json --settings=photoplanet.settings.local

	$(MANAGE) loaddata photoplanet.json --settings=photoplanet.settings.local
