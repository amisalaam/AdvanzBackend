from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserAccount
User = get_user_model()


class UserCreateSerializernew(UserCreateSerializer):
    class Meta:
        model = UserAccount
        fields = ['id','email','name','is_superuser','is_doctor','is_staff','is_active']
        


class GetAllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('id','email','name','is_superuser','is_doctor','is_staff','is_active')


class DoctorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ( 'email', 'name', 'password')
        
        
    def create(self, validated_data):
        password = validated_data.pop('password') 
        user = UserAccount.objects.create_doctor(password=password, **validated_data)
        return user




        
        




