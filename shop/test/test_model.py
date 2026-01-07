from django.test import TestCase
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
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
            price='242.22',
            category="testing the category",
            seller=self.seller,
            available=True,
        )

        self.assertEqual(item.name, "Test Product")
        self.assertEqual(item.description, "this is a description")
        self.assertEqual(item.price, '242.22')
        self.assertEqual(item.category, "testing the category")
        self.assertTrue(item.available)
        
        # testing for seller (foreign key, takes from User class)
        
        self.assertIsInstance(item.seller, User) #FK is instance?
        self.assertEqual(item.seller, self.seller)
        self.assertEqual(item.seller.username, "radwan")
        self.assertEqual(item.seller_id, self.seller.id) #comapring primark keys

    
    def test_negative_price(self):
        negative_price = "-0.1"
        item = Item.objects.create(
            name="Test Product",
            description="this is a description",
            price=negative_price,
            category="testing the category",
            seller=self.seller,
            available=True,
        )
        with self.assertRaises(ValidationError) as cm:
            item.full_clean()  
            
    def test_large_price(self):
        too_large_price = "999999999999999999999"
        item = Item( #removed Item.object.create to bypass the DB limit on the price validators
            name="Test Product",
            description="this is a description",
            price=too_large_price,
            category="testing the category",
            seller=self.seller,
            available=True,
        )
        with self.assertRaises(ValidationError):
            item.full_clean()  

    def test_too_many_decimals_price(self):
        too_many_decimals = "99.999"
        item = Item( #removed Item.object.create to bypass the DB limit on the price validators
            name="Test Product",
            description="this is a description",
            price=too_many_decimals,
            category="testing the category",
            seller=self.seller,
            available=True,
        )
        with self.assertRaises(ValidationError):
            item.full_clean() 

    def test_max_price_accepted(self):
        'should follow the total 8 and max 2 decimal restriction'
        max_price = "999999.99"
        item = Item( #removed Item.object.create to bypass the DB limit on the price validators
            name="Test Product",
            description="this is a description",
            price=max_price,
            category="testing the category",
            seller=self.seller,
            available=True,
        )
        self.assertEqual(item.price,'999999.99' )

    def test_too_large_name(self):
        too_large_name = "toolargetoolargetoolargetoolargetoolargetoolargetoolargetoolargetoolargetoolargetoolargetoolargetoolargetoolargetoolargetoolargetoolargetoolargetoolargetoolargetoolarge"
        item = Item(
            name=too_large_name,
            description="this is a description",
            price="23.2",
            category="testing the category",
            seller=self.seller,
            available=True,
        )
        with self.assertRaises(ValidationError):
            item.full_clean()  

    def test_too_large_description(self):
        too_large_descrp= 'a'*256
        item = Item(
            name='test',
            description=too_large_descrp,
            price='23.2',
            category="testing the category",
            seller=self.seller,
            available=True,
        )
        with self.assertRaises(ValidationError):
            item.full_clean()  

    def test_no_image(self):
        item = Item.objects.create(
            name='test',
            description="this is a description",
            price='23.2',
            category="testing the category",
            seller=self.seller,
            available=True,
            image = None,
        )
        item.full_clean()   # full_clean runs model‑field validation; it should succeed
        item.save() # Save to the DB to prove persistence works
        self.assertFalse(item.image)   # After saving, the image attribute should evaluate to False

    def test_item_with_image(self):
        item = Item.objects.create(
            name='test',
            description="this is a description",
            price='23.2',
            category="testing the category",
            seller=self.seller,
            available=True,
            image = 'test.png',
        )
        item.full_clean()   # full_clean runs model‑field validation; it should succeed
        item.save() # Save to the DB to prove persistence works
        self.assertTrue(item.image)   # After saving, the image attribute should evaluate to False
