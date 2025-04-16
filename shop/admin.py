from django.contrib import admin
from .models import Product, Category, SizeOption


class SizeOptionInline(admin.TabularInline):
    model = Product.sizes.through
    extra = 1
    verbose_name = "Size Option"
    verbose_name_plural = "Size Options"


class SizeOptionAdmin(admin.ModelAdmin):
    list_display = ('code', 'price', 'linked_products')

    def linked_products(self, obj):
        return ", ".join([product.name for product in obj.products.all()])
    linked_products.short_description = 'Assigned to'


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price_display', 'category', 'created_at')
    inlines = [SizeOptionInline]

    def price_display(self, obj):
        sizes = obj.sizes.all().order_by('price')
        if sizes.exists():
            return f"€{sizes.first().price:.2f}"
        return f"€{obj.base_price:.2f}"
    price_display.short_description = 'Price'


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(SizeOption, SizeOptionAdmin)
