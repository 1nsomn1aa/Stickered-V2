from decimal import Decimal


STANDARD_RATES = {
    'Stickers': Decimal("3.50"),
    'License Plates': Decimal("5.00"),
    'Banners': Decimal("6.50"),
}

EXPRESS_RATES = {
    'Stickers': Decimal("7.50"),
    'License Plates': Decimal("10.00"),
    'Banners': Decimal("12.50"),
}

FREE_SHIPPING_THRESHOLD = Decimal("50.00")


def calculate_shipping(cart, method='standard'):
    categories = set()
    subtotal = Decimal("0.00")

    for item in cart:
        categories.add(item['product'].category.name)
        subtotal += item['total_price']

    if method == 'standard' and subtotal >= FREE_SHIPPING_THRESHOLD:
        return Decimal("0.00")

    rates = STANDARD_RATES if method == 'standard' else EXPRESS_RATES
    selected_rates = [rates.get(category, Decimal("0.00")) for category in categories]

    return max(selected_rates) if selected_rates else Decimal("0.00")
