from django.urls import path
from .views import DoctorDetailsAPIview

urlpatterns = [
    path('api/details/',DoctorDetailsAPIview.as_view())

]