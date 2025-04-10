from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import JaapSession, JaapCount
import json

class JaapFunctionalityTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.jaap_input_url = reverse('jaap_input')
        self.jaap_count_url = reverse('count_ram')
        self.increment_url = reverse('jaap_submit')
        self.leaderboard_url = reverse('leaderboard')
        
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Create the global Ram count
        self.global_count = JaapCount.objects.create(id=1, total_count=0)
        
        # Login the user
        self.client.login(username='testuser', password='testpassword')
    
    def test_jaap_input_page_loads(self):
        """Test that the Jaap input page loads correctly"""
        response = self.client.get(self.jaap_input_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jaap/input.html')
    
    def test_jaap_input_unauthenticated(self):
        """Test that unauthenticated users are redirected to login"""
        self.client.logout()
        response = self.client.get(self.jaap_input_url)
        login_url_with_next = f"{reverse('login')}?next={self.jaap_input_url}"
        self.assertRedirects(response, login_url_with_next)
    
    def test_session_creation(self):
        """Test creating a new Jaap session"""
        data = {
            'timer': '15',
            'target': '1000'
        }
        
        response = self.client.post(self.jaap_input_url, data, follow=True)
        
        # Should redirect to jaap_count page
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.jaap_count_url)
        
        # Check that a session was created
        self.assertTrue(JaapSession.objects.filter(user=self.user).exists())
        session = JaapSession.objects.get(user=self.user)
        self.assertEqual(session.timer_set, 15)
        self.assertEqual(session.target_count, 1000)
        self.assertEqual(session.status, 'in_progress')
    
    def test_increment_ram_count(self):
        """Test incrementing the Ram count"""
        # Create a session first
        session = JaapSession.objects.create(
            user=self.user,
            ram_count=0,
            timer_set=15,
            target_count=1000,
            status='in_progress'
        )
        
        # AJAX request to increment count
        data = {'ram_text': 'Ram Ram Ram'}
        response = self.client.post(
            self.increment_url,
            json.dumps(data),
            content_type='application/json'
        )
        
        # Check response
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['count'], 3)
        
        # Check that session was updated
        session.refresh_from_db()
        self.assertEqual(session.ram_count, 3)
        
        # Check that global count was updated
        global_count = JaapCount.objects.get(id=1)
        self.assertEqual(global_count.total_count, 3)
        
        # Check user profile was updated
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.total_ram_count, 3)
    
    def test_invalid_input_not_counted(self):
        """Test that invalid inputs are not counted"""
        # Create a session first
        session = JaapSession.objects.create(
            user=self.user,
            ram_count=0,
            timer_set=15,
            target_count=1000,
            status='in_progress'
        )
        
        # AJAX request with invalid text
        data = {'ram_text': 'Hello World'}
        response = self.client.post(
            self.increment_url,
            json.dumps(data),
            content_type='application/json'
        )
        
        # Check response
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['count'], 0)
        
        # Check that session was not updated
        session.refresh_from_db()
        self.assertEqual(session.ram_count, 0)
    
    def test_auto_formatting(self):
        """Test that inputs are auto-formatted correctly"""
        # Create a session first
        session = JaapSession.objects.create(
            user=self.user,
            ram_count=0,
            timer_set=15,
            target_count=1000,
            status='in_progress'
        )
        
        # Test different variations
        variations = [
            'ram', 'RAM', 'rAm', 'raM',  # Case variations
            'राम', 'राम राम',  # Hindi
            'ram ram ram'  # Multiple
        ]
        
        expected_counts = [1, 1, 1, 1, 1, 2, 3]
        total_count = 0
        
        for i, text in enumerate(variations):
            data = {'ram_text': text}
            response = self.client.post(
                self.increment_url,
                json.dumps(data),
                content_type='application/json'
            )
            
            response_data = json.loads(response.content)
            total_count += expected_counts[i]
            self.assertEqual(response_data['count'], total_count)
    
    def test_leaderboard_page_loads(self):
        """Test that the leaderboard page loads correctly"""
        response = self.client.get(self.leaderboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jaap/leaderboard.html')
    
    def test_session_completion(self):
        """Test that a session can be completed"""
        # Create a session first
        session = JaapSession.objects.create(
            user=self.user,
            ram_count=995,
            timer_set=15,
            target_count=1000,
            status='in_progress'
        )
        
        # AJAX request to increment past target
        data = {'ram_text': 'Ram Ram Ram Ram Ram Ram'}
        response = self.client.post(
            self.increment_url,
            json.dumps(data),
            content_type='application/json'
        )
        
        # Check response
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['count'], 1001)
        self.assertTrue(response_data['target_reached'])
        
        # Check that session was marked as completed
        session.refresh_from_db()
        self.assertEqual(session.status, 'completed')
        self.assertIsNotNone(session.completed_at) 