from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    type = models.TextField(null=True)
    preferred_avatar = models.IntegerField(null=True, default=1)
    preferred_language = models.TextField(null=True, default='English')

    class Meta:
        db_table = 'auth_user'