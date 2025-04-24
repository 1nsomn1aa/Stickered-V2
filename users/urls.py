from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order/<str:order_number>/', views.order_detail, name='order_detail'),
]