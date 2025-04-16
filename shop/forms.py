from django import forms
from .models import Product, SizeOption


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'size_description', 'usage', 'base_price', 'image', 'category', 'sizes']

    sizes = forms.ModelMultipleChoiceField(queryset=SizeOption.objects.all(), required=False)