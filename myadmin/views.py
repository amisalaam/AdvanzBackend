from django.shortcuts import render
from django.contrib.auth import get_user_model
from doctor.models import Doctor
from rest_framework.views import APIView
from django.db import transaction
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import *
from doctor.models import Appointment

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

                # Create the doctor_data dictionary with necessary fields
                doctor_data = {
                    'department': {
                        'department_name': user.doctor.department.department_name,
                        'id': user.doctor.department.id,
                    },
                    'doctor_profile_image': user.doctor.doctor_profile_image.url if user.doctor.doctor_profile_image else None,
                    'user': {
                        'email': user.email,
                        'id': user.id,
                        'name': user.name,
                        'is_active': user.is_active,
                        'is_doctor': user.is_doctor,
                    }
                }

                return Response(doctor_data, status=status.HTTP_201_CREATED)
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
            slots = Slots.objects.all().order_by('id')
            serializer = BookedSlotSerializer(slots, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetCreateSlotGetDoctorAPIView(APIView):
    permission_classes = []

    def get(self, request):
        try:
            objects = Doctor.objects.all()
            serializer = GetCreateSlotGetDoctorSerializer(objects, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = str(e)
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetAdminAppointmentAPIView(APIView):
    permission_classes = []

    def get(self, request):
        object = Appointment.objects.all().order_by('id')
        serializer = GetAppointmentSerializer(object, many=True)
        return Response(serializer.data)


class AdminCancelSlotsAPIView(APIView):
    permission_classes = []

    def patch(self, request, slot_id):
        try:
            slot = Slots.objects.get(pk=slot_id)
        except Slots.DoesNotExist as e:
            print(f"Error: Slot with ID {slot_id} does not exist. {e}")
            return Response(status=status.HTTP_404_NOT_FOUND)

        if slot.is_booked:
            try:
                slot.is_booked = False
                slot.save()

                appointment = Appointment.objects.filter(slot=slot).first()
                if appointment:
                    appointment.status = 'blocked'
                    appointment.save()

                serializer = AdminCancelSlotsSerializer(slot)
                return Response(serializer.data)
            except Exception as e:
                print(
                    f"Error: An error occurred while canceling the booking. {e}")
                return Response({'message': 'An error occurred while canceling the booking.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'message': 'The slot is not booked, so it cannot be canceled.'}, status=status.HTTP_400_BAD_REQUEST)


class DepartmentCreate(APIView):
    permission_classes = []

    def post(self, request):
        serializer = GetAllDepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class DepartmentDelete(APIView):
    permission_classes = []

    def delete(self, request, department_id):
        department = get_object_or_404(Department, pk=department_id)
        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class AppointmentStatusUpdateView(APIView):
    permission_classes = []

    def patch(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, pk=appointment_id)

        if appointment.status == 'approved' and appointment.slot.is_booked:
            appointment.slot.is_booked = False
            appointment.slot.save()

            appointment.status = 'blocked'
            appointment.save()

            return Response({'message': 'Appointment status changed to blocked and slot is freed.'}, status=status.HTTP_200_OK)
        else:
            
            return Response({'message': 'Appointment cannot be blocked.'}, status=status.HTTP_400_BAD_REQUEST)


#DASHBOARD 

class DoctorCountAPIView(APIView):
    permission_classes = []
    
    def get(self, request, format=None):
        doctors_count = Doctor.objects.count()

        serializer = DoctorCountSerializer({'doctors_count': doctors_count})
        return Response(serializer.data)

class PatientCountAPIView(APIView):
    permission_classes = []
    
    def get(self, request, format=None):
        patients_count = UserAccount.objects.filter(is_superuser=False, is_doctor=False).count()
        serializer = PatinetCountSerializer({'patients_count': patients_count})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AppointmentCountView(APIView):
    permission_classes = []
    
    def get(self, request, format=None):
        appointment_count = Appointment.objects.count()
        serializer = AppointmentCountSerializer({'appointment_count': appointment_count})
        return Response(serializer.data)
