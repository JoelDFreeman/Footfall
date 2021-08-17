from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import *

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter SafetyForms by day
	def formatday(self, day, SafetyForms):
		SafetyForms_per_day = SafetyForms.filter(date_created=day)
		d = ''
		for SafetyForm in SafetyForms_per_day:
			d += f'<li> {SafetyForm.title} </li>'

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	# formats a week as a tr 
	def formatweek(self, theweek, SafetyForms):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, SafetyForms)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter SafetyForms by year and month
	def formatmonth(self, withyear=True):
		SafetyForms = SafetyForm.objects.filter(date_created__year=self.year, date_created__month=self.month)

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, SafetyForms)}\n'
		return cal