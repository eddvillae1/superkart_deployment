# Streamlit frontend for the SuperKart sales forecasting app
# Collects user inputs via a web form and calls the Flask API for predictions

import requests
import streamlit as st

# Page layout and title
st.set_page_config(page_title="SuperKart Sales Predictor", layout="centered")
st.title("SuperKart Sales Forecaster")
st.subheader("Predict product-level store sales revenue")

# Flask backend URL -- resolved via Docker network using the service name 'backend'
BACKEND_URL = "http://backend:7860"

# Input form -- two columns for a cleaner layout
with st.form("prediction_form"):
    st.markdown("### Enter Product and Store Details")
    col1, col2 = st.columns(2)

    with col1:
        product_weight  = st.number_input("Product Weight", min_value=0.0, value=12.66, step=0.01)
        product_sugar   = st.selectbox("Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
        product_area    = st.number_input("Allocated Area", min_value=0.0, max_value=1.0,
                                           value=0.027, step=0.001, format="%.3f")
        product_mrp     = st.number_input("Product MRP", min_value=0.0, value=117.08, step=0.01)
        product_id_char = st.selectbox("Product ID Prefix", ["FD", "DR", "NC"])

    with col2:
        store_size       = st.selectbox("Store Size", ["Small", "Medium", "High"])
        store_city       = st.selectbox("Store City Type", ["Tier 1", "Tier 2", "Tier 3"])
        store_type       = st.selectbox("Store Type", [
            "Supermarket Type1", "Supermarket Type2", "Supermarket Type3",
            "Departmental Store", "Food Mart"
        ])
        store_age        = st.number_input("Store Age (Years)", min_value=1, max_value=100, value=16)
        product_type_cat = st.selectbox("Product Type Category", ["Perishables", "Non Perishables"])

    submitted = st.form_submit_button("Predict Sales Revenue")

# Send the form data to the Flask API and display the result
if submitted:
    payload = {
        "Product_Weight":           product_weight,
        "Product_Sugar_Content":    product_sugar,
        "Product_Allocated_Area":   product_area,
        "Product_MRP":              product_mrp,
        "Store_Size":               store_size,
        "Store_Location_City_Type": store_city,
        "Store_Type":               store_type,
        "Product_Id_char":          product_id_char,
        "Store_Age_Years":          store_age,
        "Product_Type_Category":    product_type_cat,
    }
    try:
        response = requests.post(f"{BACKEND_URL}/v1/predict", json=payload, timeout=10)
        if response.status_code == 200:
            prediction = response.json()['prediction']
            st.success(f"Predicted Sales Revenue: **${prediction:,.2f}**")
            st.info(f"This product-store combination is forecast to generate **${prediction:,.2f}** in total sales.")
        else:
            st.error(f"API returned status {response.status_code}. Check that the backend container is running.")
    except requests.exceptions.ConnectionError:
        st.error("Cannot reach the backend. Ensure both Docker containers are up and on the same network.")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
