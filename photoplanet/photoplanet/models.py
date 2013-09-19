from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Photo(models.Model):
    """
    Model that holds photo related attributes.
    """
    # it is set by default by Django, but we need modified version
    # https://docs.djangoproject.com/en/1.5/topics/db/models/#automatic-primary-key-fields
    id = models.CharField(primary_key=True, max_length=100)
    username = models.CharField(max_length=100)
    user_avatar_url = models.URLField(null=True)
    photo_url = models.URLField(null=True)
    created_time = models.DateTimeField(null=True)
    like_count = models.IntegerField(null=True)
    # vote can be float, fractional part is what is estimated based on previous votes
    # formula used for estimated vote v:
    # 1 / (1 + e^-(v - 0.5))
    # 0.5 is so that if all votes are 0.5 it stays 0.5
    vote_count = models.FloatField(null=True)

    def __unicode__(self):
        return "by {} on {} vote: {}".format(
            self.username,
            datetime.strftime(self.created_time, '%Y-%m-%d'),
            self.vote_count
        )


class Vote(models.Model):
    user = models.ForeignKey(User)
    photo = models.ForeignKey(Photo)
    vote_value = models.IntegerField()
    # vote may be changed, we update the last one
    created_time = models.DateTimeField(auto_now=True)

    def save(self):
        """
        Allow only one vote per user per photo.
        
        Change old vote in database if the same user submits
        another vote for the same photo.
        """
        
        other_votes = Vote.objects.filter(user=self.user, photo=self.photo).all()
        if other_votes and not other_votes[0].pk == self.pk:
            vote = other_votes[0]
            vote.vote_value = self.vote_value
            vote.save()
        else:
            super(Vote, self).save()

        # update vote count for a photo
        Photo.objects.filter(id=self.photo_id).update(
            vote_count=Vote.objects.filter(photo=self.photo).aggregate(
            vote_count=models.Sum('vote_value'))['vote_count'])
