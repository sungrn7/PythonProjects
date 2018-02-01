from django.db import models
from jsonfield import JSONField
import time
import datetime

now = datetime.datetime.now()

class Account(models.Model):
    ids = models.CharField(max_length=128)
    point = models.FloatField(default=0)
    lasted = models.CharField(max_length=128, default=now.strftime('%y-%m-%d'))
    td_get = models.BooleanField(default=False)
    idx = models.IntegerField(default=0)

class Announ_kongju(models.Model):
    day = models.CharField(max_length=128)
    content = models.TextField(blank=True, null=True)

class Announ_brain(models.Model):
    day = models.CharField(max_length=128)
    content = models.TextField(blank=True, null=True)

class Announ_sabum(models.Model):
    day = models.CharField(max_length=128)
    content = models.TextField(blank=True, null=True)

class Announ_insa(models.Model):
    day = models.CharField(max_length=128)
    content = models.TextField(blank=True, null=True)

#class Announ_natural(models.Model):
#    day = models.CharField(max_length=128)
#    content = models.TextField(blank=True, null=True)

class Announ_indu(models.Model):
    day = models.CharField(max_length=128)
    content = models.TextField(blank=True, null=True)

class Announ_cnh(models.Model):
    day = models.CharField(max_length=128)
    content = models.TextField(blank=True, null=True)

class Announ_art(models.Model):
    day = models.CharField(max_length=128)
    content = models.TextField(blank=True, null=True)

class Announ_control(models.Model):
	day = models.CharField(max_length=128)
	content = models.TextField(blank=True, null=True)

class Announ_cse(models.Model):
	day = models.CharField(max_length=128)
	content = models.TextField(blank=True, null=True)


class Announ_mech(models.Model):
	day = models.CharField(max_length=128)
	content = models.TextField(blank=True, null=True)
class Announ_civil(models.Model):
	day = models.CharField(max_length=128)
	content = models.TextField(blank=True, null=True)
class Announ_archi(models.Model):
	day = models.CharField(max_length=128)
	content = models.TextField(blank=True, null=True)
class Announ_archeng(models.Model):
	day = models.CharField(max_length=128)
	content = models.TextField(blank=True, null=True)
class Announ_ame(models.Model):
	day = models.CharField(max_length=128)
	content = models.TextField(blank=True, null=True)
class Announ_ie(models.Model):
	day = models.CharField(max_length=128)
	content = models.TextField(blank=True, null=True)
class Announ_optical(models.Model):
	day = models.CharField(max_length=128)
	content = models.TextField(blank=True, null=True)

# 학식
class dormi_choen(models.Model):
    day = models.CharField(max_length=128)
    content = models.TextField(blank=True, null=True)
                                                       
class school_choen(models.Model):
    day = models.CharField(max_length=128)
    content = models.TextField(blank=True, null=True)
                                                                     
class staff_choen(models.Model):
    day = models.CharField(max_length=128)
    content = models.TextField(blank=True, null=True)
                                     
class school_yesan(models.Model):
    day = models.CharField(max_length=128)
    content = models.TextField(blank=True, null=True)
                                     
class staff_yesan(models.Model):
    day = models.CharField(max_length=128)
    content = models.TextField(blank=True, null=True)
                                                                               
class dreem_singwan(models.Model):
    day = models.CharField(max_length=128)
    content = models.TextField(blank=True, null=True)
                                     
class bision_singwan(models.Model):
    day = models.CharField(max_length=128)
    content = models.TextField(blank=True, null=True)
                                                             
class school_singwan(models.Model):
    day = models.CharField(max_length=128)
    content = models.TextField(blank=True, null=True)
                                                                            
class staff_singwan(models.Model):
    day = models.CharField(max_length=128)
    content = models.TextField(blank=True, null=True)
