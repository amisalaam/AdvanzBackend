from django.urls import path
from .views import *

urlpatterns = [
    path('api/get/all/doctors/',GetAllDoctorAPIView.as_view(),name = 'admin_get_all_doctors')
]
