import streamlit as st
import pandas as pd
import plotly.express as px
import re

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
    # Ubah semua nama kolom ke huruf kecil dan hapus spasi di awal/akhir
    df.columns = df.columns.str.lower().str.strip()
    return df

df = load_data()

# ==================== FUNGSI PENCARIAN KOLOM ====================
def find_column(df, keywords):
    """Cari kolom yang mengandung salah satu kata kunci (case-insensitive)"""
    for col in df.columns:
        for kw in keywords:
            if kw in col:
                return col
    return None

# ==================== TAMPILKAN DAFTAR KOLOM (untuk debugging) ====================
st.sidebar.markdown("### 📋 Nama Kolom yang Terdeteksi")
st.sidebar.write(df.columns.tolist())

# Cari kolom penting
price_col = find_column(df, ['price', 'harga'])
year_col = find_column(df, ['year', 'tahun', 'model_year'])
make_col = find_column(df, ['make', 'brand', 'manufacturer', 'merk', 'model'])
odo_col = find_column(df, ['odometer', 'mileage', 'kilometer', 'km'])

# Jika kolom tahun tidak ditemukan, coba ekstrak dari kolom model (jika ada)
if year_col is None and make_col is not None:
    # Coba ambil 4 digit angka dari awal nilai di kolom make (misal "2011 bmw x5")
    # Buat kolom tahun baru
    df['tahun_detected'] = df[make_col].astype(str).str.extract(r'^(\d{4})').astype(float)
    year_col = 'tahun_detected'
    st.sidebar.info("Kolom tahun tidak ditemukan, saya ekstrak dari kolom 'model'.")

# Jika masih tidak ada, beri error
if price_col is None or year_col is None:
    st.error("❌ Kolom 'price' atau 'year' tidak ditemukan. Silakan periksa nama kolom di sidebar.")
    st.stop()

# ==================== HEADER ====================
st.title("🚗 Dashboard Analisis Mobil Bekas")
st.markdown("""
Dashboard ini memungkinkan kamu mengeksplorasi data mobil bekas secara interaktif. 
Gunakan filter di sidebar untuk menyaring data sesuai keinginanmu.
""")

# ==================== SIDEBAR FILTER ====================
st.sidebar.header("🔍 Filter Data")

# Filter berdasarkan merek (gunakan kolom make jika ada, atau model)
if make_col is not None:
    unique_marks = sorted(df[make_col].dropna().unique().tolist())
    merk_list = ['Semua'] + unique_marks
    selected_merk = st.sidebar.selectbox("Pilih Merk / Model", merk_list)
else:
    selected_merk = 'Semua'

# Filter berdasarkan tahun
tahun_min = int(df[year_col].min())
tahun_max = int(df[year_col].max())
selected_tahun = st.sidebar.slider(
    "Rentang Tahun", 
    tahun_min, 
    tahun_max, 
    (tahun_min, tahun_max)
)

# Filter berdasarkan harga
harga_min = int(df[price_col].min())
harga_max = int(df[price_col].max())
selected_harga = st.sidebar.slider(
    "Rentang Harga", 
    harga_min, 
    harga_max, 
    (harga_min, harga_max)
)

# ==================== APLIKASI FILTER ====================
filtered_df = df.copy()

if selected_merk != 'Semua' and make_col is not None:
    filtered_df = filtered_df[filtered_df[make_col] == selected_merk]

filtered_df = filtered_df[
    (filtered_df[year_col] >= selected_tahun[0]) & 
    (filtered_df[year_col] <= selected_tahun[1])
]

filtered_df = filtered_df[
    (filtered_df[price_col] >= selected_harga[0]) & 
    (filtered_df[price_col] <= selected_harga[1])
]

# ==================== METRIK UTAMA ====================
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📊 Total Data", f"{len(filtered_df):,}")
with col2:
    st.metric("💰 Harga Rata-rata", f"Rp {filtered_df[price_col].mean():,.0f}")
with col3:
    st.metric("📅 Tahun Rata-rata", f"{filtered_df[year_col].mean():.0f}")
with col4:
    if odo_col is not None:
        st.metric("📏 Rata-rata Kilometer", f"{filtered_df[odo_col].mean():,.0f} km")
    else:
        st.metric("📏 Odometer", "Tidak tersedia")

st.divider()

# ==================== VISUALISASI ====================
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📊 Distribusi Harga")
    fig1 = px.histogram(
        filtered_df, 
        x=price_col, 
        nbins=30,
        title="Distribusi Harga Mobil Bekas",
        labels={price_col: "Harga"}
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_chart2:
    st.subheader("📈 Harga vs Tahun")
    fig2 = px.scatter(
        filtered_df, 
        x=year_col, 
        y=price_col,
        title="Hubungan Tahun dengan Harga",
        labels={year_col: "Tahun", price_col: "Harga"},
        opacity=0.6
    )
    st.plotly_chart(fig2, use_container_width=True)

# ==================== TABEL DATA ====================
st.subheader("📋 Data Mobil Bekas")
st.dataframe(filtered_df, use_container_width=True)

# ==================== FOOTER ====================
st.caption("Dashboard dibuat dengan Streamlit & Plotly | Data mobil bekas")
