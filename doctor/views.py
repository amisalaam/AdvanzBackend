from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime
from django.shortcuts import get_object_or_404
from .seriallizers import DoctorGetDetailsSerializer, CreateSlotsSerializer,GetSlotsListSerializer,GetSingleDoctorSerializer,UpdateSlotsListSerializer
from .models import Doctor, Department, Slots
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
        print (doctor)
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
                return Response({'error':'Slots overlaps with existing slots'},status = status.HTTP_400_BAD_REQUEST)
            
            slots = []
            current_time = start_time
            slot_count = (datetime.datetime.combine(date,end_time)-datetime.datetime.combine(date,start_time))//datetime.timedelta(minutes=slot_duration)
            for _ in range(slot_count):
                slot =Slots(
                    doctor=doctor,
                    date = date,
                    start_time = current_time,
                    end_time=(datetime.datetime.combine(date,current_time)+datetime.timedelta(minutes=slot_duration)).time(),
                    status = True,
                    slot_duration = slot_duration
                    )
                slots.append(slot)
                current_time = (datetime.datetime.combine(date,current_time)+datetime.timedelta(minutes=slot_duration)).time()
            Slots.objects.bulk_create(slots)
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    


class GetSlotsListAPIView(APIView):
    permission_classes = []

    def get(self, request, doctor_id):
        slots = Slots.objects.filter(doctor=doctor_id).order_by('id')
        serializer = GetSlotsListSerializer(slots, many=True)
        return Response(serializer.data)

class UpdateSlotListAPIView(APIView):
    permission_classes =[]

    def put(self, request, slot_id):
        instance = get_object_or_404(Slots, id=slot_id)
        serializer = UpdateSlotsListSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)




            
