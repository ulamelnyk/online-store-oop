class Product:
    def __init__(self, name, price, quantity, category):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category

    def __str__(self):
        return f"{self.name} - {self.price}"

    def to_dict(self):
        return{
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "category": self.category
        }

    @staticmethod
    def from_dict(data):
        return Product(
            data["name"],
            data["price"],
            data["quantity"],
            data["category"],
        )

class Cart:
    def __init__(self):
        self.items = []

    def add_product(self, product):
        self.items.append(product)

    def remove_product(self, product):
        if product in self.items:
            self.items.remove(product)

    def get_total(self):
        return sum(product.price for product in self.items)


class Order:
    def __init__(self, products, total):
        self.products = products
        self.total = total


class User:
    def __init__(self, username, email, address):
        self.username = username
        self.email = email
        self.address = address
        self.cart = Cart()
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def view_orders(self):
        return self.orders

class Customer(User):
    def __init__(self, username, email, address):
        super().__init__(username, email, address)

class Admin(User):
    def __init__(self, username, email, address):
        super().__init__(username, email, address)

    def add_product(self, product, product_list):
        product_list.append(product)