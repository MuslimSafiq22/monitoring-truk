import streamlit as st
import requests
from datetime import date

# Ganti dengan URL SheetBest kamu
API_URL = "https://api.sheetbest.com/sheets/b01b34e5-1391-4312-9230-3f18cb3e3214"  # Ganti dengan URL SheetBest kamu

st.set_page_config(page_title="Monitoring Truk", page_icon="🚚", layout="centered")

st.title("🚚 Sistem Monitoring Truk")
st.markdown("Isi data monitoring truk dan simpan ke Google Sheets secara real-time.")

# Form input data
with st.form("form_monitoring"):
    st.subheader("📥 Input Data Truk")
    tanggal = st.date_input("Tanggal", value=date.today())
    id_truk = st.text_input("ID Truk")
    berat_bersih = st.number_input("Berat Bersih (kg)", min_value=0, step=100)
    berat_muatan = st.number_input("Berat Muatan (kg)", min_value=0, step=100)
    total_berat = berat_bersih + berat_muatan
    jarak = st.number_input("Jarak Tempuh (km)", min_value=0, step=1)
    bbm = st.number_input("BBM Diisi (liter)", min_value=0, step=1)
    lokasi_awal = st.text_input("Lokasi Awal")
    tujuan = st.text_input("Tujuan")

    submitted = st.form_submit_button("💾 Simpan Data")

# Proses kirim data ke SheetBest
if submitted:
    data = {
        "tanggal": str(tanggal),
        "id_truk": id_truk,
        "berat_bersih": berat_bersih,
        "berat_muatan": berat_muatan,
        "total_berat": total_berat,
        "jarak": jarak,
        "bbm": bbm,
        "lokasi_awal": lokasi_awal,
        "tujuan": tujuan
    }

    res = requests.post(API_URL, json=data)

    if res.status_code == 200:
        st.success("✅ Data berhasil dikirim ke Google Sheets!")
    else:
        st.error("❌ Gagal mengirim data. Periksa koneksi dan URL SheetBest.")

st.markdown("---")

# Tampilkan data monitoring dari Google Sheets
st.subheader("📋 Data Monitoring Truk")

res = requests.get(API_URL)
if res.status_code == 200:
    data = res.json()
    if len(data) > 0:
        st.dataframe(data)
    else:
        st.info("Belum ada data yang tersimpan.")
else:
    st.error("Gagal mengambil data dari Google Sheets.")