from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserContacts)
admin.site.register(UserAddress)
admin.site.register(SecurityPoints)
admin.site.register(Profiles)
admin.site.register(ProfileSecurityPoints)
admin.site.register(UserProfiles)
admin.site.register(UserSecurityPoints)