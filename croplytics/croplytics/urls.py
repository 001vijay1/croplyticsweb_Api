"""croplytics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from croplytics.router import router
from Api.viewsets import LogoutView,LoginView,ChangePasswordView,OtpView,ForgotPasswordView,RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include(router.urls),name = 'api'),
    path(r'api/v1/auth/login/',LoginView.as_view()),
    path(r'api/v1/auth/logout/',LogoutView.as_view()),
    path('ss/',include('Myuser.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
    path('forgot-password/',ForgotPasswordView.as_view()),
    path('reset-password/',ChangePasswordView.as_view()),
    path('otp/',OtpView.as_view()),
    path('create/',RegisterView.as_view()),
]
