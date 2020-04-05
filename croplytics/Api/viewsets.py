from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializer import UserSerializer, FarmerLoginSerializer,OtpSerializer
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated,BasePermission
from .utils import send_response,SendSms
from .errorCode import *
from random import randint

class UserPermission(BasePermission):
    """
    Custom permission to for user and Admin
    """

    def has_permission(self, request, view):
        if view.action == 'destroy':
            return request.user.is_staff
        elif view.action in ['create','list','retrieve', 'update', 'partial_update']:
            return request.user.is_active or request.user.is_staff
        else:
            return False


class Userviewsets(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated,UserPermission]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(username=self.request.user)

    def list(self, request, *args, **kwargs):
        self.object_list = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(self.object_list, many=True)
        datas = serializer.data
        data = [{'id': datas[i]['id'], 'username': datas[i]['username'], 'first_name': datas[i]['first_name'],
                 'last_name': datas[i]['last_name'], 'is_active': datas[i]['is_active'],
                 'mobile': datas[i]['UserContacts'][0]['user_mobile'], 'address': datas[i]['UserAddress'][0]['address'],
                 'country': datas[i]['UserAddress'][0]['country'], 'state': datas[i]['UserAddress'][0]['state'],
                 'district': datas[i]['UserAddress'][0]['district']}
                for i in range(len(datas))]
        return Response(send_response(result=data, errorcode=0, errormessage='', statuscode=200))

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, id=pk)
        serializer = UserSerializer(user)
        datas = serializer.data
        data = {'username': datas['username'], 'first_name': datas['first_name'],
                'last_name': datas['last_name'], 'is_active': datas['is_active'],
                'mobile': datas['UserContacts'][0]['user_mobile'], 'address': datas['UserAddress'][0]['address'],
                'country': datas['UserAddress'][0]['country'], 'state': datas['UserAddress'][0]['state'],
                'district': datas['UserAddress'][0]['district']}
        return Response(send_response(result=data, errorcode=0, errormessage='', statuscode=200))

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            user = User.objects.get(id=pk)
            user.is_active = False
            user.save()
            msg = 'User Deleted Successfully!'
            return Response(send_response(result=msg, errorcode=0, errormessage='', statuscode=200))
        except:
            msg = "Failed To Delete User?"
            return Response(send_response(result='', errorcode=1, errormessage=msg, statuscode=200))


class LoginView(APIView):
    def post(self, request):
        serializer = FarmerLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        queryset = User.objects.filter(username=user)
        usr = get_object_or_404(queryset, username=user)
        serializer = UserSerializer(usr)
        datas = serializer.data
        data = {'accesskey': token.key, 'username': datas['username'], 'first_name': datas['first_name'],
                'last_name': datas['last_name'], 'is_active': datas['is_active'],
                'mobile': datas['UserContacts'][0]['user_mobile'], 'address': datas['UserAddress'][0]['address'],
                'country': datas['UserAddress'][0]['country'], 'state': datas['UserAddress'][0]['state'],
                'district': datas['UserAddress'][0]['district']}
        return Response(send_response(result=data, errorcode=0, errormessage='', statuscode=200))


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        django_logout(request)
        msg = "You have successfully logout."
        return Response(send_response(result=msg, errorcode=0, errormessage='', statuscode=200))

class OtpView(APIView):
    def post(self,request):
        serializer = OtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data['mobile']
        messageType = serializer.validated_data['messageType']
        projectId = serializer.validated_data['projectId']
        otp = str(randint(1000,9000))
        message = 0
        if(messageType=='registration'):
            message="OTP for registration is "+otp+". Please enter this to verify your mobile number. Croplytics®."
        elif(messageType=='forgotPassword'):
            message="OTP for forgot password is "+otp+". Please enter this to verify your mobile number. Croplytics®."
        else:
            message="OTP for reset password is "+otp+". Please enter this to verify your mobile number. Croplytics®."
        res =  SendSms(mobile,message,messageType,projectId)
        res_data = res.json()
        statusCode = res_data['Result']['ResponseMetadata']['HTTPStatusCode']
        if(statusCode==200):
            return Response(send_response(result={'OTP':otp,'Mobile':mobile},errorcode=0,errormessage='',statuscode=200))
        else:
            return Response(send_response(result='',errorcode=OTP_SEND_SMS_FAILED,errormessage='Failed to send OTP. Please try again!',statuscode=200))