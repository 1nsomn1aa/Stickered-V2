from django.shortcuts import render, redirect
from shop.models import Product
from .models import Testimonial
from .forms import TestimonialForm
from django.contrib import messages


def index(request):
    recent_products = Product.objects.order_by('-created_at')[:5]
    testimonials = Testimonial.objects.all().order_by('-created_at')

    if request.method == "POST":
        form = TestimonialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your testimonial has been submitted successfully!", extra_tags='testimonial')
            return redirect('home')
        else:
            print("Form is not valid:", form.errors)
            messages.error(request, "There was an issue submitting your testimonial.", extra_tags='testimonial')
    else:
        form = TestimonialForm()

    return render(request, 'home/index.html', {
        'recent_products': recent_products,
        'testimonials': testimonials,
        'form': form,
    })


def admin_redirect_view(request):
    return redirect('/admin/')


def contact(request):
    return render(request, 'home/contact.html')


def about(request):
    return render(request, 'home/about.html')


def page_not_found(request, exception):
    return render(request, 'home/404.html', status=404)


def server_error(request):
    return render(request, 'home/500.html', status=500)


def permission_denied(request, exception):
    return render(request, 'home/403.html', status=403)


def bad_request(request, exception):
    return render(request, 'home/400.html', status=400)