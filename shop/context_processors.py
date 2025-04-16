from .cart import Cart


def cart_totals(request):
    cart = Cart(request)
    return {
        'cart_total': cart.get_total_price(),
    }