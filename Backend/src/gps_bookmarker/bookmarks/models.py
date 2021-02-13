from django.contrib.auth.models import User
from django.db import models
from localusers.models import LocalUser


class Bookmark(models.Model):

    user = models.ForeignKey(LocalUser,related_name='bookmarks', on_delete=models.CASCADE)
    lat = models.CharField(max_length=255)
    lon = models.CharField(max_length=255)
    alt = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
