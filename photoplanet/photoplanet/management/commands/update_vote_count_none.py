from django.core.management.base import BaseCommand

from photoplanet.models import Photo


class Command(BaseCommand):
    help = "Upate None for vote_count for all photos to be 0."

    def handle(self, *args, **options):
        print "Updating vote_count from None to 0"
        Photo.objects.filter(vote_count=None).update(vote_count=0)
