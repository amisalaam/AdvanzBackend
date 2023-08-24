
from .serializers import GetAllUserSerializer
from django.shortcuts import render
from django.http import HttpResponse
from .models import UserAccount
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import *
from doctor.models import Appointment
User = get_user_model()


# Create your views here.
def Login(request):
    return HttpResponse('Gellooo')


class GetAllUserAPIView(APIView):
    
    
    def get(self, request):
        user = request.user
        
        serializer = GetAllUserSerializer(user)
        return Response(serializer.data)


# USERDASHBOARD FUNCTION


class CancelUserAppointmentAPIView(APIView):
    permission_classes = []
    
    def put(self, request, appointment_id, user_id):
        try:
            appointment = Appointment.objects.get(pk=appointment_id, patient_id=user_id)
        except Appointment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if appointment.status == 'Approved':
            return Response({"message": "Only Approved appointments can be canceled."}, status=status.HTTP_400_BAD_REQUEST)

        slot = appointment.slot
        if slot.is_booked:
            slot.is_booked = False
            slot.save()

        appointment.status = 'cancelled'
        appointment.save()

        serializer = CancelUserAppointmentSerializer(appointment)
        return Response(serializer.data)
    
#DASHBOARD

class PatientAppointmentDataAPIView(APIView):
    permission_classes = []
    
    def get(self, request, user_id, format=None):
        patient = get_object_or_404(UserAccount, id=user_id)
        approved_appointment_count = Appointment.objects.filter(patient=patient, status='approved').count()
        blocked_appointment_count = Appointment.objects.filter(patient=patient, status='blocked').count()
        rejected_appointment_count = Appointment.objects.filter(patient=patient, status='rejected').count()
        cancelled_appointment_count = Appointment.objects.filter(patient=patient, status='cancelled').count()

        data = {
            'patient_name': patient.name,
            'approved_appointment_count': approved_appointment_count,
            'blocked_appointment_count': blocked_appointment_count,
            'rejected_appointment_count': rejected_appointment_count,
            'cancelled_appointment_count': cancelled_appointment_count,
        }

        serializer = PatientAppointmentDataSerializer(data)
        return Response(serializer.data)