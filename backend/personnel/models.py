from django.db import models
from PIL import Image
from authentication.models import user

class employeeProfile(models.Model):

    photo = models.ImageField(upload_to='employee_pictures', null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role_options=("store_manager", "Store Manager"),("admin", "Admin"),("sales", "Sales"),("general_manager","General manager"),("purchaser", "Purchaser")
    role = models.CharField(choices=role_options, max_length=50)
    cv = models.FileField(upload_to='employee_cv', max_length=100)
    phone_number = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    user = models.ForeignKey(user, on_delete=models.CASCADE)


    def __str__(self):
        return self.first_name +" "+ self.last_name +" - " + self.role


