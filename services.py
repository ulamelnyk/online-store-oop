import json
from models import Product, Order, User


class ShopService:
    def create_order(self, user: User) -> Order:
        products = user.cart.items.copy()
        total = user.cart.get_total()
        order = Order(products, total)
        user.add_order(order)
        user.cart.items.clear()
        return order


class JsonService:
    def save_products(
            self,
            products: list[Product],
            filename: str
    ) -> None:
        data = [product.to_dict() for product in products]

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    def load_products(
            self,
            filename: str
    ) -> list[Product]:
        with open(filename, "r") as file:
            data = json.load(file)

        return [Product.from_dict(item) for item in data]

class OrderJsonService:
    def save_order(
            self,
            order: list[Order],
            filename: str
    ) -> None:
        data = [product.to_dict() for product in order]

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    def load_order(
            self,
            filename: str
    ) -> list[Order]:
        with open(filename, "r") as file:
            data = json.load(file)

        return [Order.from_dict(item) for item in data]