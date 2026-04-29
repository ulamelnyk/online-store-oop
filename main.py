from models import Product, Customer
from services import ShopService, JsonService

service = ShopService()
json_service = JsonService()

product1 = Product("iPhone", 1000, 5, "Electronics")
product2 = Product("Laptop", 1500, 3, "Electronics")
product3 = Product("Book", 20, 50, "Books")
product4 = Product("Headphones", 200, 10, "Electronics")

products = [product1, product2, product3, product4]

json_service.save_products(products, "products.json")

loaded_products = json_service.load_products("products.json")

user1 = Customer("Anna", "anna@mail.com", "Warsaw")
user2 = Customer("Tom", "tom@mail.com", "Berlin")

user1.cart.add_product(loaded_products[0])
user1.cart.add_product(loaded_products[2])

order1 = service.create_order(user1)

user1.cart.add_product(loaded_products[3])
order2 = service.create_order(user1)

user2.cart.add_product(loaded_products[1])
user2.cart.add_product(loaded_products[2])
user2.cart.add_product(loaded_products[3])

order3 = service.create_order(user2)

print(f"{user1.username}'s orders:")
for o in user1.view_orders():
    print("Total:", o.total)
    for product in o.products:
        print(product)
    print()

print(f"{user2.username}'s orders:")
for o in user2.view_orders():
    print("Total:", o.total)
    for product in o.products:
        print(product)
    print()