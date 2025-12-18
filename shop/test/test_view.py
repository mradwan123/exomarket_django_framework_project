from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()
from django.urls import reverse

class SessionViewsTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username= 'testuser',
            password = 'test123',
            email = 'tet@gmail.com',
        )
        
        self.home_url = reverse('shop:home')
        self.login_url = reverse('users:login')
        
        
    def test_home_view_no_sessions(self):
        response = self.client.get(self.home_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
