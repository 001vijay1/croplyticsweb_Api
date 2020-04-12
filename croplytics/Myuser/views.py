from django.shortcuts import render,HttpResponse
# from .models import UserSecurityPoints
from django.contrib.auth.hashers import check_password
# from django.contrib.auth.models import User


# Create your views here.
# def securityPoint(userid):
#     s_p = UserSecurityPoints.objects.filter(userid=userid)
#     return HttpResponse(s_p)



def securityPoint(request,userid):
    currentpassword= request.user.username #user's current password
    print(currentpassword)
    # currentpasswordentered= form.cleaned_data.get("lastpassword")
    matchcheck= check_password(userid,currentpassword)
    if(matchcheck):
        return HttpResponse('sucess')
