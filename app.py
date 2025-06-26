import streamlit as st
import pandas as pd
import os

FILE_PATH = "artisan_store.xlsx"

def load_data():
    if not os.path.exists(FILE_PATH):
        with pd.ExcelWriter(FILE_PATH, engine='openpyxl') as writer:
            pd.DataFrame(columns=["Name", "Skill", "Phone"]).to_excel(writer, sheet_name="Artisans", index=False)
            pd.DataFrame(columns=["Product", "Price", "Stock", "Artisan"]).to_excel(writer, sheet_name="Products", index=False)
            pd.DataFrame(columns=["Product", "Quantity", "Buyer"]).to_excel(writer, sheet_name="Orders", index=False)
    xls = pd.ExcelFile(FILE_PATH, engine='openpyxl')
    artisans = pd.read_excel(xls, sheet_name="Artisans")
    products = pd.read_excel(xls, sheet_name="Products")
    orders = pd.read_excel(xls, sheet_name="Orders")
    return artisans, products, orders

def save_data(artisans, products, orders):
    with pd.ExcelWriter(FILE_PATH, engine='openpyxl") as writer:
        artisans.to_excel(writer, sheet_name="Artisans", index=False)
        products.to_excel(writer, sheet_name="Products", index=False)
        orders.to_excel(writer, sheet_name="Orders", index=False)

st.title("🧵 Artisan Product App")

artisans, products, orders = load_data()

menu = st.sidebar.selectbox("Menu", ["Register Artisan", "Add Product", "View Products", "Buy Product"])

if menu == "Register Artisan":
    name = st.text_input("Name")
    skill = st.text_input("Skill")
    phone = st.text_input("Phone")
    if st.button("Register"):
        artisans = artisans.append({"Name": name, "Skill": skill, "Phone": phone}, ignore_index=True)
        save_data(artisans, products, orders)
        st.success("Artisan Registered")

elif menu == "Add Product":
    product = st.text_input("Product Name")
    price = st.number_input("Price", min_value=0.0)
    stock = st.number_input("Stock", min_value=0)
    artisan = st.selectbox("Artisan", artisans["Name"] if not artisans.empty else [])
    if st.button("Add Product"):
        products = products.append({"Product": product, "Price": price, "Stock": stock, "Artisan": artisan}, ignore_index=True)
        save_data(artisans, products, orders)
        st.success("Product Added")

elif menu == "View Products":
    st.write("### Available Products")
    st.dataframe(products)

elif menu == "Buy Product":
    product = st.selectbox("Product", products["Product"] if not products.empty else [])
    quantity = st.number_input("Quantity", min_value=1)
    buyer = st.text_input("Buyer Name")
    if st.button("Buy"):
        index = products[products["Product"] == product].index[0]
        if products.loc[index, "Stock"] >= quantity:
            products.loc[index, "Stock"] -= quantity
            orders = orders.append({"Product": product, "Quantity": quantity, "Buyer": buyer}, ignore_index=True)
            save_data(artisans, products, orders)
            st.success("Purchase successful")
        else:
            st.error("Not enough stock")
