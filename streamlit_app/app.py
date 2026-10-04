import requests
import streamlit as st


st.title("🛒 Product AI Assistant")

question = st.text_input("Ask something about your products")

if st.button("Ask"):
    product = None
    data = {}

    if question:
        response = requests.post(
            "http://127.0.0.1:8000/ai/chat",
            params={"message": question},
        )

        if response.status_code == 200:
            data = response.json()
            product = data.get("product")

    if product:
        st.success("Product found!")
        st.subheader(f" {product['name']}")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Price", f"₹{product['price']}")

        with col2:
            st.metric("Product ID", product["id"])
    else:
        st.warning(data.get("message", "Product not found"))

 
