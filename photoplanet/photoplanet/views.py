# https://docs.djangoproject.com/en/1.5/topics/http/views/
from datetime import date

from instagram.client import InstagramAPI

from django.http import HttpResponse, Http404
from django.conf import settings
from django.views.generic import ListView, DetailView
from django.views.generic.edit import BaseUpdateView

from braces.views import JSONResponseMixin

from .models import Photo


LARGE_MEDIA_MAX_ID = 100000000000000000
MEDIA_COUNT = 20
MEDIA_TAG = 'donetsk'
PHOTOS_PER_PAGE = 10


class HomePhotosListView(ListView):
    model = Photo
    queryset = Photo.objects.filter(
        created_time__gte=date.today()).order_by('-like_count')[:PHOTOS_PER_PAGE]
    template_name = 'photoplanet/index.html'
    context_object_name = 'photos'


class AllPhotosListView(ListView):
    model = Photo
    queryset = Photo.objects.order_by('-created_time').all()
    template_name = 'photoplanet/all.html'  # default is app_name/model_list.html
    context_object_name = 'photos'  # default is object_list
    paginate_by = 10


class PhotoDetailView(DetailView):
    model = Photo


# http://django-braces.readthedocs.org/en/latest/#jsonresponsemixin
class PhotoVoteView(JSONResponseMixin, BaseUpdateView):
    model = Photo

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = self.request.user
        vote_type = request.POST.get('vote_type', '')

        context_dict = {
            'username': self.object.username,
            'your_username': user.username,
            'vote_type': vote_type,
        }
        
        return self.render_json_response(context_dict)

    
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
