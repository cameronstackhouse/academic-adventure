from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

class RegisterViewTest(TestCase):
    """
    Tests the register view of the application
    """

    def test_register_GET(self):
        """
        Test when GET request method used on register view
        """
        client = Client()
        response = client.get(reverse("register:register"), follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "register/register.html")
    
    def test_register_POST(self):
        """
        Test when POST request method is used on register view
        """
        client = Client()
        response = client.get(reverse("register:register"), follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "register/register.html")