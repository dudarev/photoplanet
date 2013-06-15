"""
https://github.com/dnerdy/factory_boy
"""

import factory
from datetime import datetime

from django.utils.timezone import utc
from django.test import TestCase
from django.core.urlresolvers import reverse

from models import Photo


class PhotoFactory(factory.Factory):
    FACTORY_FOR = Photo

    id = factory.Sequence(lambda n: '{}'.format(n))
    username = 'user1'
    user_avatar_url = 'http://example.com/avatar.jpg'
    photo_url = 'http://example.com/photo.jpg'
    created_time = datetime.utcnow().replace(tzinfo=utc)
    like_count = 1
    vote_count = 0


class PhotosTest(TestCase):
    def setUp(self):
        self.all_url = reverse('all')

    def test_all_photos_view_has_latest_photo_url(self):
        """
        Tests that latest photo url is in the all photos view.
        """
        photo = PhotoFactory.create()
        photo.save()
        response = self.client.get(self.all_url)
        self.assertTrue(photo.photo_url in response.content)

    def test_all_photos_view_has_plus_two(self):
        """
        Tests that +2 is in the all photos view.
        """
        response = self.client.get(self.all_url)
        self.assertTrue('+2' in response.content)
