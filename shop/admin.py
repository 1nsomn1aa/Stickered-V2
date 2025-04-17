from django.contrib import admin
from .models import Product, Category, SizeType, SizeOption, Order, OrderItem


class SizeOptionInline(admin.TabularInline):
    model = SizeOption
    extra = 1
    fields = ('size_type', 'price')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price_display', 'category', 'created_at')
    inlines = [SizeOptionInline]

    def price_display(self, obj):
        sizes = obj.size_options.all().order_by('price')
        if sizes.exists():
            return f"€{sizes.first().price:.2f}"
        return f"€{obj.base_price:.2f}"
    price_display.short_description = 'Price'


class SizeTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'size', 'price', 'quantity')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'shipping_method', 'shipping_cost', 'total_amount', 'created_at')
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


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(SizeType, SizeTypeAdmin)
admin.site.register(Order, OrderAdmin)
