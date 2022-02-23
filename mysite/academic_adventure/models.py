from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    avatar = models.CharField(max_length=50)
    score = models.FloatField(default=0)
    intelligence = models.IntegerField(default=0)
    sociability = models.IntegerField(default=0)
    athleticism = models.IntegerField(default=0)
    intel_xp = models.FloatField(default=0)
    soc_xp = models.FloatField(default=0)
    ath_xp = models.FloatField(default=0)
    points = models.IntegerField(default=0)
    gamekeeper = models.BooleanField(default=False)

    def __str__(self):
        return self.username





