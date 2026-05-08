from models import Product, Customer
from services import ShopService, JsonService, OrderJsonService

if __name__ == "__main__":
    service = ShopService()
    json_service = JsonService()
    order_service = OrderJsonService()

    # All products:
    # Notebooks
    product1 = Product(1,"Notebook", 10, 50, "Notebooks")
    product2 = Product(2, "Daily Planner", 15, 30, "Notebooks")
    product3 = Product(3, "Calendar", 20, 50, "Notebooks")

    # Writing Tools
    product4 = Product(4, "Gel Pens Set", 5, 100, "Writing Tools")
    product5 = Product(5, "Highlighters Set", 5, 100, "Writing Tools")

    # Accessories
    product6 = Product(6, "Pencil Case", 10, 50, "Accessories")
    product7 = Product(7, "Desk Organizer", 15, 60, "Accessories")

    # Decor
    product8 = Product(8, "Stickers Pack", 5, 100, "Decor")
    product9 = Product(9, "Washi Tape Set", 10, 50, "Decor")
    product10 = Product(10, "Sticky Notes", 7, 50, "Decor")

    products = [product1, product2, product3, product4, product5, product6, product7, product8, product9, product10]

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

orders = [order1, order2, order3]
order_service.save_order(orders, "orders.json")
order_service.save_order(orders, "orders.json")
loaded_orders = (order_service.load_order("orders.json"))