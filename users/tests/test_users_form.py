from django.test import TestCase
from django.contrib.auth import get_user_model
from ..forms import UserForm
from ..models import User

class UserFormTests(TestCase):

    User = get_user_model() #for hashsed password test
    
    def test_valid_form(self):
        form = UserForm({
            'username':'testerusername', 
            'email':'tester@gmail.com', 
            'password':'test123', 
            'phone_number':'222222222', 
            'bio': 'some text', 
            'birth_date': '12/12/1976',
        })
        
        self.assertTrue(form.is_valid())
        
        
    def test_blank_data(self):
        form = UserForm(data={})
        
        self.assertFalse(form.is_valid())

    def test_invalid_email_format(self):
        """
        Provide an email that does not match Django's EmailValidator
        """
        data = {
            "username":      "testerusername",
            "email":         "bad-email_format",          # <-- deliberately bad
            "password":      "test123",
            "phone_number":  "222222222",
            "bio":           "some text",
            "birth_date":    "12/12/1976",
        }

        form = UserForm(data=data)
        self.assertFalse(form.is_valid())

        self.assertIn("email",form.errors)

    
    def test_invalid_phone_format(self):
        """
        Provide a phone past max length that does not match Django's EmailValidator
        """
        data = {
            "username":      "testerusername",
            "email":         "email@gmail.com",          # <-- deliberately bad
            "password":      "test123",
            "phone_number":  "222222222222222222222222222",
            "bio":           "some text",
            "birth_date":    "12/12/1976",
        }

        form = UserForm(data=data)
        self.assertFalse(form.is_valid())

        self.assertIn("phone_number",form.errors)

    
    def test_blank_field_date(self):
        """
        Provide an email that does not match Django's EmailValidator
        """
        data = {
            "username":      "testerusername",
            "email":         "email@gmail.com",          # <-- deliberately bad
            "password":      "test123",
            "phone_number":  "2222222222",
            "bio":           "some text",
            "birth_date":    "12/12/",
        }

        form = UserForm(data=data)
        self.assertFalse(form.is_valid())

        self.assertIn("birth_date",form.errors)
        

    def test_password_is_hashed(self):
        
        data = {
            "username":      "testerusername",
            "email":         "tester@gmail.com",
            "password":      "mySecretPwd123",   # plain‑text password to check with later
            "phone_number":  "222222222",
            "bio":           "some text",
            "birth_date":    "12/12/1976",
        }
        form = UserForm(data=data)
        self.assertTrue(form.is_valid())
        saved_user = form.save()
        db_user = User.objects.get(username="testerusername")
        self.assertTrue(db_user.check_password("mySecretPwd123")) #returns True only if the stored hash matches
        #     the plain‑text password we originally supplied 
        self.assertNotEqual(db_user.password,"mySecretPwd123",)

