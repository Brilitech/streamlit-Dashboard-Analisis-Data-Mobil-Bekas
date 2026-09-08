import streamlit as st
import pandas as pd
import plotly.express as px

# ==================== KONFIGURASI HALAMAN ====================
st.set_page_config(
    page_title="Dashboard Mobil Bekas",
    page_icon="🚗",
    layout="wide"
)

# ==================== LOAD DATASET ====================
@st.cache_data
def load_data():
    df = pd.read_csv("vehicles.csv")
    # Bersihkan nama kolom (jadi huruf kecil semua)
    df.columns = df.columns.str.lower()
    return df

df = load_data()

# ==================== HEADER ====================
st.title("🚗 Dashboard Analisis Mobil Bekas")
st.markdown("""
Dashboard ini memungkinkan kamu mengeksplorasi data mobil bekas secara interaktif. 
Gunakan filter di sidebar untuk menyaring data sesuai keinginanmu.
""")

# ==================== SIDEBAR FILTER ====================
st.sidebar.header("🔍 Filter Data")

# Filter berdasarkan merk
merk_list = ['Semua'] + sorted(df['make'].dropna().unique().tolist())
selected_merk = st.sidebar.selectbox("Pilih Merk", merk_list)

# Filter berdasarkan tahun (slider)
tahun_min = int(df['year'].min())
tahun_max = int(df['year'].max())
selected_tahun = st.sidebar.slider(
    "Rentang Tahun", 
    tahun_min, 
    tahun_max, 
    (tahun_min, tahun_max)
)

# Filter berdasarkan harga (slider)
harga_min = int(df['price'].min())
harga_max = int(df['price'].max())
selected_harga = st.sidebar.slider(
    "Rentang Harga", 
    harga_min, 
    harga_max, 
    (harga_min, harga_max)
)

# ==================== APLIKASI FILTER ====================
filtered_df = df.copy()

if selected_merk != 'Semua':
    filtered_df = filtered_df[filtered_df['make'] == selected_merk]

filtered_df = filtered_df[
    (filtered_df['year'] >= selected_tahun[0]) & 
    (filtered_df['year'] <= selected_tahun[1])
]

filtered_df = filtered_df[
    (filtered_df['price'] >= selected_harga[0]) & 
    (filtered_df['price'] <= selected_harga[1])
]

# ==================== METRIK UTAMA ====================
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📊 Total Data", f"{len(filtered_df):,}")
with col2:
    st.metric("💰 Harga Rata-rata", f"Rp {filtered_df['price'].mean():,.0f}")
with col3:
    st.metric("📅 Tahun Rata-rata", f"{filtered_df['year'].mean():.0f}")
with col4:
    if 'odometer' in filtered_df.columns:
        st.metric("📏 Rata-rata Kilometer", f"{filtered_df['odometer'].mean():,.0f} km")

st.divider()

# ==================== VISUALISASI ====================
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📊 Distribusi Harga")
    fig1 = px.histogram(
        filtered_df, 
        x="price", 
        nbins=30,
        title="Distribusi Harga Mobil Bekas",
        labels={"price": "Harga"}
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_chart2:
    st.subheader("📈 Harga vs Tahun")
    fig2 = px.scatter(
        filtered_df, 
        x="year", 
        y="price",
        title="Hubungan Tahun dengan Harga",
        labels={"year": "Tahun", "price": "Harga"},
        opacity=0.6
    )
    st.plotly_chart(fig2, use_container_width=True)

# ==================== TABEL DATA ====================
st.subheader("📋 Data Mobil Bekas")
st.dataframe(filtered_df, use_container_width=True)

# ==================== FOOTER ====================
st.caption("Dashboard dibuat dengan Streamlit & Plotly | Data mobil bekas")