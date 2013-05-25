from django.db import models
from django.contrib.auth.models import User


class Feedback(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "Feedback from".format(self.user.username)
