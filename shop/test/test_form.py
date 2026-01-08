from django.test import TestCase
from django.db import models, IntegrityError
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from ..forms import ItemForm
from decimal import Decimal

class ItemFormSimpleTest(TestCase):
    def test_valid_form(self):
        form = ItemForm({
            'title': 'Test Product',
            'name':'testname',
            'description':'testdesccrp"',
            'price':'3.22',
            'image':None,
            'category':'tech', 
            'available':True,
           
        })
        self.assertTrue(form.is_valid())