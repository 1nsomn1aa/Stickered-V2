import stripe
import json
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.core.cache import cache
from .models import Order


stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    secret = settings.STRIPE_WH_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, secret)
    except ValueError:
        return HttpResponseBadRequest()
    except stripe.error.SignatureVerificationError:
        return HttpResponseBadRequest()

    event_id = event.get('id')
    if cache.get(event_id):
        print(f"Ignored duplicate event: {event_id}")
        return HttpResponse(status=200)
    cache.set(event_id, True, timeout=300)

    if event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        order_number = intent['metadata'].get('order_number')

        try:
            order = Order.objects.get(order_number=order_number)
            print(f"Payment succeeded for Order: {order_number}")

            subject = f"Order Confirmation - {order.order_number}"
            message = f"Thank you for your order!\n\nOrder Number: {order.order_number}\nTotal: €{order.total_amount():.2f}"
            recipient = [order.email]

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                recipient,
                fail_silently=False,
            )

        except Order.DoesNotExist:
            print(f"Order not found: {order_number}")
            return HttpResponse(status=404)

    else:
        print(f"Unhandled event type {event['type']}")

    return HttpResponse(status=200)
