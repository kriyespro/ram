from django.urls import path
from . import views

urlpatterns = [
    path('input/', views.jaap_input_view, name='jaap_input'),
    path('submit/', views.jaap_submit_view, name='jaap_submit'),
    path('resume/<int:session_id>/', views.jaap_resume_view, name='jaap_resume'),
    path('count/', views.count_ram_view, name='count_ram'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
] 