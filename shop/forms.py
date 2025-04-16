from django import forms
from .models import Product, SizeOption, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'size_description', 'usage', 'base_price', 'image', 'category', 'sizes']

    sizes = forms.ModelMultipleChoiceField(queryset=SizeOption.objects.all(), required=False)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'city', 'zip_code']