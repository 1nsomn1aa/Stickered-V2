from django.contrib import admin
from .models import Product, Category, SizeType, SizeOption, Order, OrderItem
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings


# Sends a status update email when an order is updated in the admin panel
def send_order_status_email(order, status):
    template_prefix = f"emails/{status}"
    subject = render_to_string(f"{template_prefix}_subject.txt", {'order': order}).strip()
    message = render_to_string(f"{template_prefix}_body.txt", {
        'order': order,
        'order_items': order.items.all(),
    })
    send_mail(subject, message, settings.EMAIL_HOST_USER, [order.email], fail_silently=False)


# Editing size options from the product admin panel
class SizeOptionInline(admin.TabularInline):
    model = SizeOption
    extra = 1
    fields = ('size_type', 'price')


# Custom admin for products
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price_display', 'category', 'created_at')
    inlines = [SizeOptionInline]

    def price_display(self, obj):
        sizes = obj.size_options.all().order_by('price')
        if sizes.exists():
            return f"€{sizes.first().price:.2f}"
        return f"€{obj.base_price:.2f}"
    price_display.short_description = 'Price'


# Custom admin for size types
class SizeTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


# Shows order items inline when viewing an order
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'size', 'price', 'quantity')


# Custom admin for managing orders
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'full_name', 'email', 'shipping_method',
        'shipping_cost', 'total_amount', 'status', 'tracking_number', 'created_at'
    )
    readonly_fields = (
        'first_name', 'last_name', 'email',
        'address_line1', 'address_line2', 'city', 'eir_code', 'country',
        'shipping_method', 'shipping_cost', 'total_amount', 'created_at',
        'full_name', 'address_display',
    )
    inlines = [OrderItemInline]

    fieldsets = (
        ('Customer Information', {
            'fields': ('first_name', 'last_name', 'email', 'full_name')
        }),
        ('Shipping Address', {
            'fields': ('address_line1', 'address_line2', 'city', 'eir_code', 'country', 'address_display')
        }),
        ('Order Details', {
            'fields': ('shipping_method', 'shipping_cost', 'total_amount', 'created_at')
        }),
        ('Order Management', {
            'fields': ('status', 'tracking_number')
        }),
    )

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Full Name'

    def address_display(self, obj):
        address = obj.address_line1
        if obj.address_line2:
            address += f", {obj.address_line2}"
        address += f", {obj.city}, {obj.eir_code}, {obj.country}"
        return address
    address_display.short_description = 'Full Address'

    def save_model(self, request, obj, form, change):
        if change:
            old_status = Order.objects.get(pk=obj.pk).status
            if obj.status != old_status:
                send_order_status_email(obj, obj.status)
        super().save_model(request, obj, form, change)


# Register everything
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(SizeType, SizeTypeAdmin)
admin.site.register(Order, OrderAdmin)
