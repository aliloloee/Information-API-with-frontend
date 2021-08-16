from decimal import Context
from info.models import Information

from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from customUser.models import User

from .serializers import InformationSerializer, UserSerializer, ECGInformationSerializer, DoctorUsersSerializers
from .models import Information, ECGInformation
from .permissions import IsNurse



## Creating a new User
@api_view(['POST'])
@permission_classes((AllowAny, ))
def create_user(request) :
    ser = UserSerializer(data=request.data)
    if ser.is_valid():
        ser.save()
        return Response(ser.data, status=status.HTTP_201_CREATED)
    else :
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


## Get token
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_role': User.USER_TYPE_CHOICES[user.user_type - 1][1],
        })


## CRUD Information
class PatientInfoViewSet(viewsets.ModelViewSet) :
    queryset = Information.objects.all()
    serializer_class = InformationSerializer
    permission_classes = [IsAuthenticated, IsNurse, ]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', ]

    search_fields = ('fullname', 'national_id', 'gender', )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {
                "request_method": self.request.method
            }
        )
        return context

    ## url : 127.0.0.1:8000/....../pk/ => for single object
    ## url : 127.0.0.1:8000/....../ => for all objects
    def list(self, request, *args, **kwargs) :
        objs = super().list(request, *args, **kwargs)
        return objs
    
    def create(self, request, *args, **kwargs) :
        obj = super().create(request, *args, **kwargs)
        return obj

    ## url : 127.0.0.1:8000/....../pk/
    ## Full data for update
    def put(self, request, *args, **kwargs) :
        obj = super().update(request, *args, **kwargs)
        return obj

    ## url : 127.0.0.1:8000/....../pk/
    ## Partial data for update
    def patch(self, request, *args, **kwargs) :
        obj = super().partial_update(request, *args, **kwargs)
        return obj

    ## url : 127.0.0.1:8000/....../pk/
    def delete(self, request, *args, **kwargs) :
        obj = super().destroy(request, *args, **kwargs)
        return obj



# ECG Information
class ECGInformationViewSet(viewsets.ModelViewSet) :
    queryset = ECGInformation.objects.all()
    permission_classes = [IsAuthenticated, IsNurse, ]
    http_method_names = ['post', ]

    def create(self, request):
        data = request.data
        serializer = ECGInformationSerializer(context={'nurse':request.user}, data=data)
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoctorUsersViewset(viewsets.ModelViewSet) :
    queryset = User.objects.filter(user_type=1)
    permission_classes = [IsAuthenticated, IsNurse, ]
    http_method_names = ['get']
    serializer_class = DoctorUsersSerializers

    def list(self, request, *args, **kwargs):
        objs = super().list(request, *args, **kwargs)
        return objs