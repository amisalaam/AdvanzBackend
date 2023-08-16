from rest_framework import serializers 
from .models import Doctor,Slots,Booking_Notification,Appointment,Services



class DoctorGetDetailsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name', read_only=True)
    department_name =serializers.CharField(source='department.department_name',read_only = True)
    class Meta:
        model = Doctor
        fields =['user','name','department_name','doctor_profile_image']
        
class GetSingleDoctorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name', read_only=True)
    department_name =serializers.CharField(source='department.department_name',read_only = True)
    class Meta:
        model = Doctor
        fields =['user','name','department_name','doctor_profile_image']



class CreateSlotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slots
        exclude =('is_booked',)

class GetSlotsListSerializer(serializers.ModelSerializer):
    start_time = serializers.TimeField(format='%H:%M')
    end_time = serializers.TimeField(format='%H:%M')


    class Meta:
        model = Slots
        fields = '__all__'

class UpdateSlotsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slots
        fields = ['is_booked', 'doctor', 'date', 'start_time', 'end_time', 'slot_duration']

        

class BookingNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking_Notification
        fields = '__all__'

        


class GetDashboardSlotSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.user.name')
    doctor_email = serializers.CharField(source='doctor.user.email')
    doctor_image = serializers.ImageField(source='doctor.doctor_profile_image', read_only=True)
    start_time = serializers.TimeField(format='%H:%M')
    end_time = serializers.TimeField(format='%H:%M')

    class Meta:
        model = Slots
        fields = ['id', 'doctor_name', 'doctor_image', 'date', 'start_time', 'end_time','doctor_email','is_booked']


class GetAppointmentSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.user.name',read_only=True)
    patient_name = serializers.CharField(source='patient.name',read_only=True)
    doctor_email = serializers.CharField(source='doctor.user.email',read_only=True)
    doctor_image = serializers.ImageField(source='doctor.doctor_profile_image', read_only=True)
    start_time = serializers.TimeField(source = 'slot.start_time',read_only=True,format='%H:%M')
    end_time = serializers.TimeField(source = 'slot.end_time',read_only=True,format='%H:%M')
    date = serializers.TimeField(source = 'slot.date',read_only=True)
    
    class Meta:
        model =Appointment
        fields = ['id', 'doctor_name', 'doctor_image', 'date', 'start_time', 'end_time','doctor_email','status','patient_name']
        


class GetUserAppointmentSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.user.name',read_only=True)
    patient_name = serializers.CharField(source='patient.name',read_only=True)
    doctor_email = serializers.CharField(source='doctor.user.email',read_only=True)
    doctor_image = serializers.ImageField(source='doctor.doctor_profile_image', read_only=True)
    start_time = serializers.TimeField(source = 'slot.start_time',read_only=True,format='%H:%M')
    end_time = serializers.TimeField(source = 'slot.end_time',read_only=True,format='%H:%M')
    date = serializers.TimeField(source = 'slot.date',read_only=True)
    
    class Meta:
        model =Appointment
        fields = ['id', 'doctor_name', 'doctor_image', 'date', 'start_time', 'end_time','doctor_email','status','patient_name']
    


class GetServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'
