from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import *

class NewSafetyCheck(ModelForm):
	class Meta:
		model = SafetyCheck
		fields = '__all__'


class NewSafetyForm(ModelForm):
	class Meta:
		model = SafetyForm
		fields = '__all__'
		exclude = ['SafetyCheck']

