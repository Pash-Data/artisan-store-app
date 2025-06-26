import streamlit as st
import pandas as pd
import os

ARTISANS_CSV = "artisans.csv"
PRODUCTS_CSV = "products.csv"
ORDERS_CSV = "orders.csv"

def load_data():
    if not os.path.exists(ARTISANS_CSV):
        pd.DataFrame(columns=["Name", "Skill", "Phone"]).to_csv(ARTISANS_CSV, index=False)
    if not os.path.exists(PRODUCTS_CSV):
        pd.DataFrame(columns=["Product", "Price", "Stock", "Artisan"]).to_csv(PRODUCTS_CSV, index=False)
    if not os.path.exists(ORDERS_CSV):
        pd.DataFrame(columns=["Product", "Quantity", "Buyer"]).to_csv(ORDERS_CSV, index=False)

    artisans = pd.read_csv(ARTISANS_CSV)
    products = pd.read_csv(PRODUCTS_CSV)
    orders = pd.read_csv(ORDERS_CSV)
    return artisans, products, orders

def save_data(artisans, products, orders):
    artisans.to_csv(ARTISANS_CSV, index=False)
    products.to_csv(PRODUCTS_CSV, index=False)
    orders.to_csv(ORDERS_CSV, index=False)

st.title("🧵 Artisan Product Store")

artisans, products, orders = load_data()

menu = st.sidebar.selectbox("Menu", ["Register Artisan", "Add Product", "View Products", "Buy Product"])

if menu == "Register Artisan":
    name = st.text_input("Name")
    skill = st.text_input("Skill")
    phone = st.text_input("Phone")
    if st.button("Register"):
        artisans = pd.concat([artisans, pd.DataFrame([{"Name": name, "Skill": skill, "Phone": phone}])], ignore_index=True)
        save_data(artisans, products, orders)
        st.success("Artisan Registered!")

elif menu == "Add Product":
    product = st.text_input("Product Name")
    price = st.number_input("Price", min_value=0.0)
    stock = st.number_input("Stock", min_value=0)
    artisan = st.selectbox("Artisan", artisans["Name"] if not artisans.empty else [])
    if st.button("Add Product"):
        products = pd.concat([products, pd.DataFrame([{"Product": product, "Price": price, "Stock": stock, "Artisan": artisan}])], ignore_index=True)
        save_data(artisans, products, orders)
        st.success("Product Added!")

elif menu == "View Products":
    st.write("### Products for Sale")
    st.dataframe(products)

elif menu == "Buy Product":
    product = st.selectbox("Product", products["Product"] if not products.empty else [])
    quantity = st.number_input("Quantity", min_value=1)
    buyer = st.text_input("Buyer Name")
    if st.button("Buy"):
        index = products[products["Product"] == product].index[0]
        if products.loc[index, "Stock"] >= quantity:
            products.loc[index, "Stock"] -= quantity
            orders = pd.concat([orders, pd.DataFrame([{"Product": product, "Quantity": quantity, "Buyer": buyer}])], ignore_index=True)
            save_data(artisans, products, orders)
            st.success("Purchase successful!")
        else:
            st.error("Not enough stock")
