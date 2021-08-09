import csv
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import *
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from accounts.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from .filters import *
from .models import *
from .forms import *
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required(login_url='login')
@admin_only
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
@admin_only
def home(request):
	formview = SafetyForm.objects.all()
	

	total_forms = formview.count()

	Pass = formview.filter(status='Pass').count()
	Quarantine = formview.filter(status='Quarantine').count()
	Scrap = formview.filter(status='Scrap').count()
	page = request.GET.get('page', 1)
	

	paginator = Paginator(formview, 5)	
	try:
		formview = paginator.page(page)
	except PageNotAnInteger:
		formview = paginator.page(1)
	except EmptyPage:
		formview= paginator.page(paginator.num_pages)

	

	context = {'formview':formview,'total_forms':total_forms,'Pass':Pass,
	'Quarantine':Quarantine, 'Scrap':Scrap, 'paginator':paginator}

	return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@admin_only
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

		 
	
	page = request.GET.get('page', 1)

	paginator = Paginator(formview, 5)	
	try:
		formview = paginator.page(page)
	except PageNotAnInteger:
		formview = paginator.page(1)
	except EmptyPage:
		formview= paginator.page(paginator.num_pages)

	

	context = {'formview':formview,'total_forms':total_forms,'Pass':Pass, 'myFilter':myFilter,
	'Scrap':Scrap, 'Quarantine':Quarantine, 'paginator':paginator}

	return render(request, 'accounts/formview.html', context)

@login_required(login_url='login')
def form_create(request):
	form = NewSafetyForm(request.POST or None)
	if form.is_valid():
		form.save()
	
	context = {
		'form': form
	} 	
	return render(request,"accounts/form_create.html", context)

@login_required(login_url='login')
def form_delete(request, pk):
	safetyform = SafetyForm.objects.get(id=pk)
	if request.method == "POST":
		safetyform.delete()
		return redirect('/')

	context = {'item':safetyform}
	return render(request, 'accounts/form_delete.html', context)

def download_csv(request):
 
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Formview.csv"' # your filename
 
    writer = csv.writer(response)
    writer.writerow(['name','phone'])
 
    form = Form.objects.all().values_list('name','phone')
 
    for form in forms:
        writer.writerow(form)
 
     
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
def callendar(request):

	return render(request, 'accounts/callendar.html')


@login_required(login_url='login')
def safetyform(request, pk_test):
	safetyform = SafetyForm.objects.get(id=pk_test)
	form = NewSafetyForm(instance=safetyform)

	if request.method == 'POST':

		form = NewSafetyForm(request.POST, instance=safetyform)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/safetyform.html', context)	