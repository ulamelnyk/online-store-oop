import customtkinter as ctk
from models import Product, Customer
from services import ShopService

service = ShopService()
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

    print(f"User created: {username}")

    username_entry.delete(0, "end")
    email_entry.delete(0, "end")
    address_entry.delete(0, "end")

def products():
    global current_user

    if current_user is None:
        print("Please create a user first")
        return

    if check1.get() == "on":
        laptop = Product("Laptop", 1500, 3, "Electronics")
        current_user.cart.add_product(laptop)

    if check2.get() == "on":
        phone = Product("Phone", 1000, 5, "Electronics")
        current_user.cart.add_product(phone)

    if check3.get() == "on":
        tablet = Product("Tablet", 800, 4, "Electronics")
        current_user.cart.add_product(tablet)

    order = service.create_order(current_user)

    print("Order created!")
    print("Total:", order.total)

    for product in order.products:
        print(product)

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

# Products
title_products = ctk.CTkLabel(
    main_frame,
    text="Choose products",
    font=("Arial", 20),
    text_color="black"
)
title_products.pack(pady=10)

check1 = ctk.StringVar(value="off")
check2 = ctk.StringVar(value="off")
check3 = ctk.StringVar(value="off")

checkbox1 = ctk.CTkCheckBox(
    main_frame,
    text="Laptop",
    variable=check1,
    onvalue="on",
    offvalue="off",
    text_color="black",
    fg_color="#FE019A",
    border_color="#FE019A"
)
checkbox1.pack(pady=5)

checkbox2 = ctk.CTkCheckBox(
    main_frame,
    text="Phone",
    variable=check2,
    onvalue="on",
    offvalue="off",
    text_color="black",
    fg_color="#FE019A",
    border_color="#FE019A"
)
checkbox2.pack(pady=5)

checkbox3 = ctk.CTkCheckBox(
    main_frame,
    text="Tablet",
    variable=check3,
    onvalue="on",
    offvalue="off",
    text_color="black",
    fg_color="#FE019A",
    border_color="#FE019A"
)
checkbox3.pack(pady=5)

products_btn = ctk.CTkButton(
    main_frame,
    text="Create order",
    command=products,
    corner_radius=30,
    text_color="white",
    fg_color="#FF7CB0"
)
products_btn.pack(pady=20)

root.mainloop()

