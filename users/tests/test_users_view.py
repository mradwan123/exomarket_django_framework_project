from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()
from django.urls import reverse

class SessionViewsTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username= 'testuser7',
            password = 'test123',
            email = 'test@gmail.com',
        )
        
        self.home_url = reverse('shop:home')
        self.login_url = reverse('users:login')
        
        
    def test_home_view_no_sessions(self):
        response = self.client.get(self.home_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        
        
    #----- Login_Custom Tests Below:
    
    def test_login_view_get(self):
        'Test if login page loads correctly and gets'
        response = self.client.get(self.login_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, '<form')
        
    def test_login_post_valid_user(self):
        response = self.client.post(self.login_url, {
            'username':'testuser7',
            'password': 'test123'
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('shop:list'))
        
        
        session = self.client.session
        self.assertEqual(session.get('user_id'), self.user.id)
        
    def test_login_post_invalid_user(self):
        response = self.client.post(self.login_url, {})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTemplateNotUsed(response, 'wrong_template.html')

        
    # def test_not_post(self):
    #     response = self.client 
    #     self.assertTemplateUsed(response, 'login.html')

    def test_login_with_wrong_password(self):
        """Test login with correct username but wrong password"""
        response = self.client.post(self.login_url, {
            'username': 'testuser7',
            'password': 'wrongpassword'
        })
    
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:login'))
        # User should NOT be logged in
        self.assertNotIn('_auth_user_id', self.client.session)
