from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from django.contrib import messages
from jaap.models import JaapSession, JaapCount
from accounts.models import UserProfile
from datetime import timedelta
from django.conf import settings

def is_staff(user):
    """Check if user is staff"""
    return user.is_staff

@login_required
@user_passes_test(is_staff)
def admin_dashboard(request):
    """
    Custom admin dashboard view for staff users
    """
    # Get counts
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    staff_users = User.objects.filter(is_staff=True).count()
    
    # Get Ram counts
    try:
        total_ram_count = JaapCount.objects.get(id=1).total_count
    except JaapCount.DoesNotExist:
        total_ram_count = 0
    
    # Get session stats
    total_sessions = JaapSession.objects.count()
    active_sessions = JaapSession.objects.filter(status='in_progress').count()
    completed_sessions = JaapSession.objects.filter(status='completed').count()
    
    # Get today's stats
    today = timezone.now().date()
    today_start = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
    today_end = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.max.time()))
    
    today_users = User.objects.filter(date_joined__range=(today_start, today_end)).count()
    today_sessions = JaapSession.objects.filter(created_at__range=(today_start, today_end)).count()
    
    # Get weekly stats
    week_ago = today - timedelta(days=7)
    week_start = timezone.make_aware(timezone.datetime.combine(week_ago, timezone.datetime.min.time()))
    
    weekly_users = User.objects.filter(date_joined__range=(week_start, today_end)).count()
    weekly_sessions = JaapSession.objects.filter(created_at__range=(week_start, today_end)).count()
    
    # Get leaderboard
    top_users = UserProfile.objects.order_by('-total_ram_count')[:10]
    
    # Get recent users and sessions
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_sessions = JaapSession.objects.select_related('user').order_by('-created_at')[:5]
    
    context = {
        'page_title': 'Admin Dashboard',
        'total_users': total_users,
        'active_users': active_users,
        'staff_users': staff_users,
        'total_ram_count': total_ram_count,
        'total_sessions': total_sessions,
        'active_sessions': active_sessions,
        'completed_sessions': completed_sessions,
        'today_users': today_users,
        'today_sessions': today_sessions,
        'weekly_users': weekly_users,
        'weekly_sessions': weekly_sessions,
        'top_users': top_users,
        'recent_users': recent_users,
        'recent_sessions': recent_sessions,
    }
    
    return render(request, 'admin_dashboard/dashboard.html', context)

@login_required
@user_passes_test(is_staff)
def user_management(request):
    """
    User management view for admin
    """
    users = User.objects.all().order_by('-date_joined')
    
    context = {
        'page_title': 'User Management',
        'users': users,
    }
    
    return render(request, 'admin_dashboard/users.html', context)

@login_required
@user_passes_test(is_staff)
def jaap_stats(request):
    """
    Detailed Jaap statistics for admin
    """
    # Get general stats
    total_sessions = JaapSession.objects.count()
    total_ram_count = JaapCount.objects.get(id=1).total_count if JaapCount.objects.exists() else 0
    avg_rams_per_session = JaapSession.objects.filter(status='completed').aggregate(avg=Avg('ram_count'))['avg'] or 0
    
    # Get stats by time periods
    today = timezone.now().date()
    today_start = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
    today_end = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.max.time()))
    
    today_sessions = JaapSession.objects.filter(created_at__range=(today_start, today_end)).count()
    today_ram_count = JaapSession.objects.filter(created_at__range=(today_start, today_end)).aggregate(sum=Sum('ram_count'))['sum'] or 0
    
    # Weekly stats
    week_ago = today - timedelta(days=7)
    week_start = timezone.make_aware(timezone.datetime.combine(week_ago, timezone.datetime.min.time()))
    
    weekly_sessions = JaapSession.objects.filter(created_at__range=(week_start, today_end)).count()
    weekly_ram_count = JaapSession.objects.filter(created_at__range=(week_start, today_end)).aggregate(sum=Sum('ram_count'))['sum'] or 0
    
    # Monthly stats
    month_ago = today - timedelta(days=30)
    month_start = timezone.make_aware(timezone.datetime.combine(month_ago, timezone.datetime.min.time()))
    
    monthly_sessions = JaapSession.objects.filter(created_at__range=(month_start, today_end)).count()
    monthly_ram_count = JaapSession.objects.filter(created_at__range=(month_start, today_end)).aggregate(sum=Sum('ram_count'))['sum'] or 0
    
    context = {
        'page_title': 'Jaap Statistics',
        'total_sessions': total_sessions,
        'total_ram_count': total_ram_count,
        'avg_rams_per_session': int(avg_rams_per_session),
        'today_sessions': today_sessions,
        'today_ram_count': today_ram_count,
        'weekly_sessions': weekly_sessions,
        'weekly_ram_count': weekly_ram_count,
        'monthly_sessions': monthly_sessions,
        'monthly_ram_count': monthly_ram_count,
    }
    
    return render(request, 'admin_dashboard/jaap_stats.html', context)

@login_required
@user_passes_test(is_staff)
def system_info(request):
    """
    System information view for admin
    """
    import platform
    import django
    import sys
    import os
    
    context = {
        'page_title': 'System Information',
        'python_version': platform.python_version(),
        'django_version': django.get_version(),
        'platform_info': platform.platform(),
        'time_zone': timezone.get_current_timezone_name(),
        'system_info': platform.system(),
        'processor_info': platform.processor(),
        'memory_info': 'Not available',  # Would require psutil which might not be installed
        'deployment_info': 'Development Server' if settings.DEBUG else 'Production Server'
    }
    
    return render(request, 'admin_dashboard/system_info.html', context)
