# 🚗 Dashboard Analisis & Prediksi Mobil Bekas

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://cyalebbxueovzqmu5hnkgx.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Dashboard interaktif untuk **eksplorasi data mobil bekas** dan **prediksi harga wajar** menggunakan _Machine Learning_. Dilengkapi dengan fitur penilaian kelayakan harga sehingga Anda bisa mengetahui apakah harga yang ditawarkan _Layak_, _Cukup_, atau _Tidak Layak_ berdasrkan harga mobil dipasaran berdasarkan dataset.

🔗 **Demo Online:** [https://cyalebbxueovzqmu5hnkgx.streamlit.app/](https://cyalebbxueovzqmu5hnkgx.streamlit.app/)

---

## 📖 Deskripsi

Proyek ini dibuat untuk membantu calon pembeli mobil bekas dalam menganalisis pasar dan menilai harga. Dengan memanfaatkan dataset mobil bekas, dashboard ini menyajikan:

- Filter data interaktif (model, tahun, harga, kondisi, odometer)
- Visualisasi distribusi harga dan hubungan harga vs tahun
- Metrik ringkasan (total data, rata‑rata harga, tahun, kilometer)
- **Prediksi harga** menggunakan algoritma **Linear Regression**
- **Penilaian kelayakan** – apakah harga input tergolong _Layak_, _Cukup Layak_, atau _Tidak Layak_

---

## ✨ Fitur Unggulan

| Fitur | Deskripsi |
|-------|-----------|
| 🔍 **Filter Interaktif** | Filter data berdasarkan model, tahun, harga, kondisi, dan odometer. |
| 📊 **Visualisasi Dinamis** | Histogram harga dan scatter plot harga vs tahun dengan Plotly. |
| 📈 **Metrik Instan** | Total data, rata‑rata harga, tahun, dan kilometer langsung terupdate. |
| 🤖 **Prediksi Harga** | Masukkan spesifikasi mobil, dapatkan prediksi harga pasar. |
| ✅ **Penilaian Kelayakan** | Bandingkan harga input dengan prediksi, dapatkan status layak/tidak. |
| 📋 **Tabel Data** | Lihat data hasil filter secara lengkap. |

---

## 🛠️ Teknologi yang Digunakan

- **Python 3.10**
- **Streamlit** – framework dashboard
- **Pandas & NumPy** – manipulasi data
- **Plotly** – visualisasi interaktif
- **Scikit-learn** – model _Linear Regression_ dan preprocessing

---

## 🚀 Cara Menjalankan di Lokal

1. **Clone repository**
   ```bash
   git clone https://github.com/Brilitech/streamlit-Dashboard-Analisis-Data-Mobil-Bekas.git
   cd streamlit-Dashboard-Analisis-Data-Mobil-Bekas
