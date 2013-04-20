# https://docs.djangoproject.com/en/1.5/topics/http/views/
from django.shortcuts import render_to_response


def home(request):
    return render_to_response('photoplanet/index.html')
