from django.test import TestCase, Client

# Create your tests here.
class TestHomePage(TestCase):
    def setUp(self):
        self.client = Client()

    def response_is_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)