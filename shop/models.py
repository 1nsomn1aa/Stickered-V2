import uuid
from django.db import models
from django.contrib.auth.models import User


# Categories
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# Main product model
class Product(models.Model):
    sku = models.CharField(max_length=12, unique=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    size_description = models.TextField(blank=True, null=True)
    usage = models.TextField(blank=True, null=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = uuid.uuid4().hex[:12].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.sku})"


# Size labels
class SizeType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# Size and price option per product
class SizeOption(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='size_options',
        null=True,
        blank=True)
    size_type = models.ForeignKey(
        SizeType,
        on_delete=models.CASCADE,
        related_name='sizes',
        null=True,
        blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        size = self.size_type.name if self.size_type else "Unknown Size"
        product = self.product.name if self.product else "Unknown Product"
        return f"{size} - {product} - €{self.price}"


# Orders placed at checkout
class Order(models.Model):
    SHIPPING_CHOICES = [
        ('standard', 'Standard'),
        ('express', 'Express'),
    ]

    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed'),
    ]

    order_number = models.CharField(
        max_length=32, unique=True, null=True, blank=True)

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders')

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    eir_code = models.CharField(max_length=20)
    country = models.CharField(max_length=50, default='Ireland')
    shipping_method = models.CharField(
        max_length=10, choices=SHIPPING_CHOICES, default='standard'
    )
    shipping_cost = models.DecimalField(
        max_digits=6, decimal_places=2, default=0.00
    )
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='processing'
    )
    tracking_number = models.CharField(max_length=100, blank=True, null=True)

    def _generate_order_number(self):
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def total_amount(self):
        items_total = sum(i.get_total_price() for i in self.items.all())
        return items_total + self.shipping_cost
    total_amount.short_description = "Total (€)"

    def __str__(self):
        return f"Order {
            self.order_number} - {
            self.first_name} {
            self.last_name}"


# Order summary
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(SizeOption, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def get_total_price(self):
        return self.price * self.quantity
