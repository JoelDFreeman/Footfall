import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class SafetyFormFilter(django_filters.FilterSet):
	start_date = DateFilter(field_name="date_created", lookup_expr='gte')
	end_date = DateFilter(field_name="date_completion", lookup_expr='lte')
	note = CharFilter(field_name='form_note', lookup_expr='icontains')


	class Meta:
		model = SafetyForm
		fields = '__all__'
		exclude = [
			"date_created",
			'description',
			'form_note',
			'date_completion',
			'SafetyCheck',]		




				