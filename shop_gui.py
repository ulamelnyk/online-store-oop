import re
import customtkinter as ctk
from models import Customer
from services import ShopService, JsonService, OrderJsonService
from analytics import show_analytics
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

service = ShopService()
json_service = JsonService()
order_json_service = OrderJsonService()
current_user = None

root = ctk.CTk()
root.geometry("500x600")
root.title("Main Page")

main_frame = ctk.CTkScrollableFrame(
    root,
    width=480,
    height=580,
    fg_color="#dae8f4"
)
main_frame.pack(fill="both", expand=True)


EMAIL_RE = re.compile(r"^[^@]+@[^@]+\.[^@]+$")

def submit():
    global current_user

    username = username_entry.get().strip()
    email = email_entry.get().strip()
    address = address_entry.get().strip()

    # Clear previous errors
    username_error.configure(text="")
    email_error.configure(text="")
    address_error.configure(text="")
    result_label.configure(text="", text_color="black")

    # Validate username
    if not username:
        username_error.configure(text="Please enter your username")
        return

    # Validate email
    if not email:
        email_error.configure(text="Please enter your email address")
        return
    if not EMAIL_RE.match(email):
        email_error.configure(text="Please enter a valid email address")
        return

    # Validate address
    if not address:
        address_error.configure(text="Please enter your address")
        return

    # If all validations pass, create user
    current_user = Customer(username, email, address)

    # Provide success feedback and enable order button
    username_error.configure(
        text=f"Hello, {username.capitalize()}!",
        text_color="green"
    )
    create_order_btn.configure(
        state="normal",
        fg_color="#FF7CB0"
    )
    result_label.configure(
        text=f"User {username} created successfully.",
        text_color="green"
    )
    result_label.pack(pady=5)

# --- Entries ---
username_entry = ctk.CTkEntry(main_frame,
    placeholder_text="Username",
    fg_color="#FFE6EE",
    placeholder_text_color="black",
    text_color="black",
    border_color="#FF7CB0"
)
username_entry.pack(pady=1)

# Username error label
username_error = ctk.CTkLabel(
    main_frame,
    text="",
    text_color="red",
    font=("Arial", 10)
)
username_error.pack(pady=1)

email_entry = ctk.CTkEntry(main_frame,
    placeholder_text="Email",
    fg_color="#FFE6EE",
    placeholder_text_color="black",
    text_color="black",
    border_color="#FF7CB0"
)
email_entry.pack(pady=1)

# Email error label
email_error = ctk.CTkLabel(
    main_frame,
    text="",
    text_color="red",
    font=("Arial", 10)

)
email_error.pack(pady=1)

address_entry = ctk.CTkEntry(main_frame,
    placeholder_text="Address",
    fg_color="#FFE6EE",
    placeholder_text_color="black",
    text_color="black",
    border_color="#FF7CB0"
)
address_entry.pack(pady=1)

# Address error label (you already had this)
address_error = ctk.CTkLabel(
    main_frame,
    text="",
    text_color="red",
    font=("Arial", 10)
)
address_error.pack(pady=1)

submit_btn = ctk.CTkButton(
    main_frame,
    text="Create User",
    command=submit,
    corner_radius=30,
    fg_color="#FF7CB0",
    text_color="white"
)
submit_btn.pack(pady=(1, 10))

result_label = ctk.CTkLabel(
    main_frame,
    text="",
    text_color="black",
    font=("Arial", 14)
)
result_label.pack(pady=5)

# Visible result label for general messages (success/info)

# --- Product cards and actions (unchanged except using UI feedback) ---
products_frame = ctk.CTkFrame(
    main_frame,
    fg_color="transparent"
)
products_frame.pack(pady=10)

def show_message(text, color="black"):
    result_label.configure(
        text=text,
        text_color=color
    )

def add_to_cart(product):
    global current_user

    if current_user is None:
        show_message("Please create a user first", color="red")
        return

    current_user.cart.add_product(product)
    show_message(f"{product.name} added to cart", color="green")

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
        height=35,
        corner_radius=30,
    ).pack(pady=(10, 25))

def create_order():
    global current_user

    if current_user is None:
        show_message("Please create a user first", color="red")
        return

    if not current_user.cart.items:
        show_message("Cart is empty", color="red")
        return

    order = service.create_order(current_user)

    orders = current_user.view_orders()
    order_json_service.save_order(
        orders,
        "orders.json"
    )

    product_names = [product.name for product in order.products]

    order_label.configure(
        text=f"{current_user.username.capitalize()} ordered:\n"
             f"{', '.join(product_names)}\n"
             f"Total: ${order.total}"
    )

    order_label.pack(pady=5)

def display_analytics():
    df, total_revenue, figure = show_analytics()

    analytics_label.configure(
        text=f"Total products sold: {len(df)}\n"
             f"Total revenue: ${total_revenue}"
    )
    analytics_label.pack(pady=5)

    canvas = FigureCanvasTkAgg(
        figure,
        master=main_frame
    )

    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)

create_order_btn = ctk.CTkButton(
    main_frame,
    text="Create Order",
    command=create_order,
    text_color="white",
    fg_color="#FFD6E7",
    corner_radius=30,
    state="disabled"
)
create_order_btn.pack(pady=5)

order_label = ctk.CTkLabel(
    main_frame,
    text="",
    text_color="black",
    font=("Arial", 14)
)
order_label.pack()

analytics_btn = ctk.CTkButton(
    main_frame,
    text="Show Analytics",
    command=display_analytics,
    fg_color="#FF7CB0",
    text_color="white",
    corner_radius=30,
)
analytics_btn.pack(pady=10)

analytics_label = ctk.CTkLabel(
    main_frame,
    text="",
    text_color="black"
)
analytics_label.pack_forget()
