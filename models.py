class Product:
    def __init__(
            self,
            name: str,
            price: float,
            quantity: int,
            category: str
    ) -> None:
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category

    def __str__(self) -> str:
        return f"{self.name} - {self.price}"

    def to_dict(self) -> dict:
        return{
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "category": self.category
        }

    @staticmethod
    def from_dict(data: dict) -> "Product":
        return Product(
            data["name"],
            data["price"],
            data["quantity"],
            data["category"],
        )

class Cart:
    def __init__(self) -> None:
        self.items = []

    def add_product(self, product: Product) -> None:
        self.items.append(product)

    def remove_product(self, product: Product) -> None:
        if product in self.items:
            self.items.remove(product)

    def get_total(self) -> float:
        return sum(product.price for product in self.items)


class Order:
    def __init__(
            self,
            products: list[Product],
            total: float
    ) -> None:
        self.products = products
        self.total = total

    def to_dict(self) -> dict:
        return {
            "products": [product.to_dict() for product in self.products],
            "total": self.total
        }

    @staticmethod
    def from_dict(data: dict) -> "Order":
        products = [
            Product.from_dict(item)
            for item in data["products"]
        ]

        return Order(
            products,
            data["total"]
        )


class User:
    def __init__(
            self,
            username: str,
            email: str,
            address: str
    ) -> None:
        self.username = username
        self.email = email
        self.address = address
        self.cart = Cart()
        self.orders = []

    def add_order(self, order: Order) -> None:
        self.orders.append(order)

    def view_orders(self) -> list:
        return self.orders

class Customer(User):
    def __init__(
            self,
            username: str,
            email: str,
            address: str
    ) -> None:
        super().__init__(username, email, address)

class Admin(User):
    def __init__(
            self,
            username: str,
            email: str,
            address: str
    ) -> None:
        super().__init__(username, email, address)

    def add_product(
            self,
            product: Product,
            product_list: list
    ) -> None:
        product_list.append(product)