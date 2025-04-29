from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('contact/', views.contact_view, name='contact'),
    path('about/', views.about, name='about'),
    path('newsletter/signup/', views.newsletter_signup, name='newsletter_signup'),
]