from django.urls import path
from .views import GetAllUserAPIView,CreateDoctorAPIView



urlpatterns = [

   
    path('api/get/users/', GetAllUserAPIView.as_view()),
    path('api/doctors/create/', CreateDoctorAPIView.as_view()),
]