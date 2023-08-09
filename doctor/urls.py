from django.urls import path,include
from .views import *
from .routing import websocket_urlpatterns



urlpatterns = [
    path('api/details/', GetDoctorListAPIView.as_view(), name='doctor_details'),
    path('api/create/slots/', CreateSlotsAPIView.as_view(), name='create_slots'),
    
    path('api/get/doctor/notification/<int:doctor_id>/', DoctorBookinNotificationAPiView.as_view(), name='doctor_notification'),
    path('api/get/admin/notification/', AdminBookingNotificationAPIView.as_view(), name='admin_notification'),
    path('api/get/slots/<int:doctor_id>/', GetSlotsListAPIView.as_view(), name='get_slots'),
    path('api/get/dashboard/slots/<int:doctor_id>/', GetDashboardSlotsListAPIView.as_view(), name='get_slots'),
    path('api/get/dashboard/appointment/<int:doctor_id>/', GetAppointmentAPIView.as_view(), name='get_appointment'),
    path('api/get/user/appointment/<int:user_id>/', GetUserAppointmentAPIView.as_view(), name='get_user_appointment'),
    path('api/get/single/doctor/<int:doctor_id>/', GetSingleDoctorAPIView.as_view(), name='get_doctor'),
    path('api/update/slots/<int:slot_id>/<int:doctor_id>/', UpdateSlotListAPIView.as_view(), name='slot-update'),
    path('ws/', include(websocket_urlpatterns)),
    
]
