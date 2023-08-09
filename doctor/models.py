from django.db import models
from authentication.models import UserAccount


# Create your models here.

class Department(models.Model):
    department_name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    department_image = models.ImageField(upload_to='images/department/profile/',null=True,blank=True)
    
    def __str__(self):
        return self.department_name

    
    
class DoctorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user__is_doctor=True)
 
class Doctor(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    doctor_profile_image = models.ImageField(upload_to='images/doctor/profiles/', blank=True, null=True)
    objects = models.Manager()  # Default manager
    doctors = DoctorManager()
    


    def __str__(self):
        return self.user.name


class Slots(models.Model):
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.BooleanField(default=True)
    slot_duration = models.IntegerField()
    is_booked = models.BooleanField(default=False)
    
    def __str__(self):
     return str(self.doctor) + " " + str(self.start_time) +" " +str(self.end_time)

class Appointment(models.Model):
    patient = models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    STATUS_CHOICES =(('pending','Pending'),
                     ('approved','Approved'),
                     ('completed','Completed'),
                     ('cancelled','Cancelled'),
                     ('rejected','Rejected'),
                     ('blocked','Blocked'),
                     )
    status = models.CharField(max_length=10,choices= STATUS_CHOICES,default='Pending')
    slot = models.ForeignKey(Slots,on_delete=models.CASCADE)
    
class Booking_Notification(models.Model):
    send_by = models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    sent_to = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    message = models.CharField(max_length=555)
    is_seen = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.send_by.name}: {self.message}"
    

    
    


    
    
    

    