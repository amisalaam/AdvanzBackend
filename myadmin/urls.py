from django.urls import path
from .views import *

urlpatterns = [
    path('api/get/all/doctors/',GetAllDoctorAPIView.as_view(),name = 'admin_get_all_doctors'),
    path('api/doctors/create/', CreateDoctorAPIView.as_view() , name='admin_create_doctor'),
    path('api/delete/doctor/<int:doctor_id>/',DeleteDoctorAPIView.as_view(),name = 'admin_delete_doctor'),
    path('api/edit/doctor/<int:doctor_id>/',EditDoctorProfileView.as_view(),name = 'admin_edit_doctors'),
    
    path('api/get/all/users/',GetAllUsersAPIView.as_view(),name = 'admin_get_all_Users'),
    path('api/block/users/<int:user_id>/',BlockUsersView.as_view(),name = 'admin_edit_doctors'),
    
    path('api/get/all/department/',GetAllDepartmentAPIView.as_view(),name = 'admin_get_department_Users'),
    
    path('api/get/booked/slots/',GetBookedSlotsAPIView.as_view(),name = 'admin_get_department_Users'),
]
