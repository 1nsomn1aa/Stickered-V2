from django.conf import settings
from shop.models import Product, SizeOption


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product_id, size_id, quantity, update_quantity=False):
        key = f"{product_id}:{size_id}"
        if key not in self.cart:
            self.cart[key] = {'quantity': 0, 'size_id': size_id}
        if update_quantity:
            self.cart[key]['quantity'] = quantity
        else:
            self.cart[key]['quantity'] += quantity
        self.save()

    def remove(self, product_id, size_id):
        key = f"{product_id}:{size_id}"
        if key in self.cart:
            del self.cart[key]
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        self.session[settings.CART_SESSION_ID] = {}
        self.save()

    def __iter__(self):
        product_ids = [int(key.split(":")[0]) for key in self.cart.keys()]
        size_ids = [int(item['size_id']) for item in self.cart.values()]
        products = Product.objects.filter(id__in=product_ids)
        sizes = SizeOption.objects.filter(id__in=size_ids)
        size_map = {s.id: s for s in sizes}
        product_map = {p.id: p for p in products}

        for key, item in self.cart.items():
            product_id, size_id = map(int, key.split(":"))
            item['product'] = product_map[product_id]
            item['size'] = size_map[size_id]
            item['total_price'] = item['size'].price * item['quantity']
            yield item

    def get_total_price(self):
        return sum(item['size'].price * item['quantity'] for item in self.cart.values())
