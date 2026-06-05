from decimal import Decimal

from django.conf import settings

from .forms import CartAddProductForm
from .models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if cart is None:
            cart = self.session[settings.CART_SESSION_ID] = {}
        for product_id, item in list(cart.items()):
            if isinstance(item, int):
                try:
                    product = Product.objects.get(id=product_id)
                except Product.DoesNotExist:
                    del cart[product_id]
                    continue
                cart[product_id] = {
                    "quantity": item,
                    "price": str(product.price),
                }
        self.cart = cart
        self.save()

    def add(self, product, quantity=1, reload=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}

        if reload:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity

        self.cart[product_id]["quantity"] = min(
            self.cart[product_id]["quantity"], product.stock
        )
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids).select_related(
            "category", "club", "brand", "supplier"
        )
        cart = {
            product_id: item.copy()
            for product_id, item in self.cart.items()
            if isinstance(item, dict)
        }

        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            item["update_quantity_form"] = CartAddProductForm(
                initial={"quantity": item["quantity"], "reload": True}
            )
            yield item

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )

    def clear(self):
        self.session[settings.CART_SESSION_ID] = {}
        self.save()
