from django.test import TestCase
from django.db import models, IntegrityError
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from ..models import Item, User, Cart

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
        self.assertTrue(item.image)   # After saving, the image attribute should evaluate to False

    def test_category_too_many_chars(self):
        'max length for category is set at 50 in model'
        item = Item(
            name='test',
            description="this is a description",
            price='23.2',
            category="a"*51,
            seller=self.seller,
            available=True,
            )
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_available_false_valid(self):
        item = Item(
            name='test',
            description="this is a description",
            price='23.2',
            category="testing the category",
            seller=self.seller,
            available=False,
            )
        self.assertFalse(item.available) 

# ----- Cart Testing -------

class CartModelTests(TestCase):

    def setUp(cls):
        cls.user = User.objects.create_user(username='radwan', password='testpass')
        cls.item1 = Item.objects.create(
            name='SomethingCool',
            description='A descrp of something cool',
            price='9.99',
            category='tech',
            available=True,
        )
        cls.item2 = Item.objects.create(
            name='item2',
            description='A descrp item2',
            price='20.99',
            category='gadget',
            available=True,
        )
        cls.cart = Cart.objects.create(user=cls.user)

    def test_one_to_one_cart_user(self):
        with self.assertRaises(IntegrityError):
            Cart.objects.create(user=self.user)  # attempting to add cart to user with existing cart

    def test_cart_is_deleted_when_user_is_deleted(self):
        '''Cascade delete from User → Cart.'''
        
        self.assertTrue(Cart.objects.filter(user=self.user).exists())
        self.user.delete()
        self.user.save()
        self.assertFalse(Cart.objects.filter(user=self.user).exists())
    
    def test_add_items_to_cart(self):
        """Items can be added via the M2M field and retrieved back."""
        self.cart.items.add(self.item1, self.item2)
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.items.count(), 2)
        self.assertIn(self.item1, self.cart.items.all())
        self.assertIn(self.item2, self.cart.items.all())


    def test_remove_item_from_cart(self):
        '''Removing an item clears the link but leaves the cart in place.'''
        self.cart.items.add(self.item1, self.item2)
        self.cart.items.remove(self.item1)

        self.assertEqual(self.cart.items.count(), 1)
        self.assertNotIn(self.item1, self.cart.items.all())
        self.assertIn(self.item2, self.cart.items.all())

    def test_clear_all_items(self):
        ''' clear() empties the cart. checks count at 0.'''
        self.cart.items.add(self.item1, self.item2)
        self.cart.items.clear()
        self.assertEqual(self.cart.items.count(), 0)

    def test_deleting_item_removes_link_but_keeps_cart(self):
        '''testing to see if remove item does not remove cart'''
        self.cart.items.add(self.item1)
        self.item1.delete()  
        self.assertTrue(Cart.objects.filter(pk=self.cart.pk).exists())
        self.assertEqual(self.cart.items.count(), 0)

    def test_new_cart_has_no_items(self):
        '''testing new cart for new user is empty'''
        new_user = User.objects.create_user(username='wolfgang', password='testpass', email='testttttt@test.com')
        new_cart = Cart.objects.create(user=new_user)
        self.assertEqual(new_cart.items.count(), 0)