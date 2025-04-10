from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile

class AuthenticationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.dashboard_url = reverse('dashboard')
        self.jaap_input_url = reverse('jaap_input')
        
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
    
    def test_register_page_loads(self):
        """Test that the register page loads correctly"""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
    
    def test_user_registration(self):
        """Test user registration process"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'securepassword123',
            'password2': 'securepassword123'
        }
        
        response = self.client.post(self.register_url, data, follow=True)
        
        # Should redirect to jaap_input (not dashboard) after successful registration
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.jaap_input_url)
        
        # Check that the user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
        # Check that the user is logged in
        self.assertTrue(response.context['user'].is_authenticated)
        
        # Check that a profile was created
        new_user = User.objects.get(username='newuser')
        self.assertTrue(hasattr(new_user, 'profile'))
    
    def test_login_page_loads(self):
        """Test that the login page loads correctly"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
    
    def test_user_login(self):
        """Test user login process"""
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        
        response = self.client.post(self.login_url, data, follow=True)
        
        # Should redirect to jaap_input (not dashboard) after successful login
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.jaap_input_url)
        
        # Check that the user is logged in
        self.assertTrue(response.context['user'].is_authenticated)
    
    def test_invalid_login(self):
        """Test login with invalid credentials"""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(self.login_url, data)
        
        # Should not redirect
        self.assertEqual(response.status_code, 200)
        
        # Should stay on login page
        self.assertTemplateUsed(response, 'accounts/login.html')
        
        # Check that an error message is displayed
        self.assertContains(response, "Please enter a correct username and password")
    
    def test_logout(self):
        """Test user logout"""
        # Login first
        self.client.login(username='testuser', password='testpassword')
        
        # Verify logged in
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        
        # Now logout
        response = self.client.get(self.logout_url, follow=True)
        
        # Should redirect to home page
        self.assertRedirects(response, reverse('home'))
        
        # Verify logged out - dashboard should redirect to login
        response = self.client.get(self.dashboard_url)
        login_url_with_next = f"{self.login_url}?next={self.dashboard_url}"
        self.assertRedirects(response, login_url_with_next)
    
    def test_dashboard_authenticated(self):
        """Test that authenticated users can access the dashboard"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/dashboard.html')
    
    def test_dashboard_unauthenticated(self):
        """Test that unauthenticated users are redirected to login"""
        response = self.client.get(self.dashboard_url)
        login_url_with_next = f"{self.login_url}?next={self.dashboard_url}"
        self.assertRedirects(response, login_url_with_next) 