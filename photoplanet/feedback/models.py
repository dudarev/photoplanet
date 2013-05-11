from django.db import models
from django.contrib.auth.models import User


class Feedback(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()
