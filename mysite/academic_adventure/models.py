import datetime

from django.db import models
from django.utils import timezone
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

class Society(models.Model):
    """Defines a society"""
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    members = models.ManyToManyField(CustomUser, blank=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    """Defines an event in the database"""
    longitude = models.DecimalField(decimal_places=20, max_digits=30)
    latitude = models.DecimalField(decimal_places=20, max_digits=30)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    host = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField()
    duration = models.DecimalField(decimal_places=2, max_digits=6)
    code = models.CharField(max_length=100)
    type = models.CharField(max_length=40)
    society = models.OneToOneField(Society, on_delete=models.CASCADE, null=True, blank=True)
    members = models.ManyToManyField(CustomUser, blank=True, related_name='%(class)s_members_created')

    def recent(self):
        """Function to determine if the event is a recent event
        and should be displayed to the user"""
        #Checks that the date of the event is after the current time and before 2 hours in the future
        return timezone.now() <= self.date <= timezone.now() + datetime.timedelta(hours=2)

    def __str__(self):
        return self.name
