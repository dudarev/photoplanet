# https://docs.djangoproject.com/en/1.5/topics/http/views/
from instagram.client import InstagramAPI

from django.conf import settings
from django.http import HttpResponse, Http404
from django.views.decorators import csrf
from django.views.generic import ListView, DetailView
from django.views.generic.edit import BaseUpdateView
from django.views.generic.dates import DayArchiveView, TodayArchiveView
from django.utils import decorators

from braces.views import JSONResponseMixin, LoginRequiredMixin

from .models import Photo, Vote


# https://github.com/mitar/django-missing/blob/master/missing/views.py#L7
class EnsureCsrfCookieMixin(object):
    """
    Mixin for Django class-based views which forces a view to send the CSRF cookie.
    """
    @decorators.method_decorator(csrf.ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(EnsureCsrfCookieMixin, self).dispatch(*args, **kwargs)


class HomePhotosListView(EnsureCsrfCookieMixin, TodayArchiveView):
    # as template photo_archive_day.html is used since this is archive view
    queryset = Photo.objects.order_by('-vote_count', '-vote_prediction').all()
    date_field = "created_time"
    allow_empty = True
    paginate_by = settings.PHOTOS_PER_PAGE
    context_object_name = 'photos'


class UserPhotosListView(EnsureCsrfCookieMixin, ListView):
    model = Photo
    queryset = Photo.objects.filter().order_by('-created_time').all()
    template_name = 'photoplanet/user_photos.html'
    context_object_name = 'photos'  # default is object_list
    paginate_by = settings.PHOTOS_PER_PAGE

    def get_queryset(self):
        return Photo.objects.filter(username=self.kwargs['username']).order_by('-created_time')

    def get_context_data(self, **kwargs):
        context = super(UserPhotosListView, self).get_context_data(**kwargs)
        context['username'] = self.kwargs['username']
        return context


class AllPhotosListView(EnsureCsrfCookieMixin, ListView):
    model = Photo
    queryset = Photo.objects.order_by('-created_time').all()
    template_name = 'photoplanet/all.html'  # default is app_name/model_list.html
    context_object_name = 'photos'  # default is object_list
    paginate_by = settings.PHOTOS_PER_PAGE


class VotePhotosListView(LoginRequiredMixin, AllPhotosListView):
    def get_queryset(self):
        return Photo.objects.exclude(
            id__in=Vote.objects.filter(
                user_id=self.request.user.id).values_list('photo_id', flat=True)
        ).order_by('-created_time')


class PhotoDetailView(EnsureCsrfCookieMixin, DetailView):
    model = Photo


class PhotoDayArchiveView(EnsureCsrfCookieMixin, DayArchiveView):
    queryset = Photo.objects.order_by('-vote_count', '-vote_prediction').all()
    date_field = "created_time"
    month_format = '%m'
    make_object_list = True
    allow_empty = True
    paginate_by = settings.PHOTOS_PER_PAGE


# http://django-braces.readthedocs.org/en/latest/#jsonresponsemixin
class PhotoVoteView(JSONResponseMixin, BaseUpdateView):
    model = Photo

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        photo = self.get_object()
        user = self.request.user

        if user.is_authenticated():

            vote_type = request.POST.get('vote_type', '')
            vote_value = int(vote_type)

            vote = Vote(user=user, photo=photo, vote_value=vote_value)
            vote.save()
            # load the object again because it was changed by vote.save()
            photo = self.get_object()

            context_dict = {
                'username': photo.username,
                'your_username': user.username,
                'vote_type': vote_type,
                'vote_count': photo.vote_count,
                'message': 'Vote is updated.',
            }

        else:

            context_dict = {
                'message': 'You must be logged in to vote.',
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
    search_result = api.tag_recent_media(
        settings.MEDIA_COUNT, settings.LARGE_MEDIA_MAX_ID, settings.MEDIA_TAG)
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
