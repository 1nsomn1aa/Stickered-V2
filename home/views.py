from django.shortcuts import render, redirect
from shop.models import Product
from .models import Testimonial
from .forms import TestimonialForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import ContactForm
import json


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


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                form.instance.user = request.user

            contact_message = form.save()
            print(f"Contact message saved: {contact_message}")

            subject = f"New contact message from {contact_message.name}"
            message = f"Message from {contact_message.name} ({contact_message.email}):\n\n{contact_message.message}"
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            customer_subject = f"Your message has been received, {contact_message.name}"
            customer_message = f"Hi {contact_message.name},\n\nThanks for getting in touch! Here's a copy of your message:\n\n{contact_message.message}"
            send_mail(
                customer_subject,
                customer_message,
                settings.EMAIL_HOST_USER,
                [contact_message.email],
                fail_silently=False,
            )

            messages.success(request, "Your message has been sent successfully!")
            print("Success message added")

            return redirect('contact')
        else:
            print("Form is not valid:", form.errors)
            messages.error(request, "There was an issue submitting your message. Please try again.")
    else:
        form = ContactForm()

    return render(request, 'home/contact.html', {'form': form})


@csrf_exempt
def newsletter_signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')

            if email:
                if not NewsletterSubscriber.objects.filter(email=email).exists():
                    subscriber = NewsletterSubscriber.objects.create(email=email)

                    subject = "Newsletter Subscription Confirmation"
                    message = f"Hi {email},\n\nThanks for subscribing to our newsletter! You'll now receive the latest updates."
                    send_mail(
                        subject,
                        message,
                        settings.EMAIL_HOST_USER,
                        [email],
                        fail_silently=False,
                    )

                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({'success': False, 'message': 'This email is already subscribed.'})
            else:
                return JsonResponse({'success': False, 'message': 'Please provide a valid email.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})