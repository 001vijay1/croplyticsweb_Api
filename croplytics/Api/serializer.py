from rest_framework import serializers
from Myuser.models import UserAddress, UserContacts,Profiles,UserProfiles
from django.contrib.auth.models import User
from rest_framework import exceptions
from django.contrib.auth import authenticate
import json
from .utils import send_response,custom_exception_handler
from .errorCode import *
from django.contrib.auth import password_validation

from django.contrib.auth.hashers import make_password,check_password

# class UserSerializer(serializers.ModelSerializer):

#     username = serializers.CharField(
#         write_only=False,
#         required=False,
#         help_text='username must be required',
#         style={'input_type': 'text', 'placeholder': 'UserName'}
#     )

# password = serializers.CharField(
#     write_only=True,
#     required=True,
#     help_text='password must be alphanumeric',
#     style={'input_type': 'password', 'placeholder': 'Password'}
# )

# class Meta:
#     model = User
#     fields = ['username','password','first_name','last_name','is_active']
#     extra_kwargs = {'password': {'write_only': True},
#                 'is_active': {'read_only': True}}
# read_only_fields = ['username','password']

# def create(self, validated_data):
#     validated_data['password'] = make_password(validated_data.get('password'))
#     return super(UserSerializer, self).create(validated_data)
#
class UserContactsSerialier(serializers.ModelSerializer):
    class Meta:
        model = UserContacts
        fields = ['id', 'user_mobile']
#
#
class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ['id', 'address', 'country', 'state', 'district']
        extra_kwargs = {'id': {'read_only': False}}


class UserSerializer(serializers.ModelSerializer):
    mobile = UserContactsSerialier().fields['user_mobile']
    address = UserAddressSerializer().fields['address']
    country = UserAddressSerializer().fields['country']
    state = UserAddressSerializer().fields['state']
    district = UserAddressSerializer().fields['district']
    # created_by = UserAddressSerializer().fields['created_by']

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name',
                  'is_active', 'mobile','address','country','state','district']
        extra_kwargs = {'is_active': {'read_only': True}}

    def validate(self, attrs):
        mobile = attrs['mobile']
        va = UserContacts.objects.filter(user_mobile=mobile)
        if(va):
            msg = "This mobile number already exists, Please enter another mobile number."
            raise exceptions.ValidationError(msg)
        else:
            pass
        return  attrs

    def create(self, validated_data):
        mobile_data = validated_data.pop('mobile')
        address_data = validated_data.pop('address')
        country_data = validated_data.pop('country')
        state_data = validated_data.pop('state')
        district_data = validated_data.pop('district')
        created_by = validated_data.pop('created_by')
        user = User.objects.create_user(**validated_data)
        UserContacts.objects.create(user_id=user, user_mobile=mobile_data,created_by=created_by)
        UserAddress.objects.create(user_id=user, address=address_data, country=country_data, state=state_data,
                                   district=district_data,created_by=created_by)
        profile = Profiles.objects.get(profilename='Farmer')
        UserProfiles.objects.create(userid=user, profileid=profile, isdeleted=False)
        return user

    # def create(self, validated_data):
    #     UserContacts_data = validated_data.pop('UserContacts')
    #     UserAddress_data = validated_data.pop('UserAddress')
    #     user = User.objects.create_user(**validated_data)
    #     for usercontact in UserContacts_data:
    #         UserContacts.objects.create(user_id=user, **usercontact)
    #     for useraddress in UserAddress_data:
    #         UserAddress.objects.create(user_id=user, **useraddress)
    #     profile = Profiles.objects.get(profilename='Farmer')
    #     UserProfiles.objects.create(userid=user, profileid=profile, isdeleted=False)
    #     return user
    #
    #
    def update(self, instance, validated_data):
        userid = validated_data.pop('username')
        mobile_data = validated_data.pop('mobile')
        address_data = validated_data.pop('address')
        country_data = validated_data.pop('country')
        state_data = validated_data.pop('state')
        district_data = validated_data.pop('district')
        createdby_data = validated_data.pop('created_by')

        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        user_contact = UserContacts.objects.get(user_id=userid)
        user_contact.user_mobile = mobile_data
        user_contact.created_by = createdby_data
        user_contact.save()
        user_address = UserAddress.objects.get(user_id=userid)
        user_address.address = address_data
        user_address.country = country_data
        user_address.state = state_data
        user_address.district = district_data
        user_address.created_by = createdby_data
        user_address.save()
        return instance

class FarmerLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username', '')
        password = data.get('password', '')

        if (username  and password):
            user = authenticate(username=username, password=password)
            if (user):
                if (user.is_active):
                    data['username'] = user
                else:
                    response = 'User is not active!'
                    raise exceptions.ValidationError(response)
            elif(username  and password):
                try:
                    contacts = UserContacts.objects.filter(user_mobile=username)
                    if(len(contacts)==1):
                        userid = 0
                        for contact in contacts:
                            userid = contact.user_id
                            user = authenticate(username=userid, password=password)
                            if(user):
                                if (user.is_active):
                                    data['username'] = user
                                else:
                                    response = 'User is not active!'
                                    raise exceptions.ValidationError(response)
                            else:
                                response = 'Authentication error occurred. Please try again!'
                                raise exceptions.ValidationError(response)
                    else:
                        msg = 'This mobile number associated with more than one users.So you can not login.Please contact to administration!'
                        raise exceptions.ValidationError(msg)

                except:
                    response = 'Authentication error occurred. Please try again!'
                    raise exceptions.ValidationError(response)
        else:
            response = 'UserName and Password should not empty!'
            raise exceptions.ValidationError(response)
        return data

class OtpSerializer(serializers.Serializer):
    mobile = serializers.CharField()
    messageType = serializers.CharField()
    projectId = serializers.IntegerField()


    def validate(self,data):
        mobile = data.get('mobile','')
        messageType = data.get('messageType','')
        con = UserContacts.objects.filter(user_mobile=mobile)
        if(con and messageType=='forgotPassword'):
            pass
        elif(not con and messageType=='forgotPassword'):
            msg = "This mobile number does not exists, Please enter another mobile number."
            # response = send_response(result='',errorcode=MOBILE_DOES_NOT_EXISTS,errormessage=msg,statuscode=200)
            raise exceptions.ValidationError(msg)
        elif(con and messageType=='resetPassword'):
            pass
        elif(not con and messageType=='resetPassword'):
            msg = "This mobile number does not exists, Please enter another mobile number."
            # response = send_response(result='',errorcode=MOBILE_DOES_NOT_EXISTS,errormessage=msg,statuscode=200)
            raise exceptions.ValidationError(msg)
        elif(not con and messageType=='registration'):
            pass
        elif(con and messageType=='registration'):
            msg = "This mobile number already exists, Please enter another mobile number."
            # response = send_response(result='',errorcode=MOBILE_DOES_NOT_EXISTS,errormessage=msg,statuscode=200)
            raise exceptions.ValidationError(msg)
        return data


class ChangePasswordSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=14, write_only=True, required=True)
    new_password = serializers.CharField(max_length=128, write_only=True, required=True)
    confirm_password = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate(self, data):
        try:
            user = UserContacts.objects.get(user_mobile=data['mobile'])
            if(user):
                if data['new_password'] != data['confirm_password']:
                    msg = "Password and confirmation password does not match."
                    raise exceptions.ValidationError(msg)
                else:
                    userid = user.user_id
                    password = data['new_password']
                    user = User.objects.get(username=userid)
                    user.set_password(password)
                    user.save()
                    return user
        except:
            msg = 'This mobile number does not exist. Please enter another mobile number.'
            # response = send_response(result='', errorcode=USERID_NOT_MATCH, errormessage=msg, statuscode=200)
            raise exceptions.ValidationError(msg)
        return data

    # def validate(self, data):
    #     if data['new_password'] != data['confirm_password']:
    #         msg = "Your password and confirmation password do not match."
    #         response = send_response(result='',errorcode=PASSWORD_NOT_MATCH,errormessage=msg,statuscode=200)
    #         raise exceptions.ValidationError(response)
    #     password_validation.validate_password(data['new_password'])
    #     return data
    #
    # def save(self, **kwargs):
    #     userid = self.validated_data['userid']
    #     password = self.validated_data['password']
    #     user = User.objects.get(username=userid)
    #     user.set_password(password)
    #     user.save()
    #     return user

class ForgotPasswordSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=14, write_only=True, required=True)
    new_password = serializers.CharField(max_length=128, write_only=True, required=True)


    def validate(self, data):
        user_contact = UserContacts.objects.filter(user_mobile=data['mobile'])
        if(user_contact):
            if(len(user_contact)==1):
                pass
            else:
                msg = "This mobile number associated with more than one users.So you can not change your password.Please contact to administration!."
                # response = send_response(result='',errorcode=USERID_NOT_MATCH,errormessage=msg,statuscode=200)
                raise serializers.ValidationError(msg)
        else:
            msg = 'This mobile number does not exist. Please enter another mobile number.'
            # response = send_response(result='',errorcode=USERID_NOT_MATCH,errormessage=msg,statuscode=200)
            raise serializers.ValidationError(msg)
        return data
    #
    # def validate(self, data):
    #     password_validation.validate_password(data['new_password'])
    #     return data

    def save(self, **kwargs):
        contact = self.validated_data['mobile']
        userobject = UserContacts.objects.get(user_mobile=contact)
        usrid = userobject.userid
        password = self.validated_data['new_password']
        user = User.objects.get(username=usrid)
        user.set_password(password)
        user.save()
        return user

class RegisterSerializer(serializers.ModelSerializer):   # This Api only for registration
    mobile = serializers.CharField(max_length=14,required=True)
    address = serializers.CharField(max_length=255,required=True)
    country = serializers.CharField(max_length=255,required=True)
    state = serializers.CharField(max_length=255,required=True)
    district = serializers.CharField(max_length=255,required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name',
                  'is_active', 'mobile','address','country','state','district']
        extra_kwargs = {'is_active': {'read_only': True}}

    def create(self, validated_data):
        mobile_data = validated_data.pop('mobile')
        address_data = validated_data.pop('address')
        country_data = validated_data.pop('country')
        state_data = validated_data.pop('state')
        district_data = validated_data.pop('district')
        user = User.objects.create_user(**validated_data)
        UserContacts.objects.create(user_id=user, user_mobile=mobile_data)
        UserAddress.objects.create(user_id=user, address=address_data, country=country_data, state=state_data,
                                   district=district_data)
        profile = Profiles.objects.get(profilename='Farmer')
        UserProfiles.objects.create(userid=user, profileid=profile, isdeleted=False)
        return user


