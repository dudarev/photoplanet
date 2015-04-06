from datetime import datetime

from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User
from django.utils.encoding import force_text



class Photo(models.Model):
    """
    Model that holds photo related attributes.
    """
    # it is set by default by Django, but we need modified version
    # https://docs.djangoproject.com/en/1.5/topics/db/models/#automatic-primary-key-fields
    id = models.CharField(primary_key=True, max_length=100)
    username = models.CharField(max_length=100)
    user_avatar_url = models.URLField(null=True)
    caption = models.TextField(null=True)
    photo_url = models.URLField(null=True)
    created_time = models.DateTimeField(null=True)
    like_count = models.IntegerField(null=True)
    vote_count = models.IntegerField(null=False, default=0)
    
    # formula used for estimation:
    # likes * votes_avg / likes_avg
    # it is float to have better precision
    vote_prediction = models.FloatField(null=True)

    def update_vote_prediction(self):
            vote_avg = Photo.objects.filter(username=self.username).aggregate(
                Avg('vote_count'))['vote_count__avg']
            if vote_avg is None:
                vote_avg = 0
            like_avg = Photo.objects.filter(username=self.username).aggregate(
                Avg('like_count'))['like_count__avg']
            if like_avg is None:
                like_avg = 0
            if like_avg == 0:
                self.vote_prediction = 0
            else:
                self.vote_prediction = self.like_count * vote_avg / like_avg
            self.save()

    def __unicode__(self):
<<<<<<< HEAD
<<<<<<< HEAD
           return "id {} by {} on {} url {}".format(
               self.id,
               self.username,
               datetime.strftime(self.created_time, '%Y-%m-%d %H-%M'),  
               self.photo_url
           )
=======
=======
>>>>>>> f61187e41fa63bab2a367484b130a00a2ab64040
        if self.created_time:
            return "by {} on {} vote: {}".format(
                self.username,
                datetime.strftime(self.created_time, '%Y-%m-%d'),
                self.vote_count
            )
        else:
            return "by {} vote: {}".format(
                self.username,
                self.vote_count
            )
<<<<<<< HEAD
>>>>>>> f61187e41fa63bab2a367484b130a00a2ab64040
=======
>>>>>>> f61187e41fa63bab2a367484b130a00a2ab64040


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
