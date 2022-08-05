"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, re_path
from application import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.LoginUser.as_view(), name='login'),
    #path('edit/<int:id>', views.edit_delivery, name='edit'),
    re_path('add_wood/', views.add_wood, name='add_wood'),
    re_path('main/', views.main, name='main'),
    re_path('registration/', views.Registr.as_view(), name='registration'),
    re_path('^delivery/', views.delivery, name='delivery'),
    re_path('type/', views.type, name='type'),
    re_path('create_delivery/', views.create_delivery, name='create_delivery'),
    #re_path('create_delivery/<id:int>/<str:type_operation>', views.create_delivery, name='edit_delivery'),
    re_path('balance/', views.balance, name='balance'),
    re_path('add_expenses/', views.add_expenses, name='expenses'),
    re_path('download_expenses/', views.create_report_expenses, name='download_expenses'),
    re_path('download_delivery/', views.create_report_delivery, name='download_delivery'),
    re_path('download_b/', views.create_report_balance, name='download_balance'),
    re_path('download_type_of_wood/', views.create_report_type_of_wood, name='download_type_of_wood'),
    re_path('expenses/', views.expenses, name='expenses')
]
