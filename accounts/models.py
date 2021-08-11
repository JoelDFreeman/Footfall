from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
from django.conf import settings
from .managers import ProductManager
from datetime import datetime, date
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime


CURRENCY = settings.CURRENCY


class SafetyCheck(models.Model):
	CATEGORY = (
		('Pass', 'Pass'),
		('Fail', 'Fail'),
		) 
	name = models.CharField(default="Address 1", max_length=200, null=True)
	check_notes = models.CharField(max_length=1000, null=True, blank=True)
	category = models.CharField(max_length=200, null=True, choices=CATEGORY)

	def __str__(self):
		return self.name

class SafetyForm(models.Model):
	STATUS = (
		('Pass', 'Pass'),
		('Quarantine', 'Quarantine'),
		('Scrap', 'Scrap'),
		('Pending', 'Pending'),
		)	
	name = models.CharField(max_length=200, null=True)
	description = models.CharField(max_length=200, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	date_completion = models.DateTimeField("Check Completion Due Date (dd/mm/yyyy)",auto_now_add=False, null=True)
	form_note = models.CharField(max_length=1000, null=True, blank=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	SafetyCheck = models.ManyToManyField(SafetyCheck, blank=True)
	

	def __str__(self):
		return self.name

	def __str__(self):
		return self.SafetyCheck	


	
