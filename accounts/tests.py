from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Get the automatically created profile
        self.profile = self.user.profile
    
    def test_profile_creation(self):
        """Test that a UserProfile is automatically created when a User is created"""
        self.assertIsNotNone(self.profile)
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.total_ram_count, 0)
        self.assertEqual(self.profile.total_sessions, 0)
    
    def test_string_representation(self):
        """Test the string representation of the UserProfile"""
        expected_str = f"{self.user.username}'s Profile"
        self.assertEqual(str(self.profile), expected_str)
    
    def test_profile_update(self):
        """Test that the profile can be updated"""
        self.profile.total_ram_count = 108
        self.profile.total_sessions = 5
        self.profile.save()
        
        # Reload from database
        updated_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(updated_profile.total_ram_count, 108)
        self.assertEqual(updated_profile.total_sessions, 5)
    
    def test_profile_signal(self):
        """Test that the profile is automatically created via the signal"""
        # Create a new user, which should trigger the signal to create a profile
        new_user = User.objects.create_user(
            username='newuser',
            email='new@example.com',
            password='newpassword'
        )
        
        # Verify that a profile was created
        self.assertTrue(hasattr(new_user, 'profile'))
        self.assertIsNotNone(new_user.profile)
        self.assertEqual(new_user.profile.total_ram_count, 0)
        self.assertEqual(new_user.profile.total_sessions, 0)
    
    def test_cascade_delete(self):
        """Test that deleting a user also deletes their profile"""
        user_id = self.user.id
        self.user.delete()
        
        # Check that the profile is deleted
        with self.assertRaises(UserProfile.DoesNotExist):
            UserProfile.objects.get(user_id=user_id)
