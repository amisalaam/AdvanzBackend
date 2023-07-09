from rest_framework.views import APIView
from rest_framework.response import Response
from .seriallizers import DoctorDetailsSerializer
from .models import Doctor
from authentication.models import UserAccount
# Create your views here.


class DoctorDetailsAPIview(APIView):
    permission_classes =[]
    def get ( self,request):
            doctor =  Doctor.objects.all()
            serialzer = DoctorDetailsSerializer(doctor,many=True)
            serialzed_data = serialzer.data
            for data in serialzed_data:
                user_id = data['user']
                user_account = UserAccount.objects.get(id=user_id)
                data['name'] = user_account.name
            
            return Response(serialzed_data)