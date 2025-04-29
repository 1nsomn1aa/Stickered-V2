from django.contrib import admin
from .models import Testimonial, ContactMessage, NewsletterSubscriber


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'message')

    list_filter = ('created_at',)

    ordering = ('-created_at',)


class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)


admin.site.register(NewsletterSubscriber, NewsletterSubscriberAdmin)
admin.site.register(Testimonial)
admin.site.register(ContactMessage, ContactMessageAdmin)