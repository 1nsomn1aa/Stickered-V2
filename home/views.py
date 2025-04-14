from django.shortcuts import render, redirect
from shop.models import Product


def index(request):
    recent_products = Product.objects.order_by('-created_at')[:5]

    return render(request, 'home/index.html', {
        'recent_products': recent_products,
    })


def admin_redirect_view(request):
    return redirect('/admin/')


def contact(request):
    return render(request, 'home/contact.html')


def about(request):
    return render(request, 'home/about.html')