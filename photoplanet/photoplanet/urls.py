from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'photoplanet.views.home', name='home'),
    url(
        r'^all/',
        TemplateView.as_view(template_name="photoplanet/all.html"),
        name='all'),
    url(r'^feedback/', include('feedback.urls'))
)

# http://stackoverflow.com/questions/9047054/heroku-handling-static-files-in-django-app
# TODO: needs to be removed this is temporary to have static served from HEROKU
urlpatterns += patterns(
    '',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),
)
