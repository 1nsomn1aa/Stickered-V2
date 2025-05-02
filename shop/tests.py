from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal

from shop.models import (
    Category, Product, SizeType, SizeOption,
    Order, OrderItem
)
from shop.forms import ProductForm, OrderForm
from shop.views import product_list, add_product
from shop.webhooks import stripe_webhook


# --- VIEWS TESTING --- #

class ShopViewsTests(TestCase):
    """
    Test the core views in the shop app to verify product views,
    cart, and checkout.
    """

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Stickers")
        self.product = Product.objects.create(
            name="Cool Sticker",
            description="A very cool sticker",
            base_price=Decimal("3.50"),
            category=self.category,
            image=SimpleUploadedFile("test.jpg", b"file_content",
                                     content_type="image/jpeg")
        )
        self.size_type = SizeType.objects.create(name="Standard")
        self.size_option = SizeOption.objects.create(
            product=self.product,
            size_type=self.size_type,
            price=Decimal("3.50")
        )

    def test_product_list_view(self):
        """
        Test that the product list view renders correctly.
        """
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product_list.html')

    def test_cart_view_displays(self):
        """
        Test that the cart detail view loads correctly.
        """
        response = self.client.get(reverse('cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/cart_detail.html')


# --- URLS TESTING --- #

class ShopUrlsTests(TestCase):
    """
    Test that URLs in the shop app resolve to their correct views.
    """

    def test_product_list_url_resolves(self):
        """
        Check if product list URL resolves to the correct view.
        """
        url = reverse('product_list')
        self.assertEqual(resolve(url).func, product_list)

    def test_add_product_url_resolves(self):
        """
        Check if add product URL resolves correctly.
        """
        url = reverse('add_product')
        self.assertEqual(resolve(url).func, add_product)

    def test_stripe_webhook_url_resolves(self):
        """
        Check if the webhook URL resolves correctly to stripe_webhook.
        """
        url = reverse('stripe_webhook')
        self.assertEqual(resolve(url).func, stripe_webhook)


# --- MODELS TESTING --- #

class ProductModelTest(TestCase):
    """
    Test basic functionality of the Product model.
    """

    def test_string_representation(self):
        category = Category.objects.create(name="Banners")
        product = Product.objects.create(
            name="Test Banner",
            base_price=Decimal("10.00"),
            category=category,
            image=SimpleUploadedFile("test.jpg", b"file_content",
                                     content_type="image/jpeg")
        )
        self.assertIn(product.name, str(product))


class OrderModelTest(TestCase):
    """
    Test logic and string representation of Order model.
    """

    def test_order_string_contains_customer_name(self):
        order = Order.objects.create(
            first_name="Rob",
            last_name="Robertson",
            email="robbiiee@gmail.com",
            address_line1="123 Main St",
            city="Dublin",
            eir_code="A65 F4E2",
            country="Ireland"
        )
        self.assertIn("Rob", str(order))

    def test_total_amount_calculates_correctly(self):
        category = Category.objects.create(name="Stickers")
        product = Product.objects.create(
            name="X",
            base_price=Decimal("5.00"),
            category=category,
            image=SimpleUploadedFile("test.jpg", b"file_content",
                                     content_type="image/jpeg")
        )
        size_type = SizeType.objects.create(name="Mini")
        size_option = SizeOption.objects.create(
            product=product,
            size_type=size_type,
            price=Decimal("5.00")
        )
        order = Order.objects.create(
            first_name="Test",
            last_name="Tester",
            email="test@test.com",
            address_line1="123 Test St",
            city="Testville",
            eir_code="A91 XP24",
            country="Ireland",
            shipping_cost=Decimal("2.00")
        )
        OrderItem.objects.create(
            order=order,
            product=product,
            size=size_option,
            price=Decimal("5.00"),
            quantity=2
        )
        self.assertEqual(order.total_amount(), Decimal("12.00"))


# --- FORMS TESTING --- #

class ProductFormTest(TestCase):
    """
    Ensure the product form is valid when filled properly.
    """

    def test_valid_product_form(self):
        category = Category.objects.create(name="Stickers")
        form_data = {
            'name': 'Test Product',
            'description': 'Some description',
            'base_price': '9.99',
            'category': category.id
        }
        form = ProductForm(data=form_data)
        self.assertTrue(form.is_valid())


class OrderFormTest(TestCase):
    """
    Ensure the order form works with valid and invalid input.
    """

    def test_valid_order_form(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'address_line1': '123 Street',
            'city': 'Dublin',
            'eir_code': 'A1B 2C3',
            'country': 'Ireland'
        }
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_missing_required_fields(self):
        form = OrderForm(data={})
        self.assertFalse(form.is_valid())
