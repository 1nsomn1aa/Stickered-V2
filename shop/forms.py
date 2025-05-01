from django import forms
from .models import Product, SizeType, SizeOption, Order


# Form to add/edit a product
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'size_description', 'usage', 'base_price', 'image', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        all_size_types = SizeType.objects.all()
        existing_options = {}
        if self.instance.pk:
            existing_options = {so.size_type_id: so for so in self.instance.size_options.all()}

        self.size_data = []
        for size_type in all_size_types:
            size_option = existing_options.get(size_type.id)
            self.size_data.append({
                'size_type': size_type,
                'size_option': size_option,
                'checked': bool(size_option),
                'price': size_option.price if size_option else '',
            })

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


# Form on the checkout page to collect user info
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