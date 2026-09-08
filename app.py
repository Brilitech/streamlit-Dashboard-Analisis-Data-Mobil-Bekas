import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# ==================== KONFIGURASI HALAMAN ====================
st.set_page_config(
    page_title="Dashboard Mobil Bekas + Prediksi",
    page_icon="🚗",
    layout="wide"
)

# ==================== LOAD DATASET ====================
@st.cache_data
def load_data():
    df = pd.read_csv("vehicles.csv")
    df.columns = df.columns.str.lower().str.strip()
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Gagal membaca file vehicles.csv: {e}")
    st.stop()

# Tampilkan nama kolom di sidebar untuk debugging (bisa dihapus nanti)
st.sidebar.write("Kolom yang tersedia:", df.columns.tolist())

# ==================== PREPROCESSING & TRAINING MODEL ====================
@st.cache_resource
def train_model(data):
    # Daftar kolom fitur
    feature_cols = ['model_year', 'odometer', 'condition', 'cylinders', 
                    'fuel', 'transmission', 'type', 'paint_color', 'is_4wd']
    target = 'price'
    
    # Cek ketersediaan kolom
    missing = [c for c in feature_cols if c not in data.columns]
    if missing:
        st.error(f"Kolom berikut tidak ditemukan: {missing}")
        st.stop()
    
    X = data[feature_cols].copy()
    y = data[target].copy()
    
    # Hapus baris dengan target NaN
    valid = y.notna()
    X = X[valid]
    y = y[valid]
    
    if len(X) == 0:
        st.error("Tidak ada data setelah membersihkan missing value.")
        st.stop()
    
    # Konversi numerik
    numeric_cols = ['model_year', 'odometer', 'cylinders']
    for col in numeric_cols:
        X[col] = pd.to_numeric(X[col], errors='coerce')
    
    # Konversi kategorikal ke string
    categorical_cols = ['condition', 'fuel', 'transmission', 'type', 'paint_color', 'is_4wd']
    for col in categorical_cols:
        X[col] = X[col].astype(str).fillna('missing').replace('nan', 'missing')
    
    # Preprocessor
    numeric_transformer = SimpleImputer(strategy='median')
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_cols),
            ('cat', categorical_transformer, categorical_cols)
        ])
    
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])
    
    model.fit(X, y)
    
    # Evaluasi
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model_eval = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])
    model_eval.fit(X_train, y_train)
    y_pred = model_eval.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    return model, mae, r2, feature_cols

# Training model dengan penanganan error
try:
    with st.spinner("Melatih model prediksi..."):
        model, mae, r2, feature_cols = train_model(df)
    st.sidebar.success("✅ Model berhasil dilatih!")
except Exception as e:
    st.sidebar.error(f"❌ Gagal melatih model: {e}")
    model = None
    mae = r2 = None
    feature_cols = []

# ==================== HEADER ====================
st.title("🚗 Dashboard Analisis & Prediksi Mobil Bekas")
st.markdown("""
Dashboard ini memungkinkan kamu mengeksplorasi data mobil bekas dan **memprediksi harga wajar** 
serta menilai **kelayakan** berdasarkan spesifikasi yang kamu masukkan.
""")

# ==================== SIDEBAR FILTER ====================
st.sidebar.header("🔍 Filter Data Eksplorasi")

# Filter berdasarkan model
model_choices = ['Semua'] + sorted(df['model'].dropna().unique().tolist())
selected_model = st.sidebar.selectbox("Model", model_choices)

# Filter tahun
year_min = int(df['model_year'].min())
year_max = int(df['model_year'].max())
selected_year = st.sidebar.slider("Tahun", year_min, year_max, (year_min, year_max))

# Filter harga
price_min = int(df['price'].min())
price_max = int(df['price'].max())
selected_price = st.sidebar.slider("Harga (Rp)", price_min, price_max, (price_min, price_max))

# Filter kondisi
condition_choices = ['Semua'] + sorted(df['condition'].dropna().unique().tolist())
selected_condition = st.sidebar.selectbox("Kondisi", condition_choices)

# Filter odometer
odo_min = int(df['odometer'].min())
odo_max = int(df['odometer'].max())
selected_odo = st.sidebar.slider("Odometer (km)", odo_min, odo_max, (odo_min, odo_max))

# Terapkan filter
filtered_df = df.copy()
if selected_model != 'Semua':
    filtered_df = filtered_df[filtered_df['model'] == selected_model]
filtered_df = filtered_df[
    (filtered_df['model_year'] >= selected_year[0]) & 
    (filtered_df['model_year'] <= selected_year[1])
]
filtered_df = filtered_df[
    (filtered_df['price'] >= selected_price[0]) & 
    (filtered_df['price'] <= selected_price[1])
]
if selected_condition != 'Semua':
    filtered_df = filtered_df[filtered_df['condition'] == selected_condition]
filtered_df = filtered_df[
    (filtered_df['odometer'] >= selected_odo[0]) & 
    (filtered_df['odometer'] <= selected_odo[1])
]

# ==================== METRIK UTAMA ====================
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📊 Total Data", f"{len(filtered_df):,}")
with col2:
    st.metric("💰 Harga Rata-rata", f"Rp {filtered_df['price'].mean():,.0f}")
with col3:
    st.metric("📅 Tahun Rata-rata", f"{filtered_df['model_year'].mean():.0f}")
with col4:
    st.metric("📏 Rata-rata Kilometer", f"{filtered_df['odometer'].mean():,.0f} km")

st.divider()

# ==================== VISUALISASI ====================
col_chart1, col_chart2 = st.columns(2)
with col_chart1:
    st.subheader("📊 Distribusi Harga")
    fig1 = px.histogram(filtered_df, x="price", nbins=30, title="Distribusi Harga")
    st.plotly_chart(fig1, use_container_width=True)

with col_chart2:
    st.subheader("📈 Harga vs Tahun")
    fig2 = px.scatter(filtered_df, x="model_year", y="price", title="Harga vs Tahun", opacity=0.6)
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("📋 Data Mobil Bekas (Hasil Filter)")
st.dataframe(filtered_df, use_container_width=True)

# ==================== FITUR PREDIKSI ====================
st.divider()
st.header("🔮 Prediksi Harga & Kelayakan Mobil")

if model is None:
    st.warning("Model prediksi tidak tersedia karena error. Periksa dataset dan coba lagi.")
else:
    st.markdown("""
    Masukkan spesifikasi mobil yang ingin kamu evaluasi. Model akan memprediksi harga wajar, 
    lalu membandingkannya dengan harga yang kamu masukkan. 
    **Layak** berarti harga yang kamu masukkan lebih rendah dari prediksi (murah), 
    **Tidak Layak** berarti lebih mahal dari prediksi.
    """)
    
    with st.form("prediction_form"):
        col_in1, col_in2 = st.columns(2)
        
        with col_in1:
            input_price = st.number_input("💰 Harga Mobil (Rp)", min_value=0, value=10000000, step=1000000)
            input_year = st.number_input("📅 Tahun Pembuatan", min_value=1990, max_value=2025, value=2015)
            input_odometer = st.number_input("📏 Odometer (km)", min_value=0, value=80000, step=1000)
            input_cylinders = st.selectbox("🔧 Jumlah Silinder", options=sorted(df['cylinders'].dropna().unique()), index=0)
        
        with col_in2:
            input_condition = st.selectbox("🔍 Kondisi", options=sorted(df['condition'].dropna().unique()), index=0)
            input_fuel = st.selectbox("⛽ Bahan Bakar", options=sorted(df['fuel'].dropna().unique()), index=0)
            input_transmission = st.selectbox("⚙ Transmisi", options=sorted(df['transmission'].dropna().unique()), index=0)
            input_type = st.selectbox("🚗 Tipe Kendaraan", options=sorted(df['type'].dropna().unique()), index=0)
            input_paint = st.selectbox("🎨 Warna Cat", options=sorted(df['paint_color'].dropna().unique()), index=0)
            input_4wd = st.selectbox("4WD", options=[0, 1], format_func=lambda x: "Ya" if x==1 else "Tidak")
        
        submitted = st.form_submit_button("Prediksi Sekarang")
    
    if submitted:
        # Buat input dataframe
        input_data = pd.DataFrame({
            'model_year': [input_year],
            'odometer': [input_odometer],
            'condition': [input_condition],
            'cylinders': [input_cylinders],
            'fuel': [input_fuel],
            'transmission': [input_transmission],
            'type': [input_type],
            'paint_color': [input_paint],
            'is_4wd': [input_4wd]
        })
        
        # Prediksi
        try:
            predicted_price = model.predict(input_data)[0]
            
            # Penilaian kelayakan
            threshold = 0.9
            if input_price <= predicted_price * threshold:
                status = "✅ LAYAK"
                color = "green"
                detail = f"Harga yang Anda masukkan **{input_price:,.0f}** lebih rendah dari harga pasar prediksi **{predicted_price:,.0f}** (diskon > {100 - threshold*100:.0f}%). Mobil ini tergolong murah."
            elif input_price <= predicted_price:
                status = "⚠️ CUKUP LAYAK"
                color = "orange"
                detail = f"Harga Anda **{input_price:,.0f}** masih di bawah prediksi pasar **{predicted_price:,.0f}**, tapi tidak terlalu jauh. Masih tergolong wajar."
            else:
                status = "❌ TIDAK LAYAK"
                color = "red"
                detail = f"Harga yang Anda masukkan **{input_price:,.0f}** lebih tinggi dari prediksi pasar **{predicted_price:,.0f}**. Mobil ini tergolong mahal."
            
            st.subheader("📊 Hasil Prediksi")
            col_res1, col_res2, col_res3 = st.columns(3)
            with col_res1:
                st.metric("Harga Input", f"Rp {input_price:,.0f}")
            with col_res2:
                st.metric("Harga Prediksi", f"Rp {predicted_price:,.0f}", delta=f"{predicted_price - input_price:,.0f}")
            with col_res3:
                st.metric("Status Kelayakan", status, delta_color="off")
            
            st.markdown(f"<div style='background-color:{color}20; padding:15px; border-radius:10px; border-left:5px solid {color};'>{detail}</div>", unsafe_allow_html=True)
            
            if mae is not None and r2 is not None:
                with st.expander("ℹ️ Performa Model"):
                    st.write(f"**Mean Absolute Error (MAE):** Rp {mae:,.0f}")
                    st.write(f"**R² Score:** {r2:.3f}")
                    st.write("MAE adalah rata-rata selisih absolut antara harga prediksi dan aktual. R² menunjukkan seberapa baik model menjelaskan variasi harga.")
        except Exception as e:
            st.error(f"Gagal melakukan prediksi: {e}")

# ==================== FOOTER ====================
st.caption("Dashboard dibuat dengan Streamlit, Plotly, dan scikit-learn | Data mobil bekas")
