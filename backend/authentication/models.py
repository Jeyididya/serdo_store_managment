from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from  .permissions import *

# Create your models here.

class user_manager(UserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class user(AbstractUser):
    role_options=("store_manager", "Store Manager"),("store_staff", "Store Staff"),("admin", "Admin"),("finance", "Finance"),("general_manager","General manager"),("purchaser", "Purchaser")
    department_options=("finance", "Finance"),("purchasing", "Purchasing"),("management", "Management"), ("human_resources", "Human Resources")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    role = models.CharField(max_length=30, choices=role_options)
    department=models.CharField(max_length=30, choices=department_options)

    objects=user_manager()

    def __str__(self):
        return self.username

# create_group()