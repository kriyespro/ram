from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Sum
from jaap.models import JaapCount, JaapSession
from accounts.models import UserProfile

def home(request):
    """
    Home page view that shows a landing page with stats and leaderboard.
    """
    # Get total users count
    total_users = User.objects.count()
    
    # Get total Ram count
    try:
        total_ram_count = JaapCount.objects.get(id=1).total_count
    except JaapCount.DoesNotExist:
        total_ram_count = 0
    
    # Get top 5 users for leaderboard
    top_users = UserProfile.objects.order_by('-total_ram_count')[:5]
    
    context = {
        'total_users': total_users,
        'total_ram_count': total_ram_count,
        'top_users': top_users,
    }
    
    return render(request, 'core/home.html', context)

def about(request):
    """
    About page view.
    """
    return render(request, 'core/about.html')

def global_stats_context(request):
    """
    Context processor to add global stats to all templates.
    """
    # Get total users count
    total_users = User.objects.count()
    
    # Get total Ram count
    try:
        total_ram_count = JaapCount.objects.get(id=1).total_count
    except JaapCount.DoesNotExist:
        total_ram_count = 0
        
    return {
        'total_users': total_users,
        'total_ram_count': total_ram_count,
    }
