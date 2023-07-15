from rest_framework import serializers 
from .models import Doctor,Slots



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
        fields ='__all__'

        


