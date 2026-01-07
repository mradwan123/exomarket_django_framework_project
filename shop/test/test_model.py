from django.test import TestCase
from django.db import models
from django.contrib.auth import get_user_model
from ..models import Item, User

User = get_user_model()   # works whether you use the default User or a custom one


class ItemModelTests(TestCase):
    
    def setUp(self):
        'creating to test seller object in next function'
        self.seller = User.objects.create_user(
            username="radwan",
            email="radwan@example.com",
            password="password-123",
        )
        
    def test_create_item(self):
        item = Item.objects.create(
            name="Test Product",
            description="this is a description",
            price="242.22",
            category="testing the category",
            seller=self.seller,
            available=True,
        )

        self.assertEqual(item.name, "Test Product")
        self.assertEqual(item.description, "this is a description")
        self.assertEqual(item.price, "242.22")
        self.assertEqual(item.category, "testing the category")
        self.assertTrue(item.available)
        
        # testing for seller (foreign key, takes from User class)
        
        self.assertIsInstance(item.seller, User) #FK is instance?
        self.assertEqual(item.seller, self.seller)
        self.assertEqual(item.seller.username, "radwan")
        self.assertEqual(item.seller_id, self.seller.id) #comapring primark keys



        
