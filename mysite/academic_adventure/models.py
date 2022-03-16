import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser #Abstract user model to extend


class CustomUser(AbstractUser):
    """
    Defines a custom user that extends AbstractUser,
    allowing for the built in Django authentication system
    to be used with a specified user account with additional attributes.

    Extends AbstractUser to build upon the already existing django user model.
    Allows for CustomUser obejct to be used in the django authentication system
    """

    avatar = models.CharField(max_length=50) #Link to avatar file that the user uses
    intelligence = models.IntegerField(default=0) #Users intelligence score
    sociability = models.IntegerField(default=0) #Users sociability score
    athleticism = models.IntegerField(default=0) #Users athleticism score
    points = models.IntegerField(default=0) #Current user points
    gamekeeper = models.BooleanField(default=False) #Boolean indicating if user is a gamekeeper or not

    @property 
    def score(self):
        """
        Property of a user showing their overall score.
        
        Return:
        Overall user score, average of the three user stats
        """
        return (self.intelligence + self.sociability + self.athleticism) / 3

    def __str__(self):
        """
        String representation of a user.

        Return:
        Users username
        """
        return self.username #Returns a users username


class Society(models.Model):
    """
    Defines a society in the database to represent a society that can set events.

    Extends the Django model class to be stored in the built in Django database.
    """
    name = models.CharField(max_length=50) #Name of the society
    description = models.CharField(max_length=200) #Description of the society
    members = models.ManyToManyField(CustomUser, blank=True) #Members of the society

    def __str__(self):
        """
        String representation of a society

        Return:
        Society name
        """
        return self.name

class Event(models.Model):
    """
    Defines an event in the database to represent an event in the game.
    An event can either be: Academic, Sports, Battle, or Social.
    
    Extends the Django model class to be stored in the built in Django database.
    """
    #Types of events available to be set
    types = (
        ("Battle", "Battle"), 
        ("Academic", "Academic"),
        ("Sports", "Sports"),
        ("Social", "Social"),
    )

    longitude = models.DecimalField(decimal_places=20, max_digits=30) #Longitude location of event
    latitude = models.DecimalField(decimal_places=20, max_digits=30) #Latitude location of event
    name = models.CharField(max_length=100) #Name of the event
    description = models.CharField(max_length=400) #Short description of the event
    host = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True) #Host of the event
    date = models.DateTimeField() #Date and time of the event
    duration = models.DecimalField(decimal_places=2, max_digits=6) #Duration of the event
    code = models.CharField(max_length=100) #Code for the event
    type = models.CharField(
        max_length=40,
        choices=types, #Type of event (battle, academic, sports, social, ...)
    ) 

    #Society is one to one as only one society is associated with an event
    society = models.OneToOneField(Society, on_delete=models.CASCADE, null=True, blank=True) #Society the event belongs to

    #Members is many to many as many users can be members of many events
    members = models.ManyToManyField(CustomUser, blank=True, related_name='%(class)s_members_created') #Members of the event

    def recent(self):
        """
        Function to determine if the event is a recent event
        and should be displayed to the user.
        
        Return:
        Boolean indicating if the current event is between now and two hours in the future
        """
        #Checks that the date of the event is after the current time and before 2 hours in the future
        return timezone.now() <= self.date <= timezone.now() + datetime.timedelta(hours=2)

    def joinable(self):
        """
        Function to check if the event is within a scanable time frame and
        therefore if the event can be joined by a user

        Return:
        Returns a boolean indicating if the event is within a joinable timeframe
        """
        #Checks if the current time is between 10 minutes before the start of the event and 5 minutes after the start of the event
        return self.date - datetime.timedelta(minutes=10) <= timezone.now() <= self.date + datetime.timedelta(minutes=5)

    def __str__(self):
        """
        String representation of an event.

        Return:
        String of the name of the event
        """
        return self.name
