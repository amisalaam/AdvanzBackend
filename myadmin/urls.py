from django.urls import path
from .views import *

urlpatterns = [
    path('api/get/all/doctors/',GetAllDoctorAPIView.as_view(),name = 'admin_get_all_doctors'),
    path('api/doctors/create/', CreateDoctorAPIView.as_view() , name='admin_create_doctor'),
    
    path('api/department/create/', DepartmentCreate.as_view() , name='admin_create_department '),
    path('api/delete/department/<int:department_id>/',DepartmentDelete.as_view(),name = 'admin_delete_department'),
    
    path('api/delete/doctor/<int:doctor_id>/',DeleteDoctorAPIView.as_view(),name = 'admin_delete_doctor'),
    path('api/edit/doctor/<int:doctor_id>/',EditDoctorProfileView.as_view(),name = 'admin_edit_doctors'),
    
    path('api/get/all/users/',GetAllUsersAPIView.as_view(),name = 'admin_get_all_Users'),
    path('api/block/users/<int:user_id>/',BlockUsersView.as_view(),name = 'admin_edit_doctors'),
    
    path('api/get/all/department/',GetAllDepartmentAPIView.as_view(),name = 'admin_get_department_Users'),
    
    path('api/get/booked/slots/',GetBookedSlotsAPIView.as_view(),name = 'admin_get_department_Users'),
    path('api/get/slots/all/doctor/', GetCreateSlotGetDoctorAPIView.as_view(), name='create_slots_getDoctors'),
    path('api/cancel/or/book/slots/<int:slot_id>/', AdminCancelSlotsAPIView.as_view(), name='admin_cancel_or_book_slot'),
    
    
    
    path('api/block/appointment/<int:appointment_id>/', AppointmentStatusUpdateView.as_view(), name='block_or_unblock_appointment'),
    path('api/get/dashboard/appointment/', GetAdminAppointmentAPIView.as_view(), name='get_appointment'),
    
    
    #DASHBOARD
    
    path('api/doctors/count/', DoctorCountAPIView.as_view(), name='doctor-count-api'),
    path('api/patients/count/', PatientCountAPIView.as_view(), name='patient-count'),
    path('api/appointments/count/', AppointmentCountView.as_view(), name='Appointment-count'),
    
] 
