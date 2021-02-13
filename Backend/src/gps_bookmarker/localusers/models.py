from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db.models import BooleanField

# Create your models here.
class LocalUser(AbstractUser):
       premium = models.BooleanField(default=False)
