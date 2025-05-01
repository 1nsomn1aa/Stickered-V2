from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class ProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    reset_image = forms.BooleanField(required=False, label='Reset profile image to default')

    class Meta:
        model = UserProfile
        fields = [
            'profile_image', 'bio', 'reset_image',
            'first_name', 'last_name',
            'address', 'city', 'county', 'eir_code', 'role'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email

        placeholders = {
            'first_name': 'John',
            'last_name': 'Doe',
            'address': '123 Main Street, Apt 4B',
            'city': 'Dublin',
            'county': 'Louth',
            'eir_code': 'A65 F4E2',
            'role': 'Sticker collector, mechanic, etc.',
            'bio': 'Tell us a bit about yourself...',
        }

        for field, text in placeholders.items():
            self.fields[field].widget.attrs['placeholder'] = text

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user

        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']

        if self.cleaned_data.get('reset_image'):
            if profile.profile_image and profile.profile_image.name != 'default.jpg':
                profile.profile_image.delete(save=False)
            profile.profile_image = 'default.jpg'

        if commit:
            user.save()
            profile.save()
        return profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']