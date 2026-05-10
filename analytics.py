import json
import pandas as pd
import matplotlib.pyplot as plt


with open("orders.json", "r") as file:
    orders_data = json.load(file)


all_products = []

for order in orders_data:
    for product in order["products"]:
        all_products.append({
            "name": product["name"],
            "price": product["price"],
            "category": product["category"]
        })


df = pd.DataFrame(all_products)

print("Products Data:")
print(df)


total_revenue = df["price"].sum()
print("\nTotal Revenue:", total_revenue)


most_sold = df["name"].value_counts()

plt.figure(figsize=(10, 6))

most_sold.plot(kind="bar")

plt.title("Most Purchased Products")
plt.xlabel("Products")
plt.ylabel("Number of Purchases")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()