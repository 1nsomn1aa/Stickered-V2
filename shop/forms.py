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
        fields = ['first_name', 'last_name', 'email', 'address_line1', 'address_line2', 'city', 'eir_code', 'country']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'address_line1': 'Street Address',
            'address_line2': 'County',
            'city': 'City / Town',
            'eir_code': 'Eircode',
            'country': 'Country',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email address'}),
            'address_line1': forms.TextInput(attrs={'placeholder': 'Street address'}),
            'address_line2': forms.TextInput(attrs={'placeholder': 'County'}),
            'city': forms.TextInput(attrs={'placeholder': 'City or Town'}),
            'eir_code': forms.TextInput(attrs={'placeholder': 'Eircode or Postal Code'}),
            'country': forms.Select(choices=[('Ireland', 'Ireland')]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})