from django.test import TestCase
from ..models import User

class UserModelTest(TestCase):
    
    def test_create_user(self):
        user = User.objects.create(
            username = 'testusername',
            email = 'something@gmail.com',
            password = 'test123',
            phone_number = '222222222',
            bio = 'some texts',
            birth_date = 12/12/1976,
        )
        
        self.assertEqual(user.phone_number, '222222222')
        self.assertEqual(user.bio, 'some texts')