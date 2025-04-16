from decimal import Decimal
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
        product_ids = []
        size_ids = []
        for key in self.cart.keys():
            try:
                pid, sid = map(int, key.split(":"))
                product_ids.append(pid)
                size_ids.append(sid)
            except ValueError:
                continue

        product_map = {p.id: p for p in Product.objects.filter(id__in=product_ids)}
        size_map = {s.id: s for s in SizeOption.objects.filter(id__in=size_ids)}

        modified = False

        for key in list(self.cart.keys()):
            try:
                product_id, size_id = map(int, key.split(":"))
                raw = self.cart[key]
                prod = product_map[product_id]
                siz = size_map[size_id]

                yield {
                    "product": prod,
                    "size": siz,
                    "quantity": raw["quantity"],
                    "total_price": siz.price * raw["quantity"],
                }

            except (KeyError, ValueError):
                self.cart.pop(key, None)
                modified = True

        if modified:
            self.save()

    def get_total_price(self):
        return sum(item['total_price'] for item in self)
