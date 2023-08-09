
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

    def put(self, request,appointment_id):
        
        serializer = CancelUserAppointmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        appointment = get_object_or_404(
            Appointment, id=appointment_id, patient=23)

        if appointment.status == 'approved':
            # Update appointment status to 'pending'
            appointment.status = 'cancelled'
            appointment.save()

            # Update the associated slot's booking status
            slot = appointment.slot
            slot.is_booked = False
            slot.save()

            return Response({'message': 'Slot booking has been canceled successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Cannot cancel the slot as it is not in an approved state.'}, status=status.HTTP_400_BAD_REQUEST)
