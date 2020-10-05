from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)

    contact = models.CharField(max_length=10, blank=True, null=True)

    # def __str__(self):
    #     return self.user.username
# class User(AbstractUser):
#       ADMIN = 1
#       OBSERVER = 2
#       CUSTODIAN =3
#       COORDINATOR=4
#       WARD_REPRESENTATIVE =5
#       OPD_COORDINATOR=6
      
#       ROLE_CHOICES = (
#           (ADMIN, 'Admin'),
#           (OBSERVER, 'Observer'),
#           (CUSTODIAN, 'Custodian'),
#           (COORDINATOR, 'Coordinator'),
#           (WARD_REPRESENTATIVE, 'Ward_representative'),
#           (OPD_COORDINATOR, 'OPD_Coordinator'),
#       )
#       role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
# Create your models here.
# @permission_required('bed_dash.add_vote')
class coordinat_up(models.Model):
    date= models.CharField(max_length=50,null=True)
    cordname = models.CharField(max_length=50,null=True)
    contnum = models.CharField(max_length=50,null=True)
    altnum = models.CharField(max_length=50,null=True)
    schfrom = models.TimeField(auto_now=False, auto_now_add=False)
    schto = models.TimeField(auto_now=False, auto_now_add=False)


    def __str__(self):
        return self.cordname;
class doctor_up(models.Model):
    date= models.CharField(max_length=50,null=True)
    docname = models.CharField(max_length=50,null=True)
    contnum = models.CharField(max_length=50,null=True)
    altnum = models.CharField(max_length=50,null=True)
    schfrom = models.TimeField(auto_now=False, auto_now_add=False)
    schto = models.TimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.docname;

        
class formupdate(models.Model):
    date= models.CharField(max_length=50,null=True)
    tme=models.CharField(max_length=50,null=True)
    upby=models.CharField(max_length=50,null=True)
    contnum=models.CharField(max_length=50,primary_key=True)
    wardnum = models.CharField(max_length=50,null=True)
    wardtype = models.CharField(max_length=50,null=True)
    vacbed = models.CharField(max_length=50,null=True)
    ventbed = models.CharField(max_length=50,null=True)
    oxybed = models.CharField(max_length=50,null=True)

class Roles(models.Model):
    account_type = models.CharField(max_length=50, blank=True, null=True)
    roles = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'


class WardDetails(models.Model):
    ward = models.CharField(max_length=20,primary_key=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    details = models.CharField(max_length=50, blank=True, null=True)
    unit = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ward_details'

class Coordinators(models.Model):
    name =models.CharField(primary_key=True, max_length=50)
    mobile = models.CharField(max_length=12, blank=True, null=True)
    unit = models.CharField(max_length=20, blank=True, null=True)
    designation = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coordinators'


class DataEntered(models.Model):
    account_type = models.CharField(max_length=50, blank=True, null=True)
    data_entered = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_entered'


class AdminData(models.Model):
    name = models.CharField(max_length=60, blank=True, null=True)
    mobile = models.CharField(max_length=12, blank=True, null=True)
    account_type = models.CharField(max_length=50, blank=True, null=True)
    designation = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admin_data'


class bulk_reg(models.Model):
    # id =models.CharField( max_length=50,primary_key=True)
    name= models.CharField( max_length=50)
    email = models.EmailField( max_length=254)
    mobile= models.CharField( max_length=10)
    designation = models.CharField( max_length=50)
    roles= models.CharField( max_length=50)
    from_date= models.DateField(auto_now=False, auto_now_add=False,null=True)
    to_date= models.DateField(auto_now=False, auto_now_add=False,null=True)