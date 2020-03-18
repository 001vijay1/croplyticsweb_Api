from django.contrib import admin
from .models import UserAddress,UserContacts
# Register your models here.
admin.site.register(UserContacts)
admin.site.register(UserAddress)