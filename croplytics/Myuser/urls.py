from django.urls import path
from .views import securityPoint

urlpatterns = [
    path('security/<str:userid>/',securityPoint)
]