import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for plots
sns.set_style("whitegrid")


# Load the data
@st.cache_data
def load_data():
    all_data = pd.read_csv('all_data.csv')
    all_data['order_purchase_timestamp'] = pd.to_datetime(all_data['order_purchase_timestamp'])
    all_data['order_delivered_customer_date'] = pd.to_datetime(all_data['order_delivered_customer_date'])
    return all_data


try:
    loaded_df = load_data()
    all_df = loaded_df
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.stop()

st.title('Analisis Data E-commerce')

# Sidebar for navigation
page = st.sidebar.selectbox('Pilih Pertanyaan',
                            ['Pertanyaan 1', 'Pertanyaan 2', 'Pertanyaan 3', 'Pertanyaan 4', 'RFM Analysis',
                             'Geo-Analysis'])

if page == 'Pertanyaan 1':
    st.header('Kota dengan Total Penjualan dan Pendapatan Terbanyak dan Tersedikit')

    # Total penjualan per kota
    city_sales = all_df.groupby('geolocation_city').agg({
        'order_id': 'count',
        'payment_value': 'sum'
    }).reset_index()
    city_sales = city_sales.sort_values('order_id', ascending=False)

    # Kota dengan penjualan terbanyak dan tersedikit
    st.subheader('Total Penjualan')
    col1, col2 = st.columns(2)
    with col1:
        st.write("Terbanyak:", city_sales.iloc[0]['geolocation_city'])
        st.write("Jumlah:", city_sales.iloc[0]['order_id'])
    with col2:
        st.write("Tersedikit:", city_sales.iloc[-1]['geolocation_city'])
        st.write("Jumlah:", city_sales.iloc[-1]['order_id'])

    # Visualisasi total penjualan
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='order_id', y='geolocation_city', data=city_sales.head(10), ax=ax)
    ax.set_title('10 Kota dengan Total Penjualan Terbanyak')
    ax.set_xlabel('Jumlah Penjualan')
    ax.set_ylabel('Kota')
    st.pyplot(fig)

    # Kota dengan pendapatan terbanyak dan tersedikit
    city_sales = city_sales.sort_values('payment_value', ascending=False)
    st.subheader('Total Pendapatan')
    col1, col2 = st.columns(2)
    with col1:
        st.write("Terbanyak:", city_sales.iloc[0]['geolocation_city'])
        st.write("Jumlah:", f"${city_sales.iloc[0]['payment_value']:,.2f}")
    with col2:
        st.write("Tersedikit:", city_sales.iloc[-1]['geolocation_city'])
        st.write("Jumlah:", f"${city_sales.iloc[-1]['payment_value']:,.2f}")

    # Visualisasi total pendapatan
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='payment_value', y='geolocation_city', data=city_sales.head(10), ax=ax)
    ax.set_title('10 Kota dengan Total Pendapatan Terbanyak')
    ax.set_xlabel('Total Pendapatan')
    ax.set_ylabel('Kota')
    st.pyplot(fig)

elif page == 'Pertanyaan 2':
    st.header('Kategori Produk dengan Total Penjualan dan Pendapatan Terbanyak dan Tersedikit')

    # Total penjualan dan pendapatan per kategori produk
    product_sales = all_df.groupby('product_category_name_english').agg({
        'order_id': 'count',
        'payment_value': 'sum'
    }).reset_index()

    # Kategori dengan penjualan terbanyak dan tersedikit
    product_sales_count = product_sales.sort_values('order_id', ascending=False)
    st.subheader('Total Penjualan')
    col1, col2 = st.columns(2)
    with col1:
        st.write("Terbanyak:", product_sales_count.iloc[0]['product_category_name_english'])
        st.write("Jumlah:", product_sales_count.iloc[0]['order_id'])
    with col2:
        st.write("Tersedikit:", product_sales_count.iloc[-1]['product_category_name_english'])
        st.write("Jumlah:", product_sales_count.iloc[-1]['order_id'])

    # Visualisasi total penjualan
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='order_id', y='product_category_name_english', data=product_sales_count.head(10), ax=ax)
    ax.set_title('10 Kategori Produk dengan Total Penjualan Terbanyak')
    ax.set_xlabel('Jumlah Penjualan')
    ax.set_ylabel('Kategori Produk')
    st.pyplot(fig)

    # Kategori dengan pendapatan terbanyak dan tersedikit
    product_sales_revenue = product_sales.sort_values('payment_value', ascending=False)
    st.subheader('Total Pendapatan')
    col1, col2 = st.columns(2)
    with col1:
        st.write("Terbanyak:", product_sales_revenue.iloc[0]['product_category_name_english'])
        st.write("Jumlah:", f"${product_sales_revenue.iloc[0]['payment_value']:,.2f}")
    with col2:
        st.write("Tersedikit:", product_sales_revenue.iloc[-1]['product_category_name_english'])
        st.write("Jumlah:", f"${product_sales_revenue.iloc[-1]['payment_value']:,.2f}")

    # Visualisasi total pendapatan
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='payment_value', y='product_category_name_english', data=product_sales_revenue.head(10), ax=ax)
    ax.set_title('10 Kategori Produk dengan Total Pendapatan Terbanyak')
    ax.set_xlabel('Total Pendapatan')
    ax.set_ylabel('Kategori Produk')
    st.pyplot(fig)

elif page == 'Pertanyaan 3':
    st.header('Rata-rata Waktu Pengiriman Produk')

    # Menghitung waktu pengiriman
    all_df['delivery_time'] = (all_df['order_delivered_customer_date'] - all_df[
        'order_purchase_timestamp']).dt.total_seconds() / 86400  # Convert to days

    avg_delivery_time = all_df['delivery_time'].mean()

    st.write(f"Rata-rata waktu pengiriman produk adalah {avg_delivery_time:.2f} hari.")

    # Visualisasi distribusi waktu pengiriman
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(all_df['delivery_time'], kde=True, ax=ax)
    ax.set_title('Distribusi Waktu Pengiriman')
    ax.set_xlabel('Waktu Pengiriman (Hari)')
    ax.set_ylabel('Frekuensi')
    st.pyplot(fig)

elif page == 'Pertanyaan 4':
    st.header('Kategori Produk dengan Rating Terbaik dan Terburuk')

    # Menghitung rata-rata rating untuk setiap kategori produk
    product_ratings = all_df.groupby('product_category_name_english')['review_score'].mean().sort_values(
        ascending=False).reset_index()

    st.subheader('Rating Terbaik')
    st.write("Kategori:", product_ratings.iloc[0]['product_category_name_english'])
    st.write("Rating:", f"{product_ratings.iloc[0]['review_score']:.2f}")

    st.subheader('Rating Terburuk')
    st.write("Kategori:", product_ratings.iloc[-1]['product_category_name_english'])
    st.write("Rating:", f"{product_ratings.iloc[-1]['review_score']:.2f}")

    # Visualisasi top 10 dan bottom 10 kategori
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))
    sns.barplot(x='review_score', y='product_category_name_english', data=product_ratings.head(10), ax=ax1)
    ax1.set_title('10 Kategori Produk dengan Rating Terbaik')
    sns.barplot(x='review_score', y='product_category_name_english', data=product_ratings.tail(10), ax=ax2)
    ax2.set_title('10 Kategori Produk dengan Rating Terburuk')
    plt.tight_layout()
    st.pyplot(fig)

elif page == 'RFM Analysis':
    st.header('RFM (Recency, Frequency, Monetary) Analysis')

    # Menghitung RFM
    reference_date = all_df['order_purchase_timestamp'].max()
    rfm = all_df.groupby('customer_unique_id').agg({
        'order_purchase_timestamp': lambda x: (reference_date - x.max()).days,  # Recency
        'order_id': 'count',  # Frequency
        'payment_value': 'sum'  # Monetary
    })
    rfm.columns = ['Recency', 'Frequency', 'Monetary']

    st.subheader('1. Kapan terakhir pelanggan melakukan transaksi?')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=rfm['Recency'].value_counts().index[:20], y=rfm['Recency'].value_counts().values[:20], ax=ax)
    ax.set_title('Distribusi Recency (Top 20)')
    ax.set_xlabel('Hari sejak pembelian terakhir')
    ax.set_ylabel('Jumlah Pelanggan')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader('2. Seberapa sering pelanggan melakukan pembelian?')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=rfm['Frequency'].value_counts().index[:20], y=rfm['Frequency'].value_counts().values[:20], ax=ax)
    ax.set_title('Distribusi Frequency (Top 20)')
    ax.set_xlabel('Jumlah pembelian')
    ax.set_ylabel('Jumlah Pelanggan')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader('3. Berapa uang terbanyak yang dihabiskan pelanggan?')
    fig, ax = plt.subplots(figsize=(10, 6))
    monetary_bins = pd.cut(rfm['Monetary'], bins=20)
    sns.barplot(x=monetary_bins.value_counts().index.astype(str), y=monetary_bins.value_counts().values, ax=ax)
    ax.set_title('Distribusi Monetary (20 bins)')
    ax.set_xlabel('Total nilai pembelian')
    ax.set_ylabel('Jumlah Pelanggan')
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif page == 'Geo-Analysis':
    st.header('Negara Bagian dengan Total Penjualan Tertinggi dan Terendah')

    # Menghitung total penjualan per negara bagian
    state_sales = all_df.groupby('geolocation_state')['payment_value'].sum().sort_values(ascending=False).reset_index()

    st.subheader('Negara Bagian dengan Penjualan Tertinggi')
    st.write("Negara Bagian:", state_sales.iloc[0]['geolocation_state'])
    st.write("Total Penjualan:", f"${state_sales.iloc[0]['payment_value']:,.2f}")

    st.subheader('Negara Bagian dengan Penjualan Terendah')
    st.write("Negara Bagian:", state_sales.iloc[-1]['geolocation_state'])
    st.write("Total Penjualan:", f"${state_sales.iloc[-1]['payment_value']:,.2f}")

    # Visualisasi penjualan per negara bagian
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x='payment_value', y='geolocation_state', data=state_sales, ax=ax)
    ax.set_title('Total Penjualan per Negara Bagian')
    ax.set_xlabel('Total Penjualan')
    ax.set_ylabel('Negara Bagian')
    st.pyplot(fig)


st.sidebar.info('Dashboard ini menyediakan analisis data e-commerce berdasarkan pertanyaan-pertanyaan spesifik.')
