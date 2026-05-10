import customtkinter as ctk
from models import Customer
from services import ShopService, JsonService, OrderJsonService

service = ShopService()
json_service = JsonService()
order_json_service = OrderJsonService()
current_user = None

root = ctk.CTk()
root.geometry("500x400")
root.title("Main Page")
root.configure()

main_frame = ctk.CTkScrollableFrame(
    root,
    width=480,
    height=380,
    fg_color="#dae8f4"
)
main_frame.pack(fill="both", expand=True)

def submit():
    global current_user

    username = username_entry.get()
    email = email_entry.get()
    address = address_entry.get()

    current_user = Customer(username, email, address)

    print(f"Hello, {username}!")

    username_entry.delete(0, "end")
    email_entry.delete(0, "end")
    address_entry.delete(0, "end")


username_entry = ctk.CTkEntry(main_frame,
    placeholder_text="Username",
    fg_color="#FFE6EE",
    placeholder_text_color="black",
    text_color="black",
    border_color="#FF7CB0"
)
username_entry.pack(pady=10)

email_entry = ctk.CTkEntry(main_frame,
    placeholder_text="Email",
    fg_color="#FFE6EE",
    placeholder_text_color="black",
    text_color="black",
    border_color="#FF7CB0"
)
email_entry.pack(pady=10)

address_entry = ctk.CTkEntry(main_frame,
    placeholder_text="Address",
    fg_color="#FFE6EE",
    placeholder_text_color="black",
    text_color="black",
    border_color="#FF7CB0"
)
address_entry.pack(pady=10)

submit_btn = ctk.CTkButton(
    main_frame,
    text="Create User",
    command=submit,
    corner_radius=30,
    fg_color="#FF7CB0",
    text_color="white"
)
submit_btn.pack(pady=20)


# Product cards
products_frame = ctk.CTkFrame(
    main_frame,
    fg_color="transparent"
)
products_frame.pack(pady=20)


def add_to_cart(product):
    global current_user

    if current_user is None:
        print("Please create user first")
        return

    current_user.cart.add_product(product)
    print(f"{product.name} added to cart")


loaded_products = json_service.load_products("products.json")


for index, product in enumerate(loaded_products):
    row = index // 2
    column = index % 2

    product_card = ctk.CTkFrame(
        products_frame,
        width=180,
        height=180,
        fg_color="#FFE6EE"
    )
    product_card.grid(row=row, column=column, padx=10, pady=10)

    ctk.CTkLabel(
        product_card,
        text=product.name,
        text_color="black"
    ).pack(pady=(15, 5))

    ctk.CTkLabel(
        product_card,
        text=f"${product.price}",
        text_color="black"
    ).pack(pady=5)

    ctk.CTkLabel(
        product_card,
        text=product.category,
        text_color="black"
    ).pack(pady=5)

    ctk.CTkButton(
        product_card,
        text="Add to cart",
        command=lambda p=product: add_to_cart(p),
        fg_color="#FF7CB0",
        text_color="white",
        width=100,
        height=35
    ).pack(pady=(10, 25))


def create_order():
    global current_user

    if current_user is None:
        print("Please create user first")
        return

    if not current_user.cart.items:
        print("Cart is empty")
        return

    order = service.create_order(current_user)

    orders = current_user.view_orders()
    order_json_service.save_order(
        orders,
        "orders.json"
    )

    print(f"Order created! Total: ${order.total}")

create_order_btn = ctk.CTkButton(
    main_frame,
    text="Create Order",
    command=create_order,
    text_color="white",
    fg_color="#FF7CB0"
)
create_order_btn.pack(pady=20)
