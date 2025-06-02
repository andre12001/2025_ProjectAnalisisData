import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Olist Dashboard", layout="wide")
st.title("🛒 Olist E-commerce Dataset Analytics Dashboard")

# Load data from local CSVs
@st.cache_data
def load_data():
    customers = pd.read_csv("customers_dataset.csv")
    order_items = pd.read_csv("order_items_dataset.csv")
    order_payments = pd.read_csv("order_payments_dataset.csv")
    orders = pd.read_csv("orders_dataset.csv", parse_dates=["order_purchase_timestamp", "order_delivered_customer_date"])
    products = pd.read_csv("products_dataset.csv")
    sellers = pd.read_csv("sellers_dataset.csv")
    return customers, order_items, order_payments, orders, products, sellers

customers_df, order_items_df, order_payments_df, orders_df, products_df, sellers_df = load_data()

st.sidebar.header("🧭 Insight Navigator")
selected_insight = st.sidebar.radio("Pilih pertanyaan", [
    "1. Total Jumlah Pesanan",
    "2. Kategori Produk Terpopuler",
    "3. Total Revenue",
    "4. Seller dengan Penjualan Terbanyak",
    "5. Rata-rata Waktu Pengiriman",
    "6. Kota Customer Teraktif",
    "7. Metode Pembayaran Populer",
    "8. Produk Paling Mahal",
    "9. Jumlah Seller per State",
    "10. Distribusi Pesanan per Bulan"
])

# 1. Total Jumlah Pesanan
if selected_insight == "1. Total Jumlah Pesanan":
    st.subheader("🧮 Total Jumlah Pesanan")
    total_orders = orders_df["order_id"].nunique()
    st.metric("Total Orders", f"{total_orders:,}")

# 2. Kategori Produk Terpopuler
elif selected_insight == "2. Kategori Produk Terpopuler":
    st.subheader("📦 Kategori Produk Terpopuler")
    merged = order_items_df.merge(products_df, on="product_id")
    popular_categories = merged["product_category_name"].value_counts().head(10)
    st.bar_chart(popular_categories)

# 3. Total Revenue
elif selected_insight == "3. Total Revenue":
    st.subheader("💰 Total Revenue")
    total_revenue = order_payments_df["payment_value"].sum()
    st.metric("Total Revenue (BRL)", f"R$ {total_revenue:,.2f}")

# 4. Seller dengan Penjualan Terbanyak
elif selected_insight == "4. Seller dengan Penjualan Terbanyak":
    st.subheader("🏆 Seller dengan Penjualan Terbanyak")
    top_sellers = order_items_df["seller_id"].value_counts().head(10)
    st.bar_chart(top_sellers)

# 5. Rata-rata Waktu Pengiriman
elif selected_insight == "5. Rata-rata Waktu Pengiriman":
    st.subheader("🚚 Rata-rata Waktu Pengiriman")
    delivered = orders_df.dropna(subset=["order_delivered_customer_date"])
    delivered["delivery_time"] = (delivered["order_delivered_customer_date"] - delivered["order_purchase_timestamp"]).dt.days
    avg_delivery = delivered["delivery_time"].mean()
    st.metric("Rata-rata Hari Pengiriman", f"{avg_delivery:.2f} hari")

# 6. Kota Customer Teraktif
elif selected_insight == "6. Kota Customer Teraktif":
    st.subheader("🏙️ Kota Customer Teraktif")
    top_cities = customers_df["customer_city"].value_counts().head(10)
    st.bar_chart(top_cities)

# 7. Metode Pembayaran Populer
elif selected_insight == "7. Metode Pembayaran Populer":
    st.subheader("💳 Metode Pembayaran Populer")
    payment_methods = order_payments_df["payment_type"].value_counts()
    st.bar_chart(payment_methods)

# 8. Produk Paling Mahal
elif selected_insight == "8. Produk Paling Mahal":
    st.subheader("💎 Produk Paling Mahal")
    expensive_products = order_items_df.sort_values("price", ascending=False).head(10)[["order_id", "product_id", "price"]]
    st.dataframe(expensive_products)

# 9. Jumlah Seller per State
elif selected_insight == "9. Jumlah Seller per State":
    st.subheader("🗺️ Jumlah Seller per State")
    seller_state_counts = sellers_df["seller_state"].value_counts()
    st.bar_chart(seller_state_counts)

# 10. Distribusi Pesanan per Bulan
elif selected_insight == "10. Distribusi Pesanan per Bulan":
    st.subheader("📅 Distribusi Pesanan per Bulan")
    orders_df["bulan"] = orders_df["order_purchase_timestamp"].dt.to_period("M")
    monthly_orders = orders_df.groupby("bulan")["order_id"].count()
    monthly_orders.index = monthly_orders.index.astype(str)
    st.line_chart(monthly_orders)
