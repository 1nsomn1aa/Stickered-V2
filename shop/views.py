from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, SizeOption
from .forms import ProductForm
from .cart import Cart
from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_POST


def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    category_filter = request.GET.getlist('category')
    if category_filter:
        products = products.filter(category__id__in=category_filter)

    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')

    if price_from:
        products = products.filter(price__gte=price_from)
    if price_to:
        products = products.filter(price__lte=price_to)

    sort_by = request.GET.get('sort_by', 'date_desc')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'date_asc':
        products = products.order_by('created_at')
    elif sort_by == 'date_desc':
        products = products.order_by('-created_at')

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
    })


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()

            sizes = form.cleaned_data.get('sizes')
            product.sizes.set(sizes)
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

            sizes = form.cleaned_data.get('sizes')
            product.sizes.set(sizes)
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
    recent_products = Product.objects.filter(
        category=product.category
    ).exclude(pk=product.pk)[:3]

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'recent_products': recent_products,
    })


def add_to_cart(request, product_id):

    size_id = request.POST.get('size')
    quantity = request.POST.get('quantity', 1)

    if not size_id or not quantity:
        return HttpResponseBadRequest("Both size and quantity are required.")

    try:
        size_id = int(size_id)
        quantity = int(quantity)
    except ValueError:
        return HttpResponseBadRequest("Invalid size or quantity value.")

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
