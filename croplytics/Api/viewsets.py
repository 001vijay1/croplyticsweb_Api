from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView
from Api.serializer import UserSerializer, FarmerLoginSerializer
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from Myuser.utils import send_response


class Userviewsets(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        self.object_list = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(self.object_list, many=True)
        datas = serializer.data
        data = [{'id': datas[i]['id'], 'username': datas[i]['username'], 'first_name': datas[i]['first_name'],
                 'last_name': datas[i]['last_name'], 'is_active': datas[i]['is_active'],
                 'mobile': datas[i]['UserContacts'][0]['user_mobile'], 'address': datas[i]['UserAddress'][0]['address'],
                 'country': datas[i]['UserAddress'][0]['country'], 'state': datas[i]['UserAddress'][0]['state'],
                 'district': datas[i]['UserAddress'][0]['district']}
                for i in range(1, len(datas))]
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
            datas = UserSerializer(user).data
            data = {'username': datas['username'], 'first_name': datas['first_name'],
                    'last_name': datas['last_name'], 'is_active': datas['is_active'],
                    'mobile': datas['UserContacts'][0]['user_mobile'], 'address': datas['UserAddress'][0]['address'],
                    'country': datas['UserAddress'][0]['country'], 'state': datas['UserAddress'][0]['state'],
                    'district': datas['UserAddress'][0]['district']}
            return Response(send_response(result=data, errorcode=0, errormessage='', statuscode=200))
        except:
            msg = "user did not deactivate"
            return Response(send_response(result=msg, errorcode=0, errormessage='', statuscode=200))


class LoginView(APIView):
    def post(self, request):
        serializer = FarmerLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        django_login(request, user)
        token, created = Token.objects.get_or_create(user)
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
        msg = "You logged out successfully"
        return Response(send_response(result=msg, errorcode=0, errormessage='', statuscode=200))
