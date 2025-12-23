from django.test import TestCase
from ..models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError

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

    def test_password_hashing(self):        
        user = User.objects.create_user(username='bob', password='plain')
        self.assertNotEqual(user.password, 'plain')
        self.assertTrue(user.check_password('plain'))       

    def test_username_unique_constraint(self): #Abstractuser class includes by default unique username
        User.objects.create_user(username='george', email='a@gmail.com', password='p')
        with self.assertRaises(IntegrityError):
            User.objects.create_user(username='george', email='g@gmail.com', password='p')

    def test_email_unique_constraint(self): #Abstractuser class includes by default unique username
        User.objects.create_user(username='george', email='george@gmail.com', password='p')
        with self.assertRaises(IntegrityError):
            User.objects.create_user(username='radwan', email='george@gmail.com', password='p')

    def test_email_blank(self): #Abstractuser class includes by default unique username
        User.objects.create_user(username='george', password='p')
        with self.assertRaises(IntegrityError):
            User.objects.create_user(username='radwan', password='p')

    def test_blank_bio_phonenumber(self):    
        user = User.objects.create_user(username='carl')
        self.assertIsNone(user.bio)          # because `blank=True, null=True`
        self.assertIsNone(user.phone_number)

    def test_number_format(self): #after adding regex to model, now can test format
        user = User(phone_number='number format invalid!')
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_phonenumber_length(self): #should raise error for more than 20
        user = User(phone_number='+22222222222222222222222222222222222')
        with self.assertRaises(ValidationError):
            user.full_clean()

