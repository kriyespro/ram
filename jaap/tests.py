from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import JaapSession, JaapCount

class JaapSessionModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Create a sample JaapSession
        self.session = JaapSession.objects.create(
            user=self.user,
            ram_count=108,
            timer_set=15,
            target_count=1000,
            status='in_progress'
        )
    
    def test_session_creation(self):
        """Test that the JaapSession is created correctly"""
        self.assertEqual(self.session.user, self.user)
        self.assertEqual(self.session.ram_count, 108)
        self.assertEqual(self.session.timer_set, 15)
        self.assertEqual(self.session.target_count, 1000)
        self.assertEqual(self.session.status, 'in_progress')
        self.assertIsNone(self.session.completed_at)
    
    def test_string_representation(self):
        """Test the string representation of the JaapSession"""
        expected_str = f"{self.user.username}'s Session on {self.session.created_at.strftime('%Y-%m-%d %H:%M')}"
        self.assertEqual(str(self.session), expected_str)
    
    def test_ordering(self):
        """Test that sessions are ordered by created_at (newest first)"""
        # Create another session that's older
        older_time = timezone.now() - timedelta(days=1)
        older_session = JaapSession.objects.create(
            user=self.user,
            ram_count=50,
            status='completed',
            completed_at=older_time
        )
        older_session.created_at = older_time
        older_session.save()
        
        # Create a newer session
        newer_session = JaapSession.objects.create(
            user=self.user,
            ram_count=25,
            status='in_progress'
        )
        
        # Get all sessions ordered
        sessions = JaapSession.objects.all()
        
        # Newest should be first
        self.assertEqual(sessions[0], newer_session)
        self.assertEqual(sessions[1], self.session)
        self.assertEqual(sessions[2], older_session)

class JaapCountModelTest(TestCase):
    def setUp(self):
        # Create the JaapCount singleton
        self.jaap_count = JaapCount.objects.create(id=1, total_count=0)
    
    def test_jaap_count_creation(self):
        """Test that the JaapCount is created correctly"""
        self.assertEqual(self.jaap_count.total_count, 0)
    
    def test_string_representation(self):
        """Test the string representation of the JaapCount"""
        expected_str = f"Total Ram Count: {self.jaap_count.total_count}"
        self.assertEqual(str(self.jaap_count), expected_str)
    
    def test_increment_method(self):
        """Test the increment method works correctly"""
        # Default increment by 1
        count = JaapCount.increment()
        self.assertEqual(count, 1)
        
        # Increment by 5
        count = JaapCount.increment(5)
        self.assertEqual(count, 6)
        
        # Verify the database record was updated
        updated_count = JaapCount.objects.get(id=1)
        self.assertEqual(updated_count.total_count, 6)
    
    def test_singleton_behavior(self):
        """Test that increment creates the object if it doesn't exist"""
        # Delete the existing count
        JaapCount.objects.all().delete()
        
        # Call increment which should recreate with id=1
        count = JaapCount.increment(10)
        self.assertEqual(count, 10)
        
        # Verify there's exactly one object
        self.assertEqual(JaapCount.objects.count(), 1)
        self.assertEqual(JaapCount.objects.first().id, 1)
