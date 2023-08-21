from django.test import TestCase
from rest_framework.test import APIClient



# Create your tests here.
class UserListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_users(self):
        response = self.client.post('/Todo/')
        self.assertEqual(response.status_code, 200)
        