from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.admin_dashboard, name='dashboard'),
    path('users/', views.user_management, name='users'),
    path('jaap-stats/', views.jaap_stats, name='jaap_stats'),
    path('system-info/', views.system_info, name='system_info'),
] 