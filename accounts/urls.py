from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),

    path('', views.home, name="home"),
    path('user/', views.user, name="user"),
    path('account/', views.accountSettings, name="account"),

    path('form_create/', views.form_create, name='form_create'),
    path('form_delete/<str:pk>/', views.form_delete, name="form_delete"),
    path('formview/', views.formview, name="formview"),
    path('safetyform/<str:pk_test>/', views.safetyform, name="safetyform"),

    path('callendar', views.callendar, name="callendar"),
    
    path('export/',views.download_csv,name='export'),
    
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)