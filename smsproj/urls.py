"""smsproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from smsapp import views
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name="home"),
    path('', views.home, name="home"),
    path('newrecord/', views.createrecord, name="createrecord"),
    path('recordlist/', views.recordlist, name="recordlist"),
    path('grouplist/', views.grouplist, name="grouplist"),
    path('newbmessagecat/', views.createbmessagecat, name="createbmessagecat"),
    path('newbmessagedis/', views.createbmessagedis, name="createbmessagedis"),
    path('newgroup/', views.creategroup, name="creategroup"),
    path('newmesstemp/', views.messtemp, name="messtemp"),
    path('templatelist/', views.templatelist, name="templatelist"),
    path('deliverylist/', views.deliverylist, name="deliverylist"),
    path('bcriteria/', views.bcriteria, name="bcriteria"),

    path('ajax/load-grades/', views.load_grades, name='ajax_load_grades'),
    path('ajax/validate_empnumber/', views.validate_empnumber, name='validate_empnumber'),
    
    path('updaterecord/<str:pk>/', views.updaterecord, name="updaterecord"),
    path('recordsupdate/<str:pk>/', views.records_update, name="recordsupdate"),
    path('record_create/', views.record_create, name="record_create"),
    path('trying/', views.trying, name='trying'),
    
    
    
    
    #paths for the users app
    path('register/', user_views.register, name="register"),
    path('login/', user_views.loginpage, name="login"),
    path('logout/', user_views.logoutuser, name="logoutuser"),
]

admin.site.site_header = "Welcome to Western North Regional Health Directorate SMS Portal"
admin.site.site_title = "WN-RHD Admin Portal"
admin.site.index_title = "WNR-SMSApp Admin"
