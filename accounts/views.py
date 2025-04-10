from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import UserProfile
from jaap.models import JaapSession

def register_view(request):
    """
    User registration view
    """
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('jaap_input')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    """
    User login view
    """
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('jaap_input')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    """
    User logout view
    """
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

@login_required
def dashboard_view(request):
    """
    User dashboard view showing statistics and history
    """
    profile = request.user.profile
    
    # Get user's recent jaap sessions
    recent_sessions = JaapSession.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # Get user's stats
    total_sessions = profile.total_sessions
    total_ram_count = profile.total_ram_count
    
    # Get all sessions for history
    all_sessions = JaapSession.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'profile': profile,
        'recent_sessions': recent_sessions,
        'total_sessions': total_sessions,
        'total_ram_count': total_ram_count,
        'all_sessions': all_sessions
    }
    
    return render(request, 'accounts/dashboard.html', context)

@login_required
def profile_view(request):
    """
    User profile view
    """
    return render(request, 'accounts/profile.html', {'profile': request.user.profile})
