import datetime

from django.test import TestCase
from django.test.client import Client
from django.utils import timezone
from django.urls import NoReverseMatch, reverse

from .models import CustomUser, Event

class EventModelTest(TestCase):
    """
    Tests for the event model in the database.
    Extends the default django TestCase to allow for it to be run as a test
    """
    def event_is_recent_with_future_event(self):
        """
        Tests that recent() returns False for events that are not within
        2 hours in the future

        Keyword arguments:
        self -- test case object for the event model
        """

        time = timezone.now() + datetime.timedelta(hours=3) #Sets a time to be three hours in the future from now
        future_event = Event(date=time) #Creates a new event with this date

        self.assertIs(future_event.recent(), False) #Asserts that the new event is not recent using the recent function
    
    def event_is_recent_with_recent_event(self):
        """
        Tests that recent() returns True for events that are within the next
        2 hours in the future

        Keyword arguments:
        self -- test case object for the event model
        """

        time = timezone.now() + datetime.timedelta(hours=1.5) #Sets a time to be one and a half hours in the future
        current_event = Event(date=time) #Creates a new event with this date
 
        self.assertIs(current_event.recent(), True) #Asserts that the new event is recent using the recent function
    
    def event_is_recent_with_previous_event(self):
        """
        Tests that recent() returns False for events that are in the past

        Keyword arguments:
        self -- test case object for the event model
        """

        time = timezone.now() - datetime.timedelta(hours=0.2) #Sets a time to be 12 minutes in the past
        previous_event = Event(date=time) #Creates a new event with this date

        self.assertIs(previous_event.recent(), False) #Asserts that new event which is in the past is not considered recent
    
    def event_is_recent_with_boundary_event(self):
        """
        Tests that recent() returns True for events exactly 2 hours in the future

        Keyword arguments:
        self -- test case object for the event model
        """

        time = timezone.now() + datetime.timedelta(hours=2) #Sets a time to be 2 hours in the future from now
        current_event = Event(date = time) #Creates a new event with this date

        self.assertIs(current_event.recent(), True) #Asserts that the event is recent
    
    def event_is_joinable(self):
        """
        joinable() should return True if the current time is between 10 minutes before an events start time and 5 minutes after

        Keyword arguments:
        self -- TestCase obejct to allow for the method to be run as a Django test
        """

        time = timezone.now() + datetime.timedelta(minutes=3) #Sets the time to be 3 minutes in the future
        current_event = Event(date=time) #Creates a new event with the date

        self.assertIs(current_event.joinable(), True)  #Asserts that the event is joinable
    
    def event_is_joinable_lower_boundary(self):
        """
        joinable() should return True if the current time is between 10 minutes before an events start time and 5 minutes after.
        This tests the lower boundary (10 mins before).

        Keyword arguments:
        self -- TestCase obejct to allow for the method to be run as a Django test
        """

        time = timezone.now() - datetime.timedelta(minutes=10) #Sets the time to be 10 minutes in the past
        current_event = Event(date=time) #Creates a new event with the date

        self.assertIs(current_event.joinable(), True) #Asserts that the event is joinable
    
    def event_is_joinable_upper_boundary(self):
        """
        joinable() should return True if the current time is between 10 minutes before an events start time and 5 minutes after.
        This tests the upper boundary (5 mins after the start).

        Keyword arguments:
        self -- TestCase obejct to allow for the method to be run as a Django test
        """

        time = timezone.now() + datetime.timedelta(minutes=5) #Sets the time to be 5 minutes in the future
        current_event = Event(date=time) #Creates a new event with the date

        self.assertIs(current_event.joinable(), True) #Asserts that the event is joinable
    
    def event_is_joinable_invalid_lower(self):
        """
        joinable() should return false if the event is too far in the past

        Keyword arguments:
        self -- TestCase obejct to allow for the method to be run as a Django test
        """
        time = timezone.now() - datetime.timedelta(minutes=11) #Sets the time to be 11 minutes in the past
        current_event = Event(date=time) #Creates a new event with the date

        self.assertIs(current_event.joinable(), False) #Asserts that the event is not joinable
    
    def event_is_joinable_invalid_higher(self):
        """
        joinable() should return false if the event is too far in the future

        Keyword arguments:
        self -- TestCase obejct to allow for the method to be run as a Django test
        """
        time = timezone.now() + datetime.timedelta(minutes=6) #Sets the time to be 6 minutes in the future
        current_event = Event(date=time) #Creates a new event with the date

        self.assertIs(current_event.joinable(), False) #Asserts that the event is not joinable
    
    def event_is_joinable_past_day(self):
        """
        joinable() should return false if the event is on another day in the past

        Keyword arguments:
        self -- TestCase obejct to allow for the method to be run as a Django test
        """
        time = timezone.now() - datetime.timedelta(days=1) #Sets the time to be one day in the past
        current_event = Event(date=time) #Creates a new event with the date

        self.assertIs(current_event.joinable(), False) #Asserts that the event is not joinable
    
    def event_is_joinable_future_day(self):
        """
        joinable() should return false if the event is on another day in the future

        Keyword arguments:
        self -- TestCase obejct to allow for the method to be run as a Django test
        """
        time = timezone.now() + datetime.timedelta(days=1) #Sets the time to be one day in the future
        current_event = Event(date=time) #Creates a new event with the date

        self.assertIs(current_event.joinable(), False) #Asserts that the event is not joinable

class LoginTest(TestCase):
    """
    Tests for the login view.
    Extends the default django TestCase to allow for it to be run as a test
    """

    def test_login_GET(self):
        """
        Test the login view when the user is not logged in

        Keyword arguments:
        self -- test case object for the login view
        """
        client = Client() 
        response = client.get("/academic-adventure/login/") #Client tries to access the login page with a get request

        self.assertEqual(response.status_code, 200) #Assert that the client could successfully access the page
        self.assertTemplateUsed(response, "registration/login.html") #Assert that the html template used is correct

    def test_login_success(self):
        """
        Test the login view when the user is logged in.
        Should redirect the user to the home page.

        Keyword arguments:
        self -- test case object for the login view
        """
        client = Client()
        response = client.post("/academic-adventure/login/", follow=True) #Client tries to access the login page with a post request

        self.assertEqual(response.status_code, 200) #Assert that the client could successfully access the page
        self.assertTemplateUsed("home.html") #Assert that the html template used is correct


class HomeViewTest(TestCase):
    """
    Tests for the home view.
    Extends the default django TestCase to allow for it to be run as a test
    """
    
    def test_home_GET(self):
        """
        Tests a GET request for the homepage, should return and render
        home.html

        Keyword arguments:
        self -- test case object for the home view
        """
        client = Client()
        response = client.get(reverse("academic_adventure:home"), follow=True) #Client tries to access the home page using a get request

        self.assertEqual(response.status_code, 200) #Assert that the client could successfully access the page
        self.assertTemplateUsed("home.html") #Assert that the html template used is correct


class EventsViewTest(TestCase):
    """
    Tests for the map view.
    Extends the default django TestCase to allow for it to be run as a test
    """

    def test_events_GET(self):
        """
        Tests GET method on map view. Should return the map.html page

        Keyword arguments:
        self -- test case object for the events view
        """
        client = Client()
        response = client.get(reverse("academic_adventure:events"), follow=True) #Client tries to access the events page using a get request

        self.assertEqual(response.status_code, 200) #Assert that the client could successfully access the page
        self.assertTemplateUsed("events.html") #Assert that the html template used is correct


class LeaderboardViewTest(TestCase):
    """
    Tests for the leaderboard view.
    Extends the default django TestCase to allow for it to be run as a test
    """

    def test_leaderboard_GET(self):
        """
        Tests the GET method on the leaderboard view.
        Should return the leaderboard.html page

        Keyword arguments:
        self -- test case object for the leaderboard view       
        """
        client = Client()
        response = client.get(reverse("academic_adventure:leaderboard"), follow=True) #Client tries to access the leaderboard page using a get request

        self.assertEqual(response.status_code, 200) #Assert that the client could successfully access the page
        self.assertTemplateUsed("leaderboard.html") #Assert that the html template used is correct


class CreateViewTest(TestCase):
    """
    Tests the create view which allows gamekeepers to create events.
    Extends the default django TestCase to allow for it to be run as a test
    """

    def test_create_GET(self):
        """
        Tests the GET method on the create view. Should return the
        create.html page

        Keyword arguments:
        self -- test case object for the create view
        """
        client = Client()
        response = client.get(reverse("academic_adventure:create"), follow=True) #Client tries to access the create page using a get request

        self.assertEqual(response.status_code, 200) #Assert that the client could successfully access the page
        self.assertTemplateUsed("create.html") #Assert that the html template used is correct

    def test_create_POST(self):
        """
        Tests when the POST method is used on the view. Should redirect the user
        to the code.html page

        Keyword arguments:
        self -- test case object for the create view
        """
        client = Client()
        response = client.post(reverse("academic_adventure:create"), follow=True) #Client tries to access the create page using a post request

        self.assertEqual(response.status_code, 200) #Assert that the client could successfully access the page
        self.assertTemplateUsed("code.html") #Assert that the html template used is correct


class ScanViewTest(TestCase):
    """
    Tests the scan view which allows a user to scan a QR code to 
    join an event.
    Extends the default django TestCase to allow for it to be run as a test
    """

    def test_scan_GET(self):
        """
        Tests when the GET method is used on the scan view

        Keyword arguments:
        self -- test case object for the scan view
        """
        client = Client()
        response = client.get(reverse("academic_adventure:create"), follow=True) #Client tries to access the scan page using a get request

        self.assertEqual(response.status_code, 200) #Assert that the client could successfully access the page
        self.assertTemplateUsed("scan.html") #Assert that the html template used is correct
    
    def test_scan_POST(self):
        """
        Tests the POST method on the scan view

        Keyword arguments:
        self -- test case object for the scan view
        """
        client = Client()

        response = client.post(reverse("academic_adventure:create"), follow=True) #Client tries to access the scan page using a post request

        self.assertEqual(response.status_code, 200) #Assert that the client could successfully access the page
        self.assertTemplateUsed("scan.html") #Assert that the html template used is correct


class BattleViewTest(TestCase):
    """
    Tests the battle view which allows a user to battle against 
    a random user from the database scaled to the users level.
    Extends the default django TestCase to allow for it to be run as a test
    """

    def test_battle_GET(self):
        """
        Tests when the GET method is used on the battle view

        Keyword arguments:
        self -- test case object for the battle view
        """
        client = Client()

        response = client.get(reverse("academic_adventure:battle"), follow=True) #Client tries to access the battle page using a post request

        self.assertEqual(response.status_code, 200) #Assert that the client could successfully access the page
        self.assertTemplateUsed("battle.html") #Assert that the html template used is correct


class CodeViewTest(TestCase):
    """
    Tests the code view which displays a code to join an event.
    Extends the default django TestCase to allow for it to be run as a test
    """
    def test_code_GET(self):
        """
        Tests when the GET method is used on the code view

        Keyword arguments:
        self -- test case object for the code view
        """
        client = Client()

        #Creates a gamekeeper to set an event
        gamekeeper = CustomUser.objects.create(avatar="", intelligence=0, sociability=0, athleticism=0, points=0, gamekeeper=True)
        #Creates an event
        event = Event.objects.create(longitude=0, latitude=0, name="Test", description="Test", host=gamekeeper, date=timezone.now(), duration=1.2, code="a", type="Battle")
        event_number = event.id

        #Tries to get the QR code associated with the event in the code view
        response = client.get(reverse("academic_adventure:code", kwargs={"event_id":event_number}), follow=True)

        self.assertEqual(response.status_code, 200) #Assert that the client could successfully access the page
        self.assertTemplateUsed("code.html") #Assert that the html template used is correct
    
    def test_code_invalid_GET(self):
        """
        Tests the code view with an invalid code ID passed into it.

        Keyword arguments:
        self -- test case object for the code view
        """
        client = Client()

        try:
            #Trues to get the view with an invalid event code
            response = client.get(reverse("academic_adventure:code", kwargs={"event_id":"a"}), follow=True)
            self.fail #If succeeds then fail the test
        except NoReverseMatch:
            pass
