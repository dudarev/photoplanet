from math import exp

from django.core.management.base import BaseCommand
from django.db.models import Avg

from photoplanet.models import Photo


class Command(BaseCommand):
    help = 'Automatically add some rank based on previous photos'

    def handle(self, *args, **options):
        photos = Photo.objects.filter(vote_count=None).order_by('-created_time')
        for p in photos:
            print p.username
            print Photo.objects.filter(username=p.username)
            vote_avg = Photo.objects.filter(username=p.username).aggregate(
                Avg('vote_count'))['vote_count__avg']
            if vote_avg is None:
                vote_avg = 0.5
            vote_scaled = 1. / (1. + exp(0.5 - vote_avg))
            p.vote_count = vote_scaled
            p.save()
