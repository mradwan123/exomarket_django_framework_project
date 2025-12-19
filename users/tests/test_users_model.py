from django.test import TestCase
from ..models import User
from django.core.exceptions import ValidationError

class UserModelTest(TestCase):
    
    def test_create_user(self):
        user = User.objects.create(
            username = 'testusername',
            email = 'something@gmail.com',
            password = 'test123',
            phone_number = '222222222',
            bio = 'some texts',
            birth_date = '1976-12-12',
        )
        
        self.assertEqual(user.username, 'testusername')
        self.assertEqual(user.email, 'something@gmail.com')
        self.assertEqual(user.password, 'test123')
        self.assertEqual(user.phone_number, '222222222')
        self.assertEqual(user.bio, 'some texts')
        self.assertEqual(user.birth_date, '1976-12-12')
        
    def test_date_is_wrong_format(self):
        
        with self.assertRaises(ValidationError):
            user = User(birth_date='12-12-12')
            user.full_clean()
            
            
      