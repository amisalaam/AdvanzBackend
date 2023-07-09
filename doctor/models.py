from django.db import models
from authentication.models import UserAccount


# Create your models here.

class Department(models.Model):
    department_name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    department_image = models.ImageField(upload_to='images/department/profile/',null=True,blank=True)
    
    
class Doctor(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, primary_key=True)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    doctor_profile_image = models.ImageField(upload_to='images/doctor/profiles/', blank=True, null=True)


    def __str__(self):
        return self.user.email
    

    