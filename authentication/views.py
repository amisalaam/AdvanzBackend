
from .serializers import GetAllUserSerializer
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





