import streamlit as st
import pandas as pd
import os
from datetime import datetime

# File
file = "artisan_store.xlsx"

# Initialize Excel file
if not os.path.exists(file):
    with pd.ExcelWriter(file) as writer:
        pd.DataFrame(columns=["ArtisanID", "Name", "Phone", "Location"]).to_excel(writer, sheet_name="Artisans", index=False)
        pd.DataFrame(columns=["ProductID", "ArtisanID", "Name", "Category", "Price", "Stock", "ImagePath"]).to_excel(writer, sheet_name="Products", index=False)
        pd.DataFrame(columns=["OrderID", "ProductID", "CustomerName", "Quantity", "Total", "Date"]).to_excel(writer, sheet_name="Orders", index=False)

# Load data
def load_data():
    artisans = pd.read_excel(file, sheet_name="Artisans")
    products = pd.read_excel(file, sheet_name="Products")
    orders = pd.read_excel(file, sheet_name="Orders")
    return artisans, products, orders

# Save data
def save_data(artisans, products, orders):
    with pd.ExcelWriter(file, engine='openpyxl', mode='w') as writer:
        artisans.to_excel(writer, sheet_name="Artisans", index=False)
        products.to_excel(writer, sheet_name="Products", index=False)
        orders.to_excel(writer, sheet_name="Orders", index=False)

# Streamlit UI
st.title("🛍️ Artisan Product Display App")

menu = st.sidebar.selectbox("Choose Option", ["Register Artisan", "Upload Product", "View Products & Buy", "Orders"])

artisans, products, orders = load_data()

if menu == "Register Artisan":
    st.subheader("👨‍🦱 Register New Artisan")
    name = st.text_input("Name")
    phone = st.text_input("Phone")
    location = st.text_input("Location")

    if st.button("Register"):
        if name and phone and location:
            new_id = artisans["ArtisanID"].max() + 1 if not artisans.empty else 1
            artisans.loc[len(artisans)] = [new_id, name, phone, location]
            save_data(artisans, products, orders)
            st.success("Artisan registered!")
        else:
            st.warning("Please fill all fields.")

elif menu == "Upload Product":
    st.subheader("📦 Upload New Product")
    if artisans.empty:
        st.warning("Please register at least one artisan first.")
    else:
        artisan_name = st.selectbox("Select Artisan", artisans["Name"])
        artisan_id = artisans[artisans["Name"] == artisan_name]["ArtisanID"].values[0]
        name = st.text_input("Product Name")
        category = st.text_input("Category")
        price = st.number_input("Price", min_value=0.0)
        stock = st.number_input("Stock", min_value=0)
        image = st.text_input("Image path or URL (optional)", "N/A")

        if st.button("Upload Product"):
            if name and category and price and stock >= 0:
                new_id = products["ProductID"].max() + 1 if not products.empty else 1
                products.loc[len(products)] = [new_id, artisan_id, name, category, price, stock, image]
                save_data(artisans, products, orders)
                st.success("Product uploaded!")
            else:
                st.warning("Please fill all fields.")

elif menu == "View Products & Buy":
    st.subheader("🛒 Browse Products")

    if products.empty:
        st.info("No products available.")
    else:
        st.dataframe(products[["ProductID", "Name", "Category", "Price", "Stock"]])

        product_id = st.number_input("Enter Product ID to buy", min_value=1)
        customer_name = st.text_input("Customer Name")
        quantity = st.number_input("Quantity", min_value=1)

        if st.button("Buy Product"):
            product = products[products["ProductID"] == product_id]
            if product.empty:
                st.error("Product not found.")
            else:
                stock = int(product["Stock"].values[0])
                price = float(product["Price"].values[0])
                if quantity > stock:
                    st.error("Not enough stock.")
                else:
                    total = price * quantity
                    new_order_id = orders["OrderID"].max() + 1 if not orders.empty else 1
                    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    orders.loc[len(orders)] = [new_order_id, product_id, customer_name, quantity, total, date_now]
                    products.loc[products["ProductID"] == product_id, "Stock"] = stock - quantity
                    save_data(artisans, products, orders)
                    st.success(f"Order placed! Total: ₦{total}")

elif menu == "Orders":
    st.subheader("📑 Order History")
    if orders.empty:
        st.info("No orders placed yet.")
    else:
        st.dataframe(orders)



