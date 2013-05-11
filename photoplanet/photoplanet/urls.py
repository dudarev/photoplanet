from django.conf.urls import include, patterns, url
from django.conf import settings

from .views import (
    HomePhotosListView, AllPhotosListView, PhotoDetailView)

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    'photoplanet.views',
    url(r'^$', HomePhotosListView.as_view(), name='home'),
    url(r'^all/$', AllPhotosListView.as_view(), name='all'),
    url(r'^photo/(?P<pk>\w+)/$', PhotoDetailView.as_view(), name='photo-detail'),
    url(r'^load_photos/$', 'load_photos', name='load_photos')
)

urlpatterns += patterns(
    '',
    url(r'^feedback/', include('feedback.urls')),
    url(r'', include('users.urls')),
    url(r'', include('social_auth.urls')),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout')
)

# http://stackoverflow.com/questions/9047054/heroku-handling-static-files-in-django-app
# TODO: needs to be removed this is temporary to have static served from HEROKU
urlpatterns += patterns(
    '',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),
)
