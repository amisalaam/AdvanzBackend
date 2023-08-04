from rest_framework import serializers

from doctor.models import Doctor, Department,Slots
from authentication.models import UserAccount


class GetAllUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = '__all__'


class GetAllDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class GetAllDoctorsSerializers(serializers.ModelSerializer):
    user = GetAllUsersSerializer()
    department = GetAllDepartmentSerializer()

    class Meta:
        model = Doctor
        fields = '__all__'


class DoctorCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    name = serializers.CharField(max_length=200)
    password = serializers.CharField(write_only=True)
    department_id = serializers.IntegerField()
    doctor_profile_image = serializers.ImageField(
        allow_null=True, required=False)

    class Meta:
        model = UserAccount
        fields = ('email', 'name', 'password',
                  'department_id', 'doctor_profile_image')

    def create(self, validated_data):
        email = validated_data['email']
        name = validated_data['name']
        password = validated_data['password']
        department_id = validated_data['department_id']
        doctor_profile_image = validated_data.get('doctor_profile_image', None)

        department = Department.objects.get(pk=department_id)

        user = UserAccount.objects.create_doctor(
            email=email, name=name, password=password)
        doctor = Doctor.objects.create(
            user=user, department=department, doctor_profile_image=doctor_profile_image)

        return user


class EditDoctorUserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['name', 'is_active']


class EditDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['department', 'doctor_profile_image']


class BookedSlotSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.user.name')
    doctor_email = serializers.CharField(source='doctor.user.email')
    doctor_image = serializers.ImageField(source='doctor.doctor_profile_image', read_only=True)

    class Meta:
        model = Slots
        fields = ['id', 'doctor_name', 'doctor_image', 'date', 'start_time', 'end_time','doctor_email','is_booked']