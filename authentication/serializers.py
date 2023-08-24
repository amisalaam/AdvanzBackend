from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserAccount
from doctor.models import Doctor,Department,Appointment
User = get_user_model()


class UserCreateSerializernew(UserCreateSerializer):
    class Meta:
        model = UserAccount
        fields = ['id','email','name','is_superuser','is_doctor','is_staff','is_active']
        


class GetAllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('id','email','name','is_superuser','is_doctor','is_staff','is_active')






# class DoctorCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Doctor
#         fields = ('user', 'department', 'doctor_profile_image')


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['email', 'name', 'password', 'is_doctor']  # 'is_doctor' added for doctor creation

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['department', 'doctor_profile_image']

        
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'  


class CancelUserAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__' 
        
#DASHBOARD

class PatientAppointmentDataSerializer(serializers.Serializer):
    patient_name = serializers.CharField()
    approved_appointment_count = serializers.IntegerField()
    blocked_appointment_count = serializers.IntegerField()
    rejected_appointment_count = serializers.IntegerField()
    cancelled_appointment_count = serializers.IntegerField()


