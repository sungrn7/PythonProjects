from django.db import models
from jsonfield import JSONField 

class Account(models.Model):
        ids = models.CharField(max_length=128)
        idx = models.IntegerField(default=0)

class dormi_choen(models.Model):
	day = models.CharField(max_length=128)
	content = models.TextField(blank=True, null=True)

	def __unicode__(self):
		return u'%s %s' % (self.day, self.content)

class school_choen(models.Model):
	day = models.CharField(max_length=128)
	content = models.TextField(blank=True, null=True)	

	def __unicode__(self):
		return u'%s %s' % (self.day, self.content)

class staff_choen(models.Model):
	day = models.CharField(max_length=128)
	content = models.TextField(blank=True, null=True)

	def __unicode__(self):
		return u'%s %s' % (self.day, self.content)

class school_yesan(models.Model):
	day = models.CharField(max_length=128)
	content = models.TextField(blank=True, null=True)	

	def __unicode__(self):	
		return u'%s %s' % (self.day, self.content)

class staff_yesan(models.Model):
	day = models.CharField(max_length=128)
	content = models.TextField(blank=True, null=True)

	def __unicode__(self):
		return u'%s %s' % (self.day, self.content)

class dreem_singwan(models.Model):
	day = models.CharField(max_length=128)
	content = models.TextField(blank=True, null=True)

	def __unicode__(self):
		return u'%s %s' % (self.day, self.content)

class bision_singwan(models.Model):
	day = models.CharField(max_length=128)
	content = models.TextField(blank=True, null=True)

	def __unicode__(self):
		return u'%s %s' % (self.day, self.content)

class school_singwan(models.Model):
	day = models.CharField(max_length=128)
	content = models.TextField(blank=True, null=True)

	def __unicode__(self):
		return u'%s %s' % (self.day, self.content)

class staff_singwan(models.Model):
	day = models.CharField(max_length=128)
	content = models.TextField(blank=True, null=True)

	def __unicode__(self):
		return u'%s %s' % (self.day, self.content)


