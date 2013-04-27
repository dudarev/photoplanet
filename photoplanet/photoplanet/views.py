# https://docs.djangoproject.com/en/1.5/topics/http/views/
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

from instagram.client import InstagramAPI

from .models import Photo


LARGE_MEDIA_MAX_ID = 100000000000000000
MEDIA_COUNT = 20
MEDIA_TAG = 'donetsk'


def home(request):
    return render(request, 'photoplanet/index.html')


def all(request):
    photos = Photo.objects.order_by('-created_time').all()[:10]
    return render(request, 'photoplanet/all.html', {'photos': photos})


def _img_tag(s):
    return '<img src="{}"/>'.format(s)


def load_photos(request):
    """
    Loads photos from Instagram and populates database.
    """

    api = InstagramAPI(
        client_id=settings.INSTAGRAM_CLIENT_ID,
        client_secret=settings.INSTAGRAM_CLIENT_SECRET)
    search_result = api.tag_recent_media(MEDIA_COUNT, LARGE_MEDIA_MAX_ID, MEDIA_TAG)
    info = ''
    # list of media is in the first element of the tuple
    for m in search_result[0]:
        p, is_created = Photo.objects.get_or_create(
            id=m.id, username=m.user.username)
        is_like_count_updated = False
        if not p.like_count == m.like_count:
            p.username = m.user.username
            p.user_avatar_url = m.user.profile_picture
            p.photo_url = m.images['standard_resolution'].url
            p.created_time = m.created_time
            p.like_count = m.like_count
            p.save()
            is_like_count_updated = True
        info += '<li>{} {} {} {} {} {} {} {}</li>'.format(
            m.id,
            m.user.username,
            _img_tag(m.user.profile_picture),
            _img_tag(m.images['standard_resolution'].url),
            m.created_time,
            m.like_count,
            is_created,
            is_like_count_updated
        )

    html = "<html><body><ul>{}</ul></body></html>".format(info)
    return HttpResponse(html)
