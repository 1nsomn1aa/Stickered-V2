from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from .forms import ProductForm

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    category_filter = request.GET.getlist('category')
    if category_filter:
        products = products.filter(category__id__in=category_filter)

    price_to = request.GET.get('price_to')
    if price_to:
        products = products.filter(price__lte=price_to)

    return render(request, 'shop/product_list.html', {
        'products': products,
        'categories': categories,
        'category_filter': category_filter
    })

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'shop/product_form.html', {'form': form})

def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
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
    return render(request, 'shop/product_detail.html', {'product': product})