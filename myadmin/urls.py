from django.urls import path
from .views import *

urlpatterns = [
    path('api/get/all/doctors/',GetAllDoctorAPIView.as_view(),name = 'admin_get_all_doctors'),
    path('api/delete/doctor/<int:doctor_id>/',DeleteDoctorAPIView.as_view(),name = 'admin_delete_doctor'),
    path('api/edit/doctor/<int:doctor_id>/',DoctorProfileEditView.as_view(),name = 'admin_edit_doctors'),
    path('api/doctors/create/', CreateDoctorAPIView.as_view() , name='admin_create_doctor'),
    path('api/get/all/users/',GetAllUsersAPIView.as_view(),name = 'admin_get_all_Users'),
    path('api/get/all/department/',GetAllDepartmentAPIView.as_view(),name = 'admin_get_department_Users'),
]
