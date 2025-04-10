from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages
from django.db.models import Sum
from .models import JaapSession, JaapCount
from .forms import JaapInputForm, JaapSessionForm
import re

@login_required
def jaap_input_view(request):
    """
    View for Ram Naam Jaap input form
    """
    form = JaapInputForm()
    
    # Get active session if exists
    active_session = JaapSession.objects.filter(
        user=request.user, 
        status__in=['in_progress', 'paused']
    ).first()
    
    context = {
        'form': form,
        'active_session': active_session,
    }
    
    return render(request, 'jaap/input.html', context)

@login_required
def jaap_submit_view(request):
    """
    Handle Jaap form submission via AJAX
    """
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        jaap_text = request.POST.get('jaap_text', '')
        timer = request.POST.get('timer', '')
        target = request.POST.get('target', '')
        session_id = request.POST.get('session_id', '')
        ram_count = request.POST.get('ram_count', 0)
        status = request.POST.get('status', 'completed')
        
        try:
            ram_count = int(ram_count)
        except ValueError:
            ram_count = 0
        
        # Skip processing if ram_count is 0 and not a completed session
        if ram_count == 0 and status != 'completed':
            return JsonResponse({'status': 'error', 'message': 'No Ram count to save'})
        
        # Update or create session
        if session_id and session_id != '0':
            try:
                session = JaapSession.objects.get(id=session_id, user=request.user)
                
                # Only update if the current count is greater than saved count
                # to prevent losing progress when refreshing page
                if ram_count > session.ram_count:
                    # Calculate the incremental count
                    increment = ram_count - session.ram_count
                    session.ram_count = ram_count
                    session.status = status
                    
                    if status == 'completed':
                        session.completed_at = timezone.now()
                        
                        # Update user profile stats with the incremental count
                        profile = request.user.profile
                        profile.total_ram_count += increment
                        if status == 'completed':
                            profile.total_sessions += 1
                        profile.save()
                        
                        # Update global ram count with incremental count
                        JaapCount.increment(increment)
                    
                    session.save()
                
            except JaapSession.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Invalid session'})
        else:
            # Create new session
            session = JaapSession(
                user=request.user,
                ram_count=ram_count,
                status=status
            )
            
            if timer:
                session.timer_set = int(timer)
                
            if target:
                session.target_count = int(target)
            
            if status == 'completed':
                session.completed_at = timezone.now()
                
                # Update user profile stats
                profile = request.user.profile
                profile.total_ram_count += ram_count
                profile.total_sessions += 1
                profile.save()
                
                # Update global ram count
                JaapCount.increment(ram_count)
            
            session.save()
        
        return JsonResponse({'status': 'success', 'session_id': session.id})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@login_required
def jaap_resume_view(request, session_id):
    """
    Resume a paused Jaap session
    """
    session = get_object_or_404(JaapSession, id=session_id, user=request.user)
    
    if session.status == 'completed':
        messages.warning(request, 'This session is already completed.')
        return redirect('dashboard')
    
    form = JaapInputForm()
    
    context = {
        'form': form,
        'active_session': session,
    }
    
    return render(request, 'jaap/input.html', context)

def leaderboard_view(request):
    """
    View for the global leaderboard
    """
    from accounts.models import UserProfile
    
    # Get top users by ram count
    top_users = UserProfile.objects.order_by('-total_ram_count')[:20]
    
    # Get global ram count
    try:
        total_ram_count = JaapCount.objects.get(id=1).total_count
    except JaapCount.DoesNotExist:
        total_ram_count = 0
    
    context = {
        'top_users': top_users,
        'total_ram_count': total_ram_count,
    }
    
    return render(request, 'jaap/leaderboard.html', context)

@login_required
def count_ram_view(request):
    """
    AJAX view to count Ram occurrences in text
    """
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        text = request.POST.get('text', '')
        
        # Count occurrences of "ram" (case insensitive)
        count = len(re.findall(r'\bram\b', text.lower()))
        
        return JsonResponse({'count': count})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
