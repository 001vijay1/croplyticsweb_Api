from rest_framework import serializers
from Myuser.models import UserAddress, UserContacts,Profiles,UserProfiles
from django.contrib.auth.models import User
from rest_framework import exceptions
from django.contrib.auth import authenticate
import json
from .utils import send_response
from .errorCode import *

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

class UserContactsSerialier(serializers.ModelSerializer):
    class Meta:
        model = UserContacts
        fields = ['id', 'user_mobile']

class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ['id', 'address', 'country', 'state', 'district']
        extra_kwargs = {'id': {'read_only': False}}


class UserSerializer(serializers.HyperlinkedModelSerializer):
    UserContacts = UserContactsSerialier(many=True)
    UserAddress = UserAddressSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'is_active', 'UserContacts', 'UserAddress']
        extra_kwargs = {'is_active': {'read_only': True}}

    def create(self, validated_data):
        UserContacts_data = validated_data.pop('UserContacts')
        UserAddress_data = validated_data.pop('UserAddress')
        user = User.objects.create_user(**validated_data)
        for usercontact in UserContacts_data:
            UserContacts.objects.create(user_id=user, **usercontact)
        for useraddress in UserAddress_data:
            UserAddress.objects.create(user_id=user, **useraddress)
        profile = Profiles.objects.get(profilename='Farmer')
        UserProfiles.objects.create(userid=user, profileid=profile, isdeleted=False)
        return user

    def update(self, instance, validated_data):
        UserContacts_data = validated_data.pop('UserContacts')
        UserAddress_data = validated_data.pop('UserAddress')
       
        UserContacts = (instance.UserContacts).all()
        UserContacts = list(UserContacts)
        UserAddress = (instance.UserAddress).all()
        UserAddress = list(UserAddress)

        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        for usr_contact in UserContacts_data:
            user_contact = UserContacts.pop(0)
            user_contact.user_mobile = usr_contact.get('user_mobile', user_contact.user_mobile)
            user_contact.save()
        for usr_address in UserAddress_data:
            user_address = UserAddress.pop(0)
            user_address.address = usr_address.get('address', user_address.address)
            user_address.country = usr_address.get('country', user_address.country)
            user_address.state = usr_address.get('state', user_address.state)
            user_address.district = usr_address.get('district', user_address.district)
            user_address.save()

        return instance

    # def update(self, instance, validated_data):
    #     user_data = validated_data.pop('user')
    #     print(user_data)
    #     user_contact_data = validated_data.pop('user_contact')
    #     print(user_contact_data)
    #     # users = (instance.user).filter(first_name=user_data['first_name'])
    #     # users = list(users)
    #     # user_contacts = (instance.user_contact).filter(user_mobile=)
    #     # user_contacts = list(user_contacts)

    #     instance.address = validated_data.get('address',instance.address)
    #     instance.country = validated_data.get('country',instance.country)
    #     instance.state = validated_data.get('state', instance.state)
    #     instance.district = validated_data.get('district', instance.district)
    #     instance.save()

    #     # for usr_data in user_data:
    #     #     user = users.pop(0)
    #     #     user.username = usr_data.get('username', user.username)
    #     #     user.password = usr_data.get('password', user.password)
    #     #     user.first_name = usr_data.get('first_name', user.first_name)
    #     #     user.last_name = usr_data.get('last_name',user.last_name)
    #     #     user.save()
    #     # for usr_contact_data in user_contacts_data:
    #     #     user_contact = user_contacts.pop(0)
    #     #     usr_data.user_mobile = usr_contact_data.get('user_mobile',usr_contact_data.user_mobile)
    #     #     user_contact.save()
    #     # return instance
    #     keep_user_data = []
    #     keep_user_contact_data = []
    #     for usr_data in user_data:
    #         if('username' in usr_data.keys()):
    #             if(User.objects.filter(username=usr_data['username']).exists()):
    #                 c = User.objects.get(id=usr_data['id'])
    #                 c.username = usr_data.get('username',c.username)
    #                 c.password = usr_data.get('password',c.password)
    #                 c.first_name = usr_data.get('first_name',c.first_name)
    #                 c.last_name = usr_data.get('last_name',c.last_name)
    #                 c.save()
    #                 keep_user_data.append(c)
    #             else:
    #                 print("not updated.........")
    #     for usr_contact_data in user_contact_data:
    #         if('user_mobile' in usr_contact_data.keys()):
    #             if(UserContacts.objects.filter(user_mobile=usr_contact_data['user_mobile']).exist()):
    #                 c = UserContacts.objects.get(id=usr_contact_data['id'])
    #                 c.user_mobile = usr_contact_data.get('user_mobile',c.user_mobile)
    #                 c.save()
    #                 keep_user_contact_data.append(c)
    #             else:
    #                 print('not updated')
    #     return instance


class FarmerLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username', '')
        password = data.get('password', '')

        if (username and password):
            user = authenticate(username=username, password=password)
            if (user):
                if (user.is_active):
                    data['user'] = user
                else:
                    response = send_response(result='', errorcode=USER_DEACTIVATED, errormessage='User is not active!',
                                             statuscode=200)
                    msg = json.dumps(response)
                    raise exceptions.ValidationError(msg)
            else:
                response = send_response(result='', errorcode=USER_LOGIN_CREDENTIAL_WRONG,
                                         errormessage='Authentication error occurred. Please try again!',
                                         statuscode=200)
                msg = json.dumps(response)
                raise exceptions.ValidationError(msg)
        else:
            response = send_response(result='', errorcode=USERNAME_PASSWORD_EMPTY,
                                     errormessage='UserName and Password should not empty!', statuscode=200)
            msg = json.dumps(response)
            raise exceptions.ValidationError(msg)
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
        elif(con!=mobile and messageType=='forgotPassword'):
            response = send_response(result='',errorcode=MOBILE_DOES_NOT_EXISTS,errormessage='Mobile Number Does not exists!',statuscode=200)
            msg = json.dumps(response)
            raise exceptions.ValidationError(msg)
        elif(con and messageType=='resetPassword'):
            pass
        elif(con!=mobile and messageType=='resetPassword'):
            response = send_response(result='',errorcode=MOBILE_DOES_NOT_EXISTS,errormessage='Mobile Number Does not exists!',statuscode=200)
            msg = json.dumps(response)
            raise exceptions.ValidationError(msg)
        elif(con!=mobile and messageType=='registration'):
            pass
        elif(con and messageType=='registration'):
            response = send_response(result='',errorcode=MOBILE_DOES_NOT_EXISTS,errormessage='Mobile Number already exists!',statuscode=200)
            msg = json.dumps(response)
            raise exceptions.ValidationError(msg)
        return data