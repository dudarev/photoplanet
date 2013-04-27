from django.db import models


class Photo(models.Model):
    # it is set by default by Django, but we need modified version
    # https://docs.djangoproject.com/en/1.5/topics/db/models/#automatic-primary-key-fields
    id = models.CharField(primary_key=True, max_length=100)
    username = models.CharField(max_length=100)
    user_avatar_url = models.URLField()
    photo_url = models.URLField()
    created_time = models.DateTimeField()
    like_count = models.IntegerField()
