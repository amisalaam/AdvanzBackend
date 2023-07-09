from django.urls import path
from .views import UserAccountAPIView,CreateDoctorAPIView



urlpatterns = [

   
    path('api/me/', UserAccountAPIView.as_view()),
    path('api/doctors/create/', CreateDoctorAPIView.as_view()),
]