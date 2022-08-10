from django.test import TestCase
from .models import user

# Create your tests here.


class AuthenticationModelTests(TestCase):
    # @classmethod
    # def setUpTestData(cls):
    #     cls.

    def test_user_str(self):
        test_user=user.objects.create(username="username")
        self.assertEqual(str(test_user), "username")

    def test_create_user(self):
        test_user1=user.objects.create_user("user1", "password1")
        self.assertIsInstance(test_user1,user)
        self.assertFalse(test_user1.is_superuser)
        self.assertEqual(test_user1.username, "user1")

        
    def test_create_user_raise_error(self):
        self.assertRaises(ValueError, user.objects.create_user,username="")
        print("-->",self.assertRaises(ValueError, user.objects.create_user,username="",password="password1"))

    def test_create_superuser(self):
        test_superuser=user.objects.create_superuser("user1", "password1")
        self.assertIsInstance(test_superuser,user)
        self.assertTrue(test_superuser.is_superuser)
        self.assertEqual(test_superuser.username, "user1")
