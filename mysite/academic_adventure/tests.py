import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Event

class EventModelTest(TestCase):
    def event_is_recent_with_future_event(self):
        """
        recent() returns False for events that are not within
        2 hours in the future.
        """

        time = timezone.now() + datetime.timedelta(hours=3)
        future_event = Event(date=time)

        self.assertIs(future_event.recent(), False)
    
    def event_is_recent_with_recent_event(self):
        """
        recent() returns True for events that are within the next
        2 hours in the future.
        """

        time = timezone.now() + datetime.timedelta(hours=1.5)
        current_event = Event(date=time)

        self.assertIs(current_event.recent(), True)
    
    def event_is_recent_with_previous_event(self):
        """
        recent() returns False for events that are in the past.
        """

        time = timezone.now() - datetime.timedelta(hours=0.2)
        previous_event = Event(date=time)

        self.assertIs(previous_event.recent(), False)
    
    def event_is_recent_with_boundary_event(self):
        """
        recent() returns True for events exactly 2 hours in the future.
        """

        time = timezone.now() + datetime.timedelta(hours=2)
        current_event = Event(date = time)

        self.assertIs(current_event.recent(), True)    

