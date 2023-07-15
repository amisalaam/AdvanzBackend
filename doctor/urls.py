from django.urls import path
from .views import *

urlpatterns = [
    path('api/details/',GetDoctorListAPIView.as_view(),name='doctor_details'),
    path('api/create/slots/',CreateSlotsAPIView.as_view(),name='create_slots'),
    path('api/get/slots/<int:doctor_id>/',GetSlotsListAPIView.as_view(),name='get_slots'),
    path('api/get/single/doctor/<int:doctor_id>/',GetSingleDoctorAPIView.as_view(),name='get_slots'),
    path('api/update/slots/<int:slot_id>/', UpdateSlotListAPIView.as_view(), name='slot-update'),
    
    

]