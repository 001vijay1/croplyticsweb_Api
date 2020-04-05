from django.shortcuts import render,HttpResponse
from .models import UserSecurityPoints

# Create your views here.
def securityPoint(userid):
    s_p = UserSecurityPoints.objects.filter(userid=userid)
    return HttpResponse(s_p)
