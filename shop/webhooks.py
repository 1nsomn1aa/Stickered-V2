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

            subject = (
                f"Your Order is Confirmed - {order.order_number}"
            )
            message = (
                f"Hi {order.first_name},\n\n"
                f"Thanks for your order! We’ve received your payment and your "
                f"order is now being processed.\n\n"
                f"Order Number: {order.order_number}\n"
                f"Shipping Method: {order.get_shipping_method_display()}\n"
                f"Shipping Cost: €{order.shipping_cost:.2f}\n"
                f"Total Amount: €{order.total_amount():.2f}\n\n"
                f"Items Ordered:\n"
            )

            for item in order.items.all():
                message += (
                    f"- {item.quantity} x {item.product.name} "
                    f"({item.size}) - €{item.price:.2f} each\n"
                )

            message += (
                "\nYour order is now being prepared and we’ll notify you when "
                "it ships.\n\nThanks again for shopping with us!\n\n"
                "– The Stickered Team"
            )

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [order.email],
                fail_silently=False,
            )

        except Order.DoesNotExist:
            print(f"Order not found: {order_number}")
            return HttpResponse(status=404)

    elif event['type'] == 'payment_intent.canceled':
        intent = event['data']['object']
        order_number = intent['metadata'].get('order_number')

        try:
            order = Order.objects.get(order_number=order_number)
            print(f"Payment was canceled for Order: {order_number}")

            subject = f"Order Cancelled - {order.order_number}"
            message = (
                f"Hi {order.first_name},\n\n"
                f"Unfortunately, your payment for the order "
                f"{order.order_number} was cancelled.\n"
                f"If this was a mistake, you can return to the site and place "
                f"your order again.\n\n"
                f"Order Details:\n"
                f"Total Amount: €{order.total_amount():.2f}\n"
                f"Shipping Method: {order.get_shipping_method_display()}\n"
                f"Shipping Cost: €{order.shipping_cost:.2f}\n\n"
                f"Items:\n"
            )

            for item in order.items.all():
                message += (
                    f"- {item.quantity} x {item.product.name} "
                    f"({item.size}) - €{item.price:.2f} each\n"
                )

            message += (
                "\nIf you need assistance, feel free to contact our "
                "support team.\n\n– The Stickered Team"
            )

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [order.email],
                fail_silently=False,
            )

        except Order.DoesNotExist:
            print(f"Order not found for canceled intent: {order_number}")
            return HttpResponse(status=404)

    else:
        print(f"Unhandled event type {event['type']}")

    return HttpResponse(status=200)
