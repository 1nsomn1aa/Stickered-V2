from django.contrib import admin
from .models import Testimonial, ContactMessage, NewsletterSubscriber


# Admin config for managing contact messages in the admin panel
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'message')

    list_filter = ('created_at',)

    ordering = ('-created_at',)


# Admin config for newsletter signups
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)


# Register everything
admin.site.register(NewsletterSubscriber, NewsletterSubscriberAdmin)
admin.site.register(Testimonial)
admin.site.register(ContactMessage, ContactMessageAdmin)
