import datetime
from urllib import response

from django.test import TestCase
from django.test.client import Client
from django.utils import timezone
from django.urls import reverse

from .models import Event

class EventModelTest(TestCase):
    """
    Tests for the event model in the database
    """
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


class LoginTest(TestCase):
    """
    Tests for the login view
    """

    def test_login_GET(self):
        """
        Test the login view when the user is not logged in
        """
        client = Client()
        response = client.get("/academic-adventure/login/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_login_success(self):
        """
        Test the login view when the user is logged in.
        Should redirect the user to the home page.
        """
        pass


class HomeViewTest(TestCase):
    """
    Tests for the home view
    """
    
    def test_home_GET(self):
        client = Client()
        response = client.get(reverse("academic_adventure:home"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("home.html")


class MapViewTest(TestCase):
    """
    Tests for the map view
    """

    def test_map_GET(self):
        client = Client()
        response = client.get(reverse("academic_adventure:map"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("map.html")


class LeaderboardViewTest(TestCase):
    """
    Tests for the leaderboard view
    """

    def test_leaderboard_GET(self):
        client = Client()
        response = client.get(reverse("academic_adventure:leaderboard"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("leaderboard.html")

