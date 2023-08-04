from django.urls import path
from .views import GetAllUserAPIView



urlpatterns = [

    path('api/get/users/', GetAllUserAPIView.as_view()),
]