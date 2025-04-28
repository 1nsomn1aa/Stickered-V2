from django.contrib import admin
from .models import Testimonial
from .models import ContactMessage


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'message')

    list_filter = ('created_at',)

    ordering = ('-created_at',)


admin.site.register(Testimonial)
admin.site.register(ContactMessage, ContactMessageAdmin)