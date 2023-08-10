from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Booking_Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.shortcuts import get_object_or_404
from .seriallizers import *
from .models import Doctor, Department, Slots,Appointment
from authentication.models import UserAccount
from django.db.models import Q
# Create your views here.


class GetDoctorListAPIView(APIView):
    permission_classes = []

    def get(self, request):
        doctor = Doctor.objects.all()
        print(doctor)
        serializer = DoctorGetDetailsSerializer(doctor, many=True)
        serialized_data = serializer.data
        for data in serialized_data:
            user_id = data['user']
            user_account = UserAccount.objects.get(id=user_id)
            data['name'] = user_account.name

        return Response(serialized_data)


class GetSingleDoctorAPIView(APIView):
    permission_classes = []

    def get(self, request, doctor_id):
        doctor = Doctor.objects.get(user_id=doctor_id)
        print(doctor)
        serializer = GetSingleDoctorSerializer(doctor)
        serialized_data = serializer.data

        # Add user name to the serialized data
        user_id = serialized_data['user']
        user_account = UserAccount.objects.get(id=user_id)
        serialized_data['name'] = user_account.name

        return Response(serialized_data)


class CreateSlotsAPIView(APIView):
    permission_classes = []

    def post(self, request):

        serializer = CreateSlotsSerializer(data=request.data)
        valid = serializer.is_valid()
        if valid:
            doctor = serializer.validated_data['doctor']
            date = serializer.validated_data['date']
            start_time = serializer.validated_data['start_time']
            end_time = serializer.validated_data['end_time']
            slot_duration = int(serializer.validated_data['slot_duration'])

            overlapping_slots = Slots.objects.filter(Q(date=date) & (
                Q(start_time__lt=start_time, end_time__gt=start_time) |
                Q(start_time__lt=end_time, end_time__gt=end_time) |
                Q(start_time__gte=start_time, end_time__lte=end_time)
            ))
            if overlapping_slots.exists():
                return Response({'error': 'Slots overlaps with existing slots'}, status=status.HTTP_400_BAD_REQUEST)

            slots = []
            current_time = start_time
            slot_count = (datetime.datetime.combine(date, end_time)-datetime.datetime.combine(
                date, start_time))//datetime.timedelta(minutes=slot_duration)
            for _ in range(slot_count):
                slot = Slots(
                    doctor=doctor,
                    date=date,
                    start_time=current_time,
                    end_time=(datetime.datetime.combine(
                        date, current_time)+datetime.timedelta(minutes=slot_duration)).time(),
                    status=True,
                    slot_duration=slot_duration
                )
                slots.append(slot)
                current_time = (datetime.datetime.combine(
                    date, current_time)+datetime.timedelta(minutes=slot_duration)).time()
            Slots.objects.bulk_create(slots)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetSlotsListAPIView(APIView):
    permission_classes = []

    def get(self, request, doctor_id):
        object = Slots.objects.filter(doctor=doctor_id).order_by('id')
        serializer = GetSlotsListSerializer(object, many=True)
        return Response(serializer.data)




class UpdateSlotListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, slot_id, doctor_id):
        slot_instance = get_object_or_404(Slots, id=slot_id)
        serializer = UpdateSlotsListSerializer(
            slot_instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Check if the slot is available for booking
        if not slot_instance.is_booked:
            # Mark the slot as booked
            serializer.save(is_booked=True)

            # Create an appointment record for the booking
            appointment = Appointment.objects.create(
                patient=request.user,
                doctor=slot_instance.doctor,
                status='approved',  # You can set the status according to your logic
                slot=slot_instance
            )

            # Send a notification to the doctor using channels
            # channel_layer = get_channel_layer()
            # notification = {
            #     'type': 'slot_booked',
            #     'message': f'Slot {slot_id} has been booked by user {request.user}!',
            # }
            # async_to_sync(channel_layer.group_send)(
            #     f'doctor_{doctor_id}', notification)

            # # Send a notification to the superuser using channels
            # async_to_sync(channel_layer.group_send)(
            #     'superuser_group', notification)

            # # Save the booking notification to the database
            # booking_notification = Booking_Notification.objects.create(
            #     send_by=request.user,
            #     sent_to=get_object_or_404(Doctor, user_id=doctor_id),
            #     message=notification['message'],
            #     is_seen=False
            # )

            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response({'message': 'Slot is already booked.'}, status=status.HTTP_400_BAD_REQUEST)



    
class DoctorBookinNotificationAPiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, doctor_id):
        try:
            objects = Booking_Notification.objects.filter(sent_to_id=doctor_id).order_by('-time')
            serializer = BookingNotificationSerializer(objects, many=True)
            return Response(serializer.data)
        except Booking_Notification.DoesNotExist:
            return Response({"detail": "No notifications found for the specified doctor."},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": "An error occurred while processing the request."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
class AdminBookingNotificationAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        try:
            objects = Booking_Notification.objects.all().order_by('-time')
            serializer = BookingNotificationSerializer(objects, many=True)
            return Response(serializer.data)
        except Exception as e:
            # Handle any unexpected exceptions and return a generic error response
            return Response({"detail": "An error occurred while processing the request."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class GetDashboardSlotsListAPIView(APIView):
    permission_classes = []

    def get(self, request, doctor_id):
        object = Slots.objects.filter(doctor=doctor_id).order_by('id')
        serializer = GetDashboardSlotSerializer(object, many=True)
        return Response(serializer.data)
    
class GetAppointmentAPIView(APIView):
    permission_classes = []

    def get(self, request, doctor_id):
        object = Appointment.objects.filter(doctor=doctor_id).order_by('id')
        serializer = GetAppointmentSerializer(object, many=True)
        return Response(serializer.data)
    
    
class GetUserAppointmentAPIView(APIView):
    
    permission_classes = []

    def get(self, request,user_id):
        
        appointments = Appointment.objects.filter(patient_id=user_id)
        serializer = GetUserAppointmentSerializer(appointments, many=True)
        return Response(serializer.data)