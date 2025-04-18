from django.conf import settings
from shop.models import Product, SizeOption


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product_id, size_id, quantity=1, update_quantity=False):
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
        keys = self.cart.keys()
        product_ids = []
        size_ids = []

        for key in keys:
            try:
                pid, sid = map(int, key.split(":"))
                product_ids.append(pid)
                size_ids.append(sid)
            except ValueError:
                continue

        products = Product.objects.filter(id__in=product_ids)
        sizes = SizeOption.objects.filter(id__in=size_ids)

        product_map = {p.id: p for p in products}
        size_map = {s.id: s for s in sizes}

        for key in list(self.cart.keys()):
            try:
                pid, sid = map(int, key.split(":"))
                product = product_map[pid]
                size = size_map[sid]
                item = self.cart[key]

                yield {
                    'product': product,
                    'size': size,
                    'quantity': item['quantity'],
                    'total_price': size.price * item['quantity'],
                }

            except (KeyError, ValueError):
                self.cart.pop(key, None)
                self.save()

    def get_total_price(self):
        return sum(item['total_price'] for item in self)

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
