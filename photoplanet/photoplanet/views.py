# https://docs.djangoproject.com/en/1.5/topics/http/views/
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

from instagram.client import InstagramAPI


LARGE_MEDIA_MAX_ID = 100000000000000000
MEDIA_COUNT = 20
MEDIA_TAG = 'donetsk'


def home(request):
    return render(request, 'photoplanet/index.html')


def _img_tag(s):
    return '<img src="{}"/>'.format(s)


def load_photos(request):

    api = InstagramAPI(
        client_id=settings.INSTAGRAM_CLIENT_ID,
        client_secret=settings.INSTAGRAM_CLIENT_SECRET)
    search_result = api.tag_recent_media(MEDIA_COUNT, LARGE_MEDIA_MAX_ID, MEDIA_TAG)
    info = ''
    # list of media is in the first element of the tuple
    for m in search_result[0]:
        info += '<li>{} {} {} {} {} {}</li>'.format(
            m.id,
            m.user.username,
            _img_tag(m.user.profile_picture),
            _img_tag(m.images['standard_resolution'].url),
            m.created_time,
            m.like_count)

    html = "<html><body><ul>{}</ul></body></html>".format(info)
    return HttpResponse(html)
