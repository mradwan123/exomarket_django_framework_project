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
        self.item = Item.objects.create(
            name="Test Tech gadget",
            description="A cool gadget.",
            price="19.99",
            category="Tech",
            available=True,
        )
        # Build the URL that includes the primary‑key of the item
        self.detail_url = reverse(
            "shop:detail", kwargs={"item_id": self.item.id}
        )


    def test_item_detail_receives_correct_id(self):
        """
        The view should return HTTP 200, render the correct template,
        and expose the ``item`` object (with the same PK we passed in the URL)
        in the template context.
        """
        response = self.client.get(self.detail_url)

        # 1️⃣ Status code should be 200 (not a 404)
        self.assertEqual(response.status_code, 200)

        # 2️⃣ The view should have used the expected template
        self.assertTemplateUsed(response, "item_detail_view.html")

        # 3️⃣ The context must contain an ``item`` key
        self.assertIn("item", response.context)

        # 4️⃣ The ``item`` in the context must be the same object we created
        context_item = response.context["item"]
        self.assertEqual(context_item.id, self.item.id)
        self.assertEqual(context_item.name, self.item.name)