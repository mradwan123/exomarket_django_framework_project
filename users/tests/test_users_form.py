from django.test import TestCase
from ..forms import UserForm

class UserFormTests(TestCase):
    
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