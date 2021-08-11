from os import name, stat_result
from django.forms import ModelForm, widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import date, datetime
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime


from .models import *

class NewSafetyCheck(forms.ModelForm):
	class Meta:
		model = SafetyCheck
		fields = [
			'name',
			'check_notes',
			'category',
		]





class NewSafetyForm(forms.ModelForm):
	class Meta:
		model = SafetyForm
		fields = [
			'name',
			'description',
			'form_note',
			'status',
			'user',
			'date_completion',
			'SafetyCheck',
			
		]

		name = label='Enter Form Name' 