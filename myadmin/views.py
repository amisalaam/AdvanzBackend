from django.shortcuts import render
from django.contrib.auth import get_user_model
from doctor.models import Doctor
from rest_framework.views import APIView
from django.db import transaction
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from .serializers import *

# Create your views here.


# CREATING DOCTOR BY ADMIN
class CreateNewDoctorAPIView(APIView):

    def post(self, request):
        User = get_user_model()
        serializer = GetAllUsersSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Doctor created successfully.",
                "email": user.email,
                "name": user.name
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAllDoctorAPIView(APIView):
    permission_classes = []

    def get(self, request):
        objects = Doctor.objects.all()
        serializers = GetAllDoctorsSerializers(objects, many=True)
        return Response(serializers.data)


class CreateDoctorAPIView(APIView):
    permission_classes = []  

    def post(self, request):
        serializer = DoctorCreateSerializer(data=request.data)
        try:
            if serializer.is_valid():
                user = serializer.save()
                return Response({'message': 'Doctor account created successfully.'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'An error occurred while creating the doctor account.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetAllUsersAPIView(APIView):
    permission_classes = []

    def get(self, request):
        try:
            objects = UserAccount.objects.filter(
                is_superuser=False, is_doctor=False)
            serializers = GetAllUsersSerializer(objects, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'An error occurred while fetching user data.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetAllDepartmentAPIView(APIView):
    permission_classes = []

    def get(self, request):
        try:
            objects = Department.objects.all()
            serializers = GetAllDepartmentSerializer(objects, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": 'An error occured while fecthing department data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteDoctorAPIView(APIView):
    permission_classes = []

    def delete(self, request, doctor_id):
        try:
            with transaction.atomic():
                user = UserAccount.objects.get(id=doctor_id)
                doctor = Doctor.objects.get(user=user)

                doctor.delete()
                user.delete()

                return Response({'message': 'Doctor account and user successfully deleted.'}, status=status.HTTP_200_OK)

        except UserAccount.DoesNotExist:
            return Response({'message': 'User account not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Doctor.DoesNotExist:
            return Response({'message': 'Doctor not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'message': 'An error occurred while deleting the doctor account.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EditDoctorProfileView(APIView):
    permission_classes = []

    def get_user_and_doctor(self, doctor_id):
        try:
            user = UserAccount.objects.get(pk=doctor_id)
            try:
                doctor = Doctor.objects.get(user=user)
            except Doctor.DoesNotExist:
                doctor = None
            return user, doctor
        except UserAccount.DoesNotExist:
            return None, None

    def put(self, request, doctor_id):
        user, doctor = self.get_user_and_doctor(doctor_id)

        if not user:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        user_serializer = EditDoctorUserAccountSerializer(
            user, data=request.data, partial=True)
        doctor_serializer = EditDoctorSerializer(
            doctor, data=request.data, partial=True) if doctor else None

        if user_serializer.is_valid():
            user_instance = user_serializer.save()
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if doctor_serializer:
            if doctor_serializer.is_valid():
                doctor_serializer.save()
            else:

                return Response(doctor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'user': EditDoctorUserAccountSerializer(user_instance).data,
            'doctor': EditDoctorSerializer(doctor).data if doctor else None
        })
        
        
class BlockUsersView(APIView):
    permission_classes = []
    
    def patch(self, request, user_id):
        try:
            user = get_object_or_404(UserAccount, id=user_id, is_doctor=False)
            user.is_active = not user.is_active  
            user.save()
            
            if user.is_active:
                message = 'User is now active.'
            else:
                message = 'User is now blocked.'
            
            return Response({'message': message}, status=status.HTTP_200_OK)

        except UserAccount.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    
class GetBookedSlotsAPIView(APIView):
    permission_classes = []

    def get(self, request):
        try:
            booked_slots = Slots.objects.filter(is_booked=True)
            serializer = BookedSlotSerializer(booked_slots, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)