from django.urls import path
from . import views

urlpatterns = [
    path(
        'profile/',
        views.profile_view,
        name='profile'),
    path(
        'order/<str:order_number>/',
        views.order_detail,
        name='order_detail'),
    path(
        'delete_contact_message/<int:message_id>/',
        views.delete_contact_message,
        name='delete_contact_message'),
]
