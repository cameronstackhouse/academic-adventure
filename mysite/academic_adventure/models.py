from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Defines a custom user that extends AbstractUser,
    allowing for the built in Django authentication system
    to be used with a specified user account."""

    avatar = models.CharField(max_length=50) #Link to avatar file that the user uses
    intelligence = models.IntegerField(default=0) #Users intelligence score
    sociability = models.IntegerField(default=0) #Users sociability score
    athleticism = models.IntegerField(default=0) #Users athleticism score
    intel_xp = models.FloatField(default=0) #Current xp for intelligence
    soc_xp = models.FloatField(default=0) #Current xp for sociability
    ath_xp = models.FloatField(default=0) #Current xp for athleticism
    points = models.IntegerField(default=0) #Current user points
    gamekeeper = models.BooleanField(default=False) #Boolean indicating if user is a gamekeeper or not

    @property
    def score(self):
        """Function to calculate the users overall
        score, using their attributes"""
        return (self.intelligence + self.sociability + self.athleticism) / 3

    def __str__(self):
        return self.username





