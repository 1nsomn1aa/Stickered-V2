from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.conf import settings

from .models import Product, Category, SizeOption, SizeType, Order, OrderItem
from .forms import ProductForm, OrderForm
from .cart import Cart
from .shipping import calculate_shipping

import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY


def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    query = request.GET.get('q')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(category__name__icontains=query))

    category_filter = request.GET.getlist('category')
    if category_filter:
        products = products.filter(category__id__in=category_filter)

    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    if price_from:
        products = products.filter(base_price__gte=price_from)
    if price_to:
        products = products.filter(base_price__lte=price_to)

    sort_by = request.GET.get('sort_by', 'date_desc')
    sort_options = {
        'price_asc': 'base_price',
        'price_desc': '-base_price',
        'name_asc': 'name',
        'name_desc': '-name',
        'date_asc': 'created_at',
        'date_desc': '-created_at',
    }
    products = products.order_by(sort_options.get(sort_by, '-created_at'))

    recent_products = Product.objects.order_by('-created_at')[:5]

    return render(request, 'shop/product_list.html', {
        'products': products,
        'recent_products': recent_products,
        'categories': categories,
        'category_filter': category_filter,
        'sort_by': sort_by,
        'price_from': price_from,
        'price_to': price_to,
        'selected_categories': category_filter,
        'query': query,
    })


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            product.size_options.all().delete()
            selected_sizes = request.POST.getlist('sizes')
            for size_type_id in selected_sizes:
                price = request.POST.get(f'price_{size_type_id}', 0)
                if price:
                    SizeOption.objects.create(product=product, size_type_id=size_type_id, price=price)
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'shop/product_form.html', {'form': form})


def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            product.size_options.all().delete()
            selected_sizes = request.POST.getlist('sizes')
            for size_type_id in selected_sizes:
                price = request.POST.get(f'price_{size_type_id}', 0)
                if price:
                    SizeOption.objects.create(product=product, size_type_id=size_type_id, price=price)
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/product_form.html', {'form': form})


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'shop/confirm_delete.html', {'product': product})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    recent_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:3]
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'recent_products': recent_products,
    })


def add_to_cart(request, product_id):
    size_id = request.POST.get('size')
    quantity = request.POST.get('quantity', 1)
    if not size_id or not quantity:
        return HttpResponseBadRequest("Size and quantity are required.")
    try:
        size_id = int(size_id)
        quantity = int(quantity)
    except ValueError:
        return HttpResponseBadRequest("Invalid size or quantity.")

    size = get_object_or_404(SizeOption, id=size_id)
    cart = Cart(request)
    cart.add(product_id=product_id, size_id=size.id, quantity=quantity)
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart_detail.html', {'cart': cart})


def remove_from_cart(request, product_id, size_id):
    cart = Cart(request)
    cart.remove(product_id=product_id, size_id=size_id)
    return redirect('cart_detail')


@require_POST
def update_cart_quantity(request, product_id, size_id):
    cart = Cart(request)
    quantity = request.POST.get('quantity')
    try:
        quantity = int(quantity)
        if quantity > 0:
            cart.add(product_id=product_id, size_id=size_id, quantity=quantity, update_quantity=True)
        else:
            cart.remove(product_id=product_id, size_id=size_id)
    except (ValueError, TypeError):
        pass
    return redirect('cart_detail')


def checkout(request):
    cart = Cart(request)
    cart_subtotal = cart.get_total_price()
    form = OrderForm()

    shipping_standard = calculate_shipping(cart, 'standard')
    shipping_express = calculate_shipping(cart, 'express')

    return render(request, 'shop/checkout.html', {
        'form': form,
        'cart': cart,
        'cart_subtotal': cart_subtotal,
        'shipping_standard': shipping_standard,
        'shipping_express': shipping_express,
        'shipping_method': 'standard',
        'shipping_cost': shipping_standard,
        'grand_total': cart_subtotal + shipping_standard,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
    })


@require_POST
def create_payment_intent(request):
    try:
        cart = Cart(request)
        cart_subtotal = cart.get_total_price()

        shipping_method = request.POST.get('shipping_method', 'standard')
        shipping_cost = calculate_shipping(cart, shipping_method)
        grand_total = cart_subtotal + shipping_cost

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            first_name=request.POST.get('first_name', ''),
            last_name=request.POST.get('last_name', ''),
            email=request.POST.get('email', ''),
            address_line1=request.POST.get('address_line1', ''),
            address_line2=request.POST.get('address_line2', ''),
            city=request.POST.get('city', ''),
            country=request.POST.get('country', ''),
            eir_code=request.POST.get('eir_code', ''),
            shipping_method=shipping_method,
            shipping_cost=shipping_cost,
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                size=item['size'],
                price=item['size'].price,
                quantity=item['quantity']
            )

        intent = stripe.PaymentIntent.create(
            amount=int(grand_total * 100),
            currency='eur',
            metadata={
                'order_number': order.order_number,
            }
        )

        return JsonResponse({
            'client_secret': intent.client_secret,
            'order_number': order.order_number,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def checkout_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    Cart(request).clear()
    return render(request, 'shop/checkout_success.html', {'order': order})