from django.core.management.base import BaseCommand

from photoplanet.models import Photo


class Command(BaseCommand):
    help = "Automatically add some rank based on previous photos"
    args = "<Number of photos to update>"

    def handle(self, *args, **options):
        UPDATE_NUMBER = 200
        if args:
            UPDATE_NUMBER = args[0]
        photos = Photo.objects.order_by('-created_time')[:UPDATE_NUMBER]
        for p in photos:
            print p.username
            p.update_vote_prediction()
