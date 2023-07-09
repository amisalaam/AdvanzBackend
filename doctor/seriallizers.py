from rest_framework import serializers
from .models import Doctor



class DoctorDetailsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name', read_only=True)
    class Meta:
        model = Doctor
        fields =['user','name','department','profile_image']
