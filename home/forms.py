from django import forms
from .models import Testimonial, ContactMessage, NewsletterSubscriber


# Form for users to submit testimonials
class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'message', 'role']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Your testimonial here...'}),
        }


# Contact form
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your Message', 'class': 'form-control'}),
        }


# Newsletter signup form
class NewsletterSignupForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']

    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}), required=True)