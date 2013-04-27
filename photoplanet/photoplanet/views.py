# https://docs.djangoproject.com/en/1.5/topics/http/views/
from django.shortcuts import render


def home(request):
    return render(request, 'photoplanet/index.html')
