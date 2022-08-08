from pyexpat import model
from django.contrib.auth.models import AbstractUser, UserManager

from django.test import TestCase
from .models import user
from .models import user_manager

# Create your tests here.

# class URLTests(TestCase):
#     def test_home_page(self):
#         response= self.client.get('/')
#         self.assertEqual(response.status_code, 200)


class AuthenticationModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user=user.objects.create(username="username")
        print(cls.test_user.is_superuser)

    def test_model_str(self):
        self.assertEqual(str(self.test_user), "username")

    def test_create_super_user(self):  #not working
        test_user=user_manager.create_user(self, username="user1", password="pass1")
        self.assertTrue(test_user.is_superuser)

