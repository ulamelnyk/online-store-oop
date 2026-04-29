import json
from models import Product, Order


class ShopService:
    def create_order(self, user):
        products = user.cart.items.copy()
        total = user.cart.get_total()
        order = Order(products, total)
        user.add_order(order)
        user.cart.items.clear()
        return order


class JsonService:
    def save_products(self, products, filename):
        data = [product.to_dict() for product in products]

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    def load_products(self, filename):
        with open(filename, "r") as file:
            data = json.load(file)

        return [Product.from_dict(item) for item in data]