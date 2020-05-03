from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializer import UserSerializer, FarmerLoginSerializer, OtpSerializer, ChangePasswordSerializer,ForgotPasswordSerializer,RegisterSerializer
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated,BasePermission
from .utils import send_response
from .errorCode import *
from random import randint
from Myuser.models import UserContacts,UserAddress
from rest_framework.generics import UpdateAPIView,CreateAPIView,ListAPIView
import json
from django.db import connection

#
# class UserPermission(BasePermission):
#     """
#     Custom permission to for user and Admin
#     """
#
#     def has_permission(self, request, view):
#         if view.action == 'destroy':
#             return request.user.is_staff
#         elif view.action in ['create','list','retrieve', 'update', 'partial_update']:
#             return request.user.is_active or request.user.is_staff
#         else:
#             return False
class Userviewsets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(username=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            msg = 'User registered successfully!'
            return Response(send_response(result=msg,errorcode=0,errormessage='',statuscode=200))
        else:
            message = serializer.errors
            try:
                message = serializer.errors
                err_msg = message['non_field_errors'][0]
                return Response(send_response(result=None,errorcode=1,errormessage=err_msg,statuscode=200))
            except:
                err_msg = "User already exists!"
                return Response(send_response(result=None,errorcode=1,errormessage=err_msg,statuscode=200))


    def list(self, request, *args, **kwargs):
        self.object_list = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(self.object_list, many=True)
        datas = serializer.data
        data = [{'id': datas[i]['id'], 'username': datas[i]['username'],'password': datas[i]['password'], 'first_name': datas[i]['first_name'],
                 'last_name': datas[i]['last_name'], 'is_active': datas[i]['is_active']}
                for i in range(len(datas))]
        return Response(send_response(result=data, errorcode=0, errormessage='', statuscode=200))

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, id=pk)
        serializer = UserSerializer(user)
        datas = serializer.data
        try:
            user_contact = UserContacts.objects.get(user_id=user)
            mobile = user_contact.user_mobile
        except:
            mobile = ''
        try:
            user_address = UserAddress.objects.get(user_id=user)
            address = user_address.address
            country = user_address.country
            state = user_address.state
            district = user_address.district
        except:
            address = ''
            country = ''
            state = ''
            district = ''
        data = {'username': datas['username'], 'first_name': datas['first_name'],
                'last_name': datas['last_name'], 'is_active': datas['is_active'], 'Mobile': mobile, 'Address': address,
                'Country': country, 'State': state, 'District': district}
        return Response(send_response(result=data, errorcode=0, errormessage='', statuscode=200))

    def destroy(self, request, pk=None, *args, **kwargs): # Soft delete
        try:
            user = User.objects.get(id=pk)
            user.is_active = False
            user.save()
            userid = user.username
            user_contact = UserContacts.objects.filter(user_id=userid)
            if(user_contact):
                for contact in user_contact:
                    contact.is_active = False
                    contact.save()
            else:
                pass
            user_address = UserAddress.objects.filter(user_id=userid)
            if (user_address):
                for address in user_address:
                    address.is_active = False
                    address.save()
            else:
                pass
            msg = 'User Deleted Successfully!'
            return Response(send_response(result=msg, errorcode=0, errormessage='', statuscode=200))
        except:
            msg = "Failed To Delete User?"
            return Response(send_response(result='', errorcode=FAILED_TO_DELETE_USER, errormessage=msg, statuscode=200))

    # def destroy(self, request, pk=None, *args, **kwargs):   # Hard delete
    #     try:
    #         user = User.objects.get(id=pk)
    #         userid = user.username
    #         user_contacts = UserContacts.objects.filter(user_id=userid)
    #         if(user_contacts):
    #             user_contacts.delete()
    #         else:
    #             pass
    #         user_address = UserAddress.objects.filter(user_id=userid)
    #         if(user_address):
    #             user_address.delete()
    #         else:
    #             pass
    #         user.delete()
    #         msg = 'User Deleted Successfully!'
    #         return Response(send_response(result=msg, errorcode=0, errormessage='', statuscode=200))
    #     except:
    #         msg = 'Something went wrong!!'
    #         return Response(send_response(result=msg, errorcode=0, errormessage='', statuscode=200))

    # def update(self, request,pk=None, *args, **kwargs):
    #     user = self.queryset.get(id=pk)
    #     print(user)
    #     serializer = UserSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     msg = 'User record updated successfully!'
    #     return Response(send_response(result=msg,errorcode=0,errormessage='',statuscode=200))


class LoginView(APIView):
    def post(self, request):
        serializer = FarmerLoginSerializer(data=request.data)
        if(serializer.is_valid()):
            username = serializer.validated_data['username']
            django_login(request, username)
            token, created = Token.objects.get_or_create(user=username)
            Queryset = User.objects.filter(username=username)
            usr = get_object_or_404(Queryset, username=username)
            serializer = UserSerializer(usr)
            auth_user_data = serializer.data
            user_contact = UserContacts.objects.filter(user_id=username)
            mobile = 0
            if(len(user_contact)==0):
                mobile = ''
            else:
                for contact in user_contact:
                    mobile = contact.user_mobile
            user_address = UserAddress.objects.filter(user_id=username)
            address = 0
            country = 0
            state = 0
            district = 0
            if(len(user_address)==0):
                address = ''
                country = ''
                state = ''
                district = ''
            else:
                for usr_address in user_address:
                    address = usr_address.address
                    country = usr_address.country
                    state = usr_address.state
                    district = usr_address.district
            data = {'accesskey': token.key, 'username':auth_user_data['username'],'first_name':auth_user_data['first_name'],
                    'last_name':auth_user_data['last_name'],'mobile':mobile,'address':address,'country':country,'state':state,
                    'district':district}
            return Response(send_response(result=data, errorcode=0, errormessage='', statuscode=200))
        else:
            message = serializer.errors
            err_msg = message['non_field_errors'][0]
            return Response(send_response(result=None,errorcode=1,errormessage=err_msg,statuscode=200))



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
        # message = 0
        # if(messageType=='registration'):
        #     message="OTP for registration is "+otp+". Please enter this to verify your mobile number. Croplytics®."
        # elif(messageType=='forgotPassword'):
        #     message="OTP for forgot password is "+otp+". Please enter this to verify your mobile number. Croplytics®."
        # else:
        #     message="OTP for reset password is "+otp+". Please enter this to verify your mobile number. Croplytics®."
        # res =  SendSms(mobile,message,messageType,projectId)
        # res_data = res.json()
        # statusCode = res_data['Result']['ResponseMetadata']['HTTPStatusCode']
        # if(statusCode==200):
        return Response(send_response(result={'OTP':otp,'Mobile':mobile},errorcode=0,errormessage='',statuscode=200))
        # else:
        #     return Response(send_response(result='',errorcode=OTP_SEND_SMS_FAILED,errormessage='Failed to send OTP. Please try again!',statuscode=200))

class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        if(serializer.is_valid()):
        # serializer.save()
            msg = 'password change successfully'
            return Response(send_response(result=msg,errorcode=0,errormessage='',statuscode=200))
        else:
            message = serializer.errors
            err_msg = message['non_field_errors'][0]
            return Response(send_response(result=None, errorcode=1, errormessage=err_msg, statuscode=200))


class ForgotPasswordView(UpdateAPIView):
    serializer_class = ForgotPasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            msg = 'password change successfully'
            return Response(send_response(result=msg,errorcode=0,errormessage='',statuscode=200))
        else:
            message = serializer.errors
            err_msg = message['non_field_errors'][0]
            return Response(send_response(result=None, errorcode=1, errormessage=err_msg, statuscode=200))


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        msg = 'User created successfully'
        return Response(send_response(result=msg,errorcode=0,errormessage='',statuscode=200))

# class ListApiView(ListAPIView):

    # def get_queryset(self):
    #     if self.request.user.is_superuser:
    #         return User.objects.all()
    #     return User.objects.filter(username=self.request.user)

    # def get(self, request, *args, **kwargs):
    #     # self.object_list = self.filter_queryset(self.get_queryset())
    #     # serializer = self.get_serializer(self.object_list, many=True)
    #     # datas = serializer.data
    #     users = User.objects.all()
    #     id = 0
    #     username = 0
    #     first_name = 0
    #     last_name = 0
    #     for user in users:
    #         id = user.id
    #         username=user.username
    #         first_name=user.first_name
    #         last_name=user.last_name
    #     user_contacts = UserContacts.objects.all()
    #     mobile = 0
    #     for contact in user_contacts:
    #         mobile = contact.user_mobile
    #     user_addresss = UserAddress.objects.all()
    #     address = 0
    #     country = 0
    #     state = 0
    #     district = 0
    #     for address in user_addresss:
    #         address=address.address
    #         country = address.country
    #         state = address.state
    #         district = address.district
    #     data = [{'id': id, 'username': username,'first_name':first_name,'last_name':last_name,'mobile':mobile,'address':address
    #              ,'country':country,'district':district}]
    #     return Response(send_response(result=data, errorcode=0, errormessage='', statuscode=200))
