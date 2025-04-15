from django import forms
from .models import Testimonial

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'message', 'role']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Your testimonial here...'}),  # Make sure the message field is a Textarea
        }