# https://docs.djangoproject.com/en/1.5/howto/custom-management-commands/
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.timezone import utc
from django.utils.encoding import force_text
from instagram.client import InstagramAPI
import re

from photoplanet.models import Photo


class Command(BaseCommand):
    # args = '<poll_id poll_id ...>'
    help = 'Loads recent photos'

    def handle(self, *args, **options):
        # raise CommandError('Some error.')
        api = InstagramAPI(
            client_id=settings.INSTAGRAM_CLIENT_ID,
            client_secret=settings.INSTAGRAM_CLIENT_SECRET)
        search_result = api.tag_recent_media(
            settings.MEDIA_COUNT,
            settings.LARGE_MEDIA_MAX_ID,
            settings.MEDIA_TAG
        )
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
#                p.caption = m.caption
                tmp = force_text(m.caption, encoding='utf-8')
                p.caption =  re.sub(r'([^\s])#', r'\1 #', tmp)
                p.created_time = m.created_time.replace(tzinfo=utc)
                p.like_count = m.like_count
                p.save()
                is_like_count_updated = True
            info = ''
            info += '{id}\n{username}\n{avatar_url}\n{photo_url}\n'.format(
                id=m.id,
                username=m.user.username,
                avatar_url=m.user.profile_picture,
                photo_url=m.images['standard_resolution'].url
            )
            info += '\n{caption}\n{created_time}\n{like_count}\n{is_created}\n{is_like_count_updated}\n'.format(
                caption="caption",
		created_time=m.created_time,
                like_count=m.like_count,
                is_created=is_created,
                is_like_count_updated=is_like_count_updated
            )
            info += 40 * '-'
            p.update_vote_prediction()
            self.stdout.write(info)
