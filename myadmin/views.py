from django.shortcuts import render
from django.contrib.auth import get_user_model
from doctor.models import Doctor
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *

# Create your views here.


# CREATING DOCTOR BY ADMIN

def admin_create_doctor(email, name, password):
    User = get_user_model()
    try:
        user = User.objects.create_doctor(email=email, name=name, password=password)
        print("Doctor created successfully.")
        print(f"Email: {user.email}")
        print(f"Name: {user.name}")
        return user
    except ValueError as e:
        print(str(e))
        return None
    
class GetAllDoctorAPIView(APIView):
    permission_classes= []
    
    def get(self,request):
        objects = Doctor.objects.all()
        serializers = GetAllDoctorsSerializers(objects,many = True)
        return Response(serializers.data)
    



