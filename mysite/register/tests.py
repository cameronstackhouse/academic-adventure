from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

class RegisterViewTest(TestCase):
    """
    Tests the register view of the application

    Extends the TestCase class to allow for the methods inside of the class
    to be run as Django tests
    """

    def test_register_GET(self):
        """
        Test when GET request method used on register view

        Keyword arguments:
        self -- test case object for the register view
        """
        client = Client()
        response = client.get(reverse("register:register"), follow=True) #Client tries to get registration page

        self.assertEquals(response.status_code, 200) #Assert that a page has successfully been returned to the client
        self.assertTemplateUsed(response, "register/register.html") #Assert that the correct template was displayed
    
    def test_register_POST(self):
        """
        Test when POST request method is used on register view

        Keyword arguments:
        self -- test case object for the register view
        """
        client = Client()
        response = client.post(reverse("register:register"), follow=True) #Client tries to send a post request to registration page

        self.assertEquals(response.status_code, 200) #Assert that a page has successfully been returned to the client
        self.assertTemplateUsed(response, "register/register.html") #Assert that the correct template was displayed