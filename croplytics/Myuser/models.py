from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserContacts(models.Model):#gene
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User,to_field='username',db_column='user_id',related_name='UserContacts',on_delete=models.CASCADE,blank=True, null=True)
    user_mobile = models.CharField(max_length=255, blank=True, null=True)
    user_email = models.EmailField(blank=True,null=True)
    creation_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    is_primary = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.user_mobile

    class Meta:
        managed = False
        db_table = 'user_contacts'


class UserAddress(models.Model):#generel
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,db_column='user_id',to_field='username',related_name='UserAddress',blank=True, null=True)
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
        managed = False
        db_table = 'user_address'

class SecurityPoints(models.Model):
    id = models.AutoField(primary_key=True)
    securityname = models.CharField(max_length=255, blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(blank=True, null=True)
    creationtime = models.DateTimeField(blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'security_points'

class Profiles(models.Model):
    id = models.AutoField(primary_key=True)
    profilename = models.CharField(max_length=255, blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(blank=True, null=True)
    creationtime = models.DateTimeField(auto_now_add=True)  # Field name made lowercase.
    isdeleted = models.BooleanField(default=True) # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'profiles'

class ProfileSecurityPoints(models.Model):
    id = models.AutoField(primary_key=True)
    profileid = models.ForeignKey(Profiles,db_column='profileid', on_delete=models.CASCADE,blank=True, null=True)  # Field name made lowercase.
    security_point = models.ForeignKey(SecurityPoints,db_column='security_point', on_delete=models.CASCADE, blank=True, null=True)
    creationtime = models.DateTimeField(auto_now_add=True)  # Field name made lowercase.
    isdeleted = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'profile_security_points'

class UserProfiles(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey(User,to_field='username',db_column='userid', on_delete=models.CASCADE, blank=True, null=True)  # Field name made lowercase.
    profileid = models.ForeignKey(Profiles,db_column='profileid', on_delete=models.CASCADE,blank=True, null=True)  # Field name made lowercase.
    creationtime = models.DateTimeField(auto_now_add=True)
    isdeleted = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'user_profiles'

class UserSecurityPoints(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey(User,db_column='userid',on_delete=models.CASCADE, to_field='username', blank=True, null=True)  # Field name made lowercase.
    security_point = models.ForeignKey(SecurityPoints,db_column='security_point', on_delete=models.CASCADE, blank=True, null=True)
    creationtime = models.DateTimeField(auto_now_add=True)
    isdeleted = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'user_security_points'