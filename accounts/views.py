import csv
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import *
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime
from django.contrib import messages
from accounts.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from .filters import *
from .models import *
from .forms import *
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .utils import Calendar
from django.views import generic
from django.utils.safestring import mark_safe

class CalendarView(generic.ListView):
    model = SafetyForm
    template_name = 'accounts/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = datetime.now()

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context

@login_required(login_url='login')
def form_create(request):
	form = form_create(request.POST or None)
	if form.is_valid():
		form.save()
	
	context = {
		'form': form
	} 	
	return render(request,"accounts/form_create.html", context)

@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def home(request):
	formview = SafetyForm.objects.all()
	

	total_forms = formview.count()

	Pass = formview.filter(status='Pass').count()
	Quarantine = formview.filter(status='Quarantine').count()
	Scrap = formview.filter(status='Scrap').count()
	Pending = formview.filter(status='Pending').count()

	page = request.GET.get('page', 1)
	

	paginator = Paginator(formview, 5)	
	try:
		formview = paginator.page(page)
	except PageNotAnInteger:
		formview = paginator.page(1)
	except EmptyPage:
		formview= paginator.page(paginator.num_pages)

	

	context = {'formview':formview,'total_forms':total_forms,'Pass':Pass,
	'Quarantine':Quarantine, 'Scrap':Scrap, 'Pending':Pending, 'paginator':paginator}

	return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
def formview(request):
	formview = SafetyForm.objects.all()
	

	total_forms = formview.count()

	myFilter = SafetyFormFilter(request.GET, queryset=SafetyForm)
	formview = myFilter.qs 

	form = NewSafetyForm()
	if request.method == 'POST':
		form = NewSafetyForm(request.POST)
		if form.is_valid():
			user = form.save()
			
			messages.success(request, 'Form Created ')

			return redirect('login')
	Pass = formview.filter(status='Pass').count()
	Scrap = formview.filter(status='Scrap').filter(status='Quarantine').count()
	Quarantine = formview.filter(status='Quarantine').count()
	Pending = formview.filter(status='Pending').count()

		 
	
	page = request.GET.get('page', 1)

	paginator = Paginator(formview, 5)	
	try:
		formview = paginator.page(page)
	except PageNotAnInteger:
		formview = paginator.page(1)
	except EmptyPage:
		formview= paginator.page(paginator.num_pages)

	

	context = {'formview':formview,'total_forms':total_forms,'Pass':Pass, 'myFilter':myFilter,
	'Scrap':Scrap, 'Quarantine':Quarantine, 'Pending':Pending, 'paginator':paginator}

	return render(request, 'accounts/formview.html', context)

@login_required(login_url='login')
def forms(request):
	formview = SafetyForm.objects.all()

	myFilter = SafetyFormFilter(request.GET, queryset=formview)
	formview = myFilter.qs 

	page = request.GET.get('page', 1)

	paginator = Paginator(formview, 10)	
	try:
		formview = paginator.page(page)
	except PageNotAnInteger:
		formview = paginator.page(1)
	except EmptyPage:
		formview= paginator.page(paginator.num_pages)

	context = {
		'formview':formview, 'myFilter':myFilter,'paginator':paginator
	}
	return render(request, 'accounts/forms.html', context)

@login_required(login_url='login')
def form_delete(request, pk):
	safetyform = SafetyForm.objects.get(id=pk)
	if request.method == "POST":
		safetyform.delete()
		return redirect('/')

	context = {'item':safetyform}
	return render(request, 'accounts/delete.html', context)

@login_required(login_url='login')
def form_create(request):
	form = NewSafetyForm(request.POST or None)
	if form.is_valid():
		form.save()
	
	context = {
		'form': form,
	} 	
	return render(request,"accounts/form_create.html", context)

def download_csv(request):
 
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Formview.csv"' # your filename
 
    writer = csv.writer(response)
    writer.writerow([
			'name',
			'description',
			'form_note',
			'status',
			'user',
			'date_completion',
			'SafetyCheck',
			])
 
    safetyForms = SafetyForm.objects.all().values_list(
			'name',
			'description',
			'form_note',
			'status',
			'user',
			'date_completion',
			'SafetyCheck',
	)
 
    for safetyForm in safetyForms:
        writer.writerow(safetyForm)
 
     
    return response


@login_required(login_url='login')
def user(request):

	forms= request.user.formview.order_set.all()

	total_forms = forms.count()

	print('FORMS:', forms)

	context = {'forms':forms, 'total_forms':total_forms}
	return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
def accountSettings(request):

	return render(request, 'accounts/account_settings.html')

@login_required(login_url='login')
def calendar(request):

	# get current year
	now = datetime.now()
	current_year = now.year

	# cal = HTMLCalendar().formatmonth(
		# year,
		# month)

	context= {"current_year":current_year}

	return render(request, 'accounts/calendar.html', context)


@login_required(login_url='login')
def safetyform(request, pk_test):
	safetyform = SafetyForm.objects.get(id=pk_test)
	form = NewSafetyForm(instance=safetyform)

	safety_checks = safetyform.SafetyCheck.all()

	safety_check_forms = []
	for sc in safety_checks:
		safety_check_forms.append(NewSafetyCheck(instance=sc))

	if request.method == 'POST':

		form = NewSafetyForm(request.POST, instance=safetyform)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form, 'safety_checks': safety_check_forms}
	return render(request, 'accounts/safetyform.html', context)	

@login_required(login_url='login')
def check_create(request):
	form = NewSafetyCheck(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('/form_create')

	context = {
		'form': form
	} 	
	return render(request,"accounts/check_create.html", context)

@login_required(login_url='login')
def check_update(request, pk):
	safetycheck = SafetyCheck.objects.get(id=pk)
	form = NewSafetyCheck(instance=SafetyCheck)
	print('SAFETYCHECK:', SafetyCheck)
	if request.method == 'POST':

		form = NewSafetyCheck(request.POST, instance=SafetyCheck)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/check_create.html', context)

@login_required(login_url='login')
def check_delete(request, pk):
	safetycheck = SafetyCheck.objects.get(id=pk)
	if request.method == "POST":
		safetycheck.delete()
		return redirect('/')

	context = {'item':safetycheck}
	return render(request, 'accounts/delete.html', context)				