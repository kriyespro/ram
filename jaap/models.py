from django.db import models
from django.contrib.auth.models import User
from core.models import TimeStampedModel

class JaapSession(TimeStampedModel):
    """
    Model to track individual Jaap sessions
    """
    TIMER_CHOICES = [
        (5, '5 Minutes'),
        (10, '10 Minutes'),
        (15, '15 Minutes'),
        (30, '30 Minutes'),
        (60, '60 Minutes'),
    ]
    
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jaap_sessions')
    ram_count = models.PositiveIntegerField(default=0)
    timer_set = models.PositiveIntegerField(choices=TIMER_CHOICES, null=True, blank=True)
    target_count = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Session on {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        ordering = ['-created_at']

class JaapCount(TimeStampedModel):
    """
    Model to track the total Ram Jaap counts for all users
    """
    total_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"Total Ram Count: {self.total_count}"
    
    @classmethod
    def increment(cls, count=1):
        """
        Increment the total Ram count
        """
        obj, created = cls.objects.get_or_create(id=1)
        obj.total_count += count
        obj.save()
        return obj.total_count
