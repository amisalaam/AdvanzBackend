from rest_framework.generics import ListAPIView
from .serializers import UserCreateSerializer,GetAllUserSerializer,DoctorCreateSerializer
from django.shortcuts import render
from django.http import HttpResponse
from .models import UserAccount
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()




# Create your views here.
def Login(request):
    return HttpResponse('Gellooo')




class GetAllUserAPIView(APIView):
    def get(self, request):
        user = request.user
        serializer = GetAllUserSerializer(user)
        return Response(serializer.data)



class CreateDoctorAPIView(APIView):
    permission_classes = []  # Allow unauthenticated requests

    def post(self, request):
        serializer = DoctorCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

