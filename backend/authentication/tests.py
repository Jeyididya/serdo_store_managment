from django.test import TestCase ,Client
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
        # print("-->",self.assertRaises(ValueError, user.objects.create_user,username="",password="password1"))

    def test_create_superuser(self):
        test_superuser=user.objects.create_superuser("user1", "password1")
        self.assertIsInstance(test_superuser,user)
        self.assertTrue(test_superuser.is_superuser)
        self.assertEqual(test_superuser.username, "user1")





import authentication.schema as authentication_schema
import graphene
from django.contrib.auth import authenticate, login



class AuthenticationCreateUserTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.schema = graphene.Schema(query=authentication_schema.userQuery, mutation=authentication_schema.authMutation)


    def test_mutate(self):
        result=self.schema.execute(
        """
             mutation{
               createUser(email:"user@example.com" password:"password" username:"user1"){
             		user{
                   id,
                   username,
                   email,
                   password,    
                 }    
               }
            }
        """)
        # print("<->",result.data['createUser']['user']['id'])
        self.assertTrue(result.data['createUser']['user']['username']=="user1")
        self.assertTrue(result.data['createUser']['user']['email']=="user@example.com")

  
    

class AuthenticationUserQueryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client=Client()
        # cls.test_superuser=user.objects.create_superuser("admin", "admin")
        # cls.client.force_login(user.objects.create_superuser(username='admin',password="admin"))
        cls.schema = graphene.Schema(query=authentication_schema.userQuery, mutation=authentication_schema.authMutation)
        cls.result=cls.schema.execute(
        """
             mutation{
               createUser(email:"user@example.com" password:"password" username:"user1"){
             		user{
                   id,
                   username,
                   email,
                   password,    
                 }    
               }
            }
        """)


    def test_resolve_users(self):
        users_result=self.schema.execute(
        """
            query{
                users{
                    username
                    email
                    isActive
                }
            }
        """)
        # print("++",users_result.data['users'])
        self.assertTrue(users_result.data['users'][0]['username']=="user1")
        self.assertTrue(users_result.data['users'][0]['email']=="user@example.com")
        self.assertTrue(users_result.data['users'][0]['isActive']==True)

    
    def test_resolve_me(self):
        # c=Client()
        # log=c.login(username="user1",password="password")
        # print(">>>>>>>>>>>>",log,"<<<<<<<<<<<<<<<<<<<")
        me_result=self.schema.execute(
        """
            query{
                me{
                    username,
                    email,
                    isActive,
                }   
            }
        """
        )
        print("<><><> ",me_result.data)
        



# class CreateUserGrapheneTest(TestCase):
    