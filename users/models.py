from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
  following = models.ManyToManyField(
    "self", related_name='followers', symmetrical=False
    ) # symmetrical 대칭 기능
