import streamlit as st
import pandas as pd
import random

# Sample product data
data = {
    "Product Name": ["T-shirt", "Jeans", "Sneakers", "Handbag", "Sunglasses", "Watch", "Jacket", "Perfume"],
    "Category": ["Clothing", "Clothing", "Footwear", "Accessories", "Accessories", "Accessories", "Clothing", "Fragrance"],
    "Price": [500, 1200, 2500, 1800, 999, 3000, 2200, 1500],
    "Rating": [4.5, 4.3, 4.7, 4.1, 4.2, 4.8, 4.6, 4.0],
    "Stock": [10, 5, 7, 8, 6, 4, 9, 3],
    "Image": ["images/tshirt.png", "images/jeans.png", "images/sneakers.png", "images/handbag.png", "images/sunglasses.png", "images/watch.png", "images/jacket.png", "images/perfume.png"]
}

df = pd.DataFrame(data)

# Streamlit UI
st.set_page_config(page_title="TrendHive - Shopping Website", layout="wide")


st.markdown("<h1 class='title'>🛍️ TrendHive - The Ultimate Shopping Experience</h1>", unsafe_allow_html=True)
st.sidebar.header("Categories")
category_filter = st.sidebar.selectbox("Select a category", ["All"] + list(df["Category"].unique()))

# Filter products based on category
filtered_df = df if category_filter == "All" else df[df["Category"] == category_filter]

# Display Products
st.subheader("✨ Featured Products ✨")
cols = st.columns(3)

for i, row in filtered_df.iterrows():
    with cols[i % 3]:
        st.image(row["Image"], width=150)
        st.write(f"**{row['Product Name']}**")
        st.write(f"💲 Price: {row['Price']} INR")
        st.write(f"⭐ Rating: {row['Rating']}")
        if st.button(f"Add to Cart - {row['Product Name']}", key=row['Product Name']):
            st.session_state.setdefault("cart", []).append(row)
            st.success(f"{row['Product Name']} added to cart!")

# Shopping Cart
st.sidebar.subheader("🛒 Your Cart")
if "cart" in st.session_state and st.session_state["cart"]:
    total_price = sum(item["Price"] for item in st.session_state["cart"])
    for item in st.session_state["cart"]:
        st.sidebar.write(f"{item['Product Name']} - ₹{item['Price']}")
    st.sidebar.write(f"**Total: ₹{total_price}**")
    
    if st.sidebar.button("Clear Cart"):
        st.session_state["cart"] = []
        st.sidebar.success("Cart Cleared!")
    
    if st.sidebar.button("Checkout"):
        st.session_state["checkout"] = True
else:
    st.sidebar.write("Your cart is empty.")

# Checkout Page
if "checkout" in st.session_state and st.session_state["checkout"]:
    st.subheader("🛒 Checkout")
    address = st.text_area("📍 Enter your delivery address:")
    payment_method = st.radio("💳 Select Payment Method", ["Cash on Delivery", "Net Banking", "Credit/Debit Card", "UPI"])
    
    st.subheader("🧾 Final Bill")
    st.write(f"**Total Amount Payable: ₹{total_price}**")
    
    if st.button("Confirm Order"):
        if not address:
            st.warning("⚠️ Please enter a valid address.")
        else:
            st.success("🎉 Order Placed Successfully!")
            st.write(f"💰 Payment Method: {payment_method}")
            st.write(f"📦 Delivery Address: {address}")
            st.session_state["cart"] = []
            st.session_state["checkout"] = False
            
st.sidebar.subheader("Search")
search_query = st.sidebar.text_input("🔍 Search for products...")
if search_query:
    search_results = df[df["Product Name"].str.contains(search_query, case=False, na=False)]
    for _, row in search_results.iterrows():
        st.sidebar.write(f"{row['Product Name']} - ₹{row['Price']}")
