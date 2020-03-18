from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserContacts(models.Model):#gene
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User,to_field='username',related_name='UserContacts',on_delete=models.CASCADE,blank=True, null=True)
    user_mobile = models.CharField(max_length=255, blank=True, null=True)
    user_email = models.EmailField(blank=True,null=True)
    creation_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    is_primary = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.user_mobile

    class Meta:
        managed = True
        db_table = 'user_contacts'


class UserAddress(models.Model):#generel
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,to_field='username',related_name='UserAddress',blank=True, null=True)
    village = models.CharField(max_length=255, blank=True, null=True)
    block = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    pincode = models.IntegerField(blank=True, null=True)
    is_primary = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return self.address

    class Meta:
        managed = True
        db_table = 'user_address'
