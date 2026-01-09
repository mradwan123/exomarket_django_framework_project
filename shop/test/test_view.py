from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()
from django.urls import reverse
from ..models import Item

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
        
    def test_home_view_display_user(self):
        login_ok = self.client.login(username="testuser", password="test123")
        self.assertTrue(login_ok, "Login failed in test setup")

        response = self.client.get(self.home_url)

        self.assertIn("user", response.context)
        self.assertEqual(response.context["user"], self.user.username)


# Items view testing

class ItemDetailViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="SellerMan",
            email="seller@notgmail.com",
            password="pass1234",
        )

        self.item = Item.objects.create( #item without image
            name="Test Tech gadget",
            description="A cool gadget.",
            price="19.99",
            category="Tech",
            seller= self.user,
            available=True,
        )
        # Build the URL that includes the primary‑key of the item
        self.detail_url = reverse(
            "shop:detail", kwargs={"item_id": self.item.id}
        )


    def test_item_detail_receives_correct_id(self):
        """
        The view should return HTTP 200, render the correct template,
        and expose the `item` object (with the same PK we passed in the URL)
        in the template context.
        """
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "item_detail_view.html")

        # The context must contain an ``item`` key
        self.assertIn("item", response.context)

        # The `item` in the context must be the same object we created
        context_item = response.context["item"]
        self.assertEqual(context_item.id, self.item.id)
        self.assertEqual(context_item.name, self.item.name)

    def test_item_detail_view(self):
        response = self.client.get(self.detail_url)
        self.assertIn("item", response.context)

    def test_detail_returns_404_for_missing_item(self):
        # Pick an ID far beyond the current max
        missing_pk = Item.objects.latest("id").id + 999
        url = reverse("shop:detail", kwargs={"item_id": missing_pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_unavailable_item_still_renders(self):
        self.unavailable_item = Item.objects.create( 
            name="Test Tech gadget",
            description="A cool gadget.",
            price="19.99",
            category="Tech",
            seller= self.user,
            available=False,
        )
        url = reverse(
            "shop:detail", kwargs={"item_id": self.unavailable_item.id}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("item", response.context)
        self.assertFalse(response.context["item"].available)

        self.assertFalse(response.context["is_available"])
        self.assertIn("availability_message", response.context)
        self.assertEqual(
            response.context["availability_message"],
            "This item is currently unavailable.",
        )
    def test_item_delete_view(self):
        self.item = Item.objects.create( 
            name="Test Tech gadget",
            description="A cool gadget.",
            price="19.99",
            category="Tech",
            seller= self.user,
            available=True,
        )        
        self.item.delete()
        self.assertFalse(Item.objects.filter(pk=self.item.pk).exists())

class ItemCreateTest(TestCase):
    def setUpUserTestData(cls):
        cls.seller = User.objects.create_user(
            username="radwan",
            email="radwan@example.com",
            password="Password123"
        )

    def setUp(self):
        self.client.login(username="radwan", password="Password123")
        self.url = reverse("shop:create-item")  
        
    def test_get_returns_form(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create_item.html")
        
        
    
    
  
class ItemUpdateTest(TestCase): 
    @classmethod
    def setUpTestData(cls):
        # Two users: one will own the item, the other will try to edit it
        cls.owner = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="OwnerPass",
        )
        cls.other = User.objects.create_user(
            username="intruder",
            email="intruder@example.com",
            password="IntruderPass",
        )

        # Create an item that belongs to ``owner``
        cls.item = Item.objects.create(
            name="Original Name",
            description="Original description",
            price="10.00",
            category="Original",
            seller=cls.owner,
            available=True,
        )
        
    
    def setUp(self):
        self.update_url = reverse(
            "shop:update",
            kwargs={"item_id": self.item.id},
        )
        
    #----#
    def test_non_owner_cannot_update(self):
        self.client.login(username="intruder", password="IntruderPass")
        resp = self.client.get(self.update_url)

        self.assertEqual(resp.status_code, 200)   # view returns HttpResponse, not a redirect
        self.assertContains(resp, "You are not allowed to update this item!")

        # Even a POST should be blocked
        resp_post = self.client.post(self.update_url, data={"name": "Hacked"})
        self.assertContains(resp_post, "You are not allowed to update this item!")
    
    def test_owner_post_valid_updates_item(self):
        self.client.login(username="owner", password="OwnerPass")

        # Minimal payload that satisfies ItemForm validation
        payload = {
            "name": "Updated Name",
            "description": "Updated description",
            "price": "42.50",
            "category": "Updated Category",
            "available": True, 
        }  
    
        resp = self.client.post(self.update_url, data=payload, follow=False)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Success! Your Item Has Been Updated.')

        self.item.refresh_from_db()
        self.assertEqual(self.item.name, "Updated Name")
        self.assertEqual(self.item.description, "Updated description")
        self.assertEqual(str(self.item.price), "42.50")
        self.assertEqual(self.item.category, "Updated Category")
        self.assertTrue(self.item.available)


class ListItemsViewTests(TestCase):
    """
    Tests for ``list_items_view`` which renders ``view_all_items.html`` with
    the current user and a queryset of all Item objects.
    """

    @classmethod
    def setUpTestData(cls):
        # Create two users – one will be logged in, the other will stay anonymous
        cls.user = User.objects.create_user(
            username="radwan",
            email="radwan@example.com",
            password="StrongPwd!23",
        )
        cls.other_user = User.objects.create_user(
            username="alice",
            email="alice@example.com",
            password="AlicePwd!23",
        )

        # Create a handful of Item instances that the view should list
        cls.item_a = Item.objects.create(
            name="Alpha",
            description="First item",
            price="10.00",
            category="Category A",
            seller=cls.user,
            available=True,
        )
        cls.item_b = Item.objects.create(
            name="Beta",
            description="Second item",
            price="20.50",
            category="Category B",
            seller=cls.other_user,
            available=False,
        )
        cls.item_c = Item.objects.create(
            name="Gamma",
            description="Third item",
            price="5.75",
            category="Category C",
            seller=cls.user,
            available=True,
        )

    def setUp(self):
        # Resolve the URL that points to the view – adjust the name if yours differs
        self.url = reverse("shop:list") 
        
    def test_authenticated_user_is_passed_to_template(self):
        """
        When a logged-in user accesses the view, ``request.user`` should be
        the actual User instance (not AnonymousUser) and still see all items.
        """
        self.client.login(username="radwan", password="StrongPwd!23")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "view_all_items.html")

        # ``user`` in the context should be the logged‑in user
        self.assertTrue(response.context["user"].is_authenticated)
        self.assertEqual(response.context["user"], self.user)

        # All items must still be present
        all_items_qs = response.context["all_items"]
        self.assertQuerySetEqual(
            all_items_qs.order_by("id"),
            Item.objects.all().order_by("id"),
            transform=lambda x: x,
        )

    # TO BE COMPLETETD
  
    # def test_list_items(self):
    # def item_delete_view(self)
    # def seller_all_items_view(self)


   
    