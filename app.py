import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# Judul Aplikasi
# ----------------------------
st.set_page_config(page_title="Model Persediaan EOQ", layout="centered")
st.title("📦 Model Persediaan EOQ (Economic Order Quantity)")
st.write("Aplikasi ini membantu menghitung jumlah pemesanan optimal (EOQ) untuk meminimalkan total biaya persediaan.")

# ----------------------------
# Sidebar: Dokumentasi
# ----------------------------
st.sidebar.title("📘 Instruksi Penggunaan")
st.sidebar.markdown("""
**Economic Order Quantity (EOQ)** adalah metode untuk menentukan jumlah pembelian yang optimal agar biaya total persediaan minimal.

### 📥 Input yang Diperlukan:
- Permintaan tahunan (**D**)
- Biaya pemesanan per kali pesan (**S**)
- Biaya penyimpanan per unit per tahun (**H**)

### 📤 Output:
- Nilai EOQ
- Total biaya tahunan
- Grafik hubungan biaya dan kuantitas
""")

# ----------------------------
# Contoh Studi Kasus
# ----------------------------
with st.expander("📖 Contoh Studi Kasus Industri"):
    st.markdown("""
**PT. **, sebuah pabrik komponen otomotif, ingin mengoptimalkan pembelian baut baja untuk produksi:

- Permintaan tahunan: `12.000 unit`
- Biaya pemesanan: `Rp 200.000` per pesanan
- Biaya penyimpanan: `Rp 500` per unit per tahun

""")

# ----------------------------
# Input Pengguna
# ----------------------------
st.subheader("📊 Masukkan Parameter")
col1, col2, col3 = st.columns(3)

with col1:
    D = st.number_input("Permintaan Tahunan (D)", min_value=1, value=12000, step=100)
with col2:
    S = st.number_input("Biaya Pemesanan per Kali (S)", min_value=1, value=200000, step=1000)
with col3:
    H = st.number_input("Biaya Penyimpanan per Unit per Tahun (H)", min_value=1, value=500, step=10)

# ----------------------------
# Perhitungan EOQ
# ----------------------------
if D > 0 and S > 0 and H > 0:
    EOQ = np.sqrt((2 * D * S) / H)
    num_orders = D / EOQ
    total_cost = (D / EOQ) * S + (EOQ / 2) * H

    st.subheader("📈 Hasil Perhitungan")
    st.write(f"✅ **EOQ (Economic Order Quantity)**: `{EOQ:.2f}` unit")
    st.write(f"📦 Jumlah Pemesanan per Tahun: `{num_orders:.2f}` kali")
    st.write(f"💰 Total Biaya Persediaan Tahunan: `Rp {total_cost:,.2f}`")

# ----------------------------
# Visualisasi Grafik
# ----------------------------
st.subheader("📉 Grafik Total Biaya vs Jumlah Pesanan")

Q_range = np.linspace(1, 2 * EOQ, 100)
TC_range = (D / Q_range) * S + (Q_range / 2) * H

fig, ax = plt.subplots()
ax.plot(Q_range, TC_range, label="Total Cost", color="blue")
ax.axvline(EOQ, color="red", linestyle="--", label=f"EOQ = {EOQ:.2f}")
ax.set_xlabel("Jumlah Pesanan (Q)")
ax.set_ylabel("Total Biaya (Rp)")
ax.set_title("Total Cost vs Order Quantity")
ax.legend()
ax.grid(True)

    st.pyplot(fig)
else:
    st.warning("Silakan isi semua parameter dengan nilai lebih dari 0.")
