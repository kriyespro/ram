from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import TimeStampedModel

class UserProfile(TimeStampedModel):
    """
    User profile model to store additional user information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    total_ram_count = models.PositiveIntegerField(default=0)
    total_sessions = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update user profile when User object changes
    """
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.profile.save()
