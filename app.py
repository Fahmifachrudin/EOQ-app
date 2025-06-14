import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Konfigurasi halaman
st.set_page_config(page_title="Model EOQ - Koil Gulung", layout="centered")

# Judul
st.title("📦 Model Persediaan EOQ (Koil Gulung)")
st.markdown("Menghitung jumlah pemesanan optimal untuk meminimalkan total biaya persediaan.")

# Sidebar dokumentasi
st.sidebar.title("📘 Dokumentasi")
st.sidebar.markdown("""
### Economic Order Quantity (EOQ)
EOQ digunakan untuk menentukan **jumlah pembelian optimal** agar biaya total persediaan minimal.

**Input:**
- Permintaan tahunan (D)
- Biaya pemesanan (S)
- Biaya penyimpanan (H)

**Output:**
- Nilai EOQ
- Jumlah pemesanan per tahun
- Total biaya tahunan
- Grafik total biaya vs kuantitas
""")

# Input parameter
st.header("📊 Input Parameter")
col1, col2, col3 = st.columns(3)

with col1:
    D = st.number_input("Permintaan Tahunan (D)", value=2000, min_value=1)
with col2:
    S = st.number_input("Biaya Pemesanan per Kali (S)", value=2000000, min_value=1)
with col3:
    H = st.number_input("Biaya Penyimpanan per Unit per Tahun (H)", value=50000, min_value=1)

# Perhitungan EOQ
if D > 0 and S > 0 and H > 0:
    EOQ = np.sqrt((2 * D * S) / H)
    order_freq = D / EOQ
    total_cost = (D / EOQ) * S + (EOQ / 2) * H

    st.subheader("📈 Hasil Perhitungan EOQ")
    st.write(f"✅ **EOQ (Jumlah Pemesanan Optimal):** `{EOQ:.2f}` unit")
    st.write(f"📦 **Jumlah Pemesanan per Tahun:** `{order_freq:.2f}` kali")
    st.write(f"💰 **Total Biaya Persediaan Tahunan:** `Rp {total_cost:,.2f}`")

    # Grafik Total Biaya vs Jumlah Pemesanan
    st.subheader("📉 Grafik: Total Biaya vs Kuantitas Pemesanan")
    Q = np.linspace(1, 2 * EOQ, 100)
    TC = (D / Q) * S + (Q / 2) * H

    fig, ax = plt.subplots()
    ax.plot(Q, TC, label="Total Biaya", color="blue")
    ax.axvline(EOQ, color="red", linestyle="--", label=f"EOQ ≈ {EOQ:.0f}")
    ax.set_xlabel("Jumlah Pemesanan (Q)")
    ax.set_ylabel("Total Biaya (Rp)")
    ax.set_title("Total Biaya vs Kuantitas Pemesanan")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)
else:
    st.warning("Silakan masukkan nilai > 0 untuk semua parameter.")
