from django.urls import path
from .views import *



urlpatterns = [

    path('api/get/users/', GetAllUserAPIView.as_view()),
    path('api/cancel/user/appointment/<int:appointment_id>/<int:user_id>/', CancelUserAppointmentAPIView.as_view()),
    
    #DASHBOARD
    path('user/api/appointment/count/<int:user_id>/', PatientAppointmentDataAPIView.as_view(), name='doctor_appointment_count'),
    

    
]