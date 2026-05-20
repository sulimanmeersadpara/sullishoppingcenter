from django.db import models

from categories.models import gender
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Add your custom fields here
    parent=models.CharField(max_length=100,null=True)
    code = models.CharField(max_length=15,null=True)
    is_verified = models.BooleanField(default=False,null=True)
    gender_id=models.ForeignKey(gender,on_delete=models.CASCADE,related_name='emp_gender_id',null=True)  
    CNIC=models.CharField(max_length=100,null=True)
    job_title=models.CharField(max_length=200,null=True)
    salary=models.IntegerField(default=0,null=True)
    address=models.CharField(max_length=200,null=True)
    nationality=models.CharField(max_length=100,null=True)
    bank_account_number=models.CharField(max_length=100,null=True)
    profile_image=models.ImageField(upload_to='employees_images/',null=True)
    phone=models.CharField(max_length=50,null=True)
    DOB=models.DateField(null=True)
    def __str__(self):
        return self.first_name
