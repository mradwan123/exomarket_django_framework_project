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
        The view should return HTTP 200, render the correct template,
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
        self.assertNotContains(response, "<img", html=True) #check no image tag because no image file

    def test_detail_returns_404_for_missing_item(self):
        # Pick an ID far beyond the current max
        missing_pk = Item.objects.latest("id").id + 999
        url = reverse("shop:detail", kwargs={"item_id": missing_pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


