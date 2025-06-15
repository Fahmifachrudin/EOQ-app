import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from scipy.optimize import linprog

st.set_page_config(page_title="Aplikasi Matematika Terapan", layout="centered")

st.title("📘 Aplikasi Matematika Terapan")

# ----------------- 1. Optimasi Produksi Roti -----------------
st.header("🔧 Optimasi Biaya Produksi Roti")
with st.expander("Lihat / Sembunyikan Optimasi Produksi"):
    max_kapasitas = st.number_input("Kapasitas Produksi Maksimum (unit)", min_value=1, value=1000)
    budget = st.number_input("Anggaran Maksimal (Rp)", min_value=1, value=1800000)
    harga_roti_manis = st.number_input("Biaya/unit Roti Manis (Rp)", min_value=1, value=2000)
    harga_roti_tawar = st.number_input("Biaya/unit Roti Tawar (Rp)", min_value=1, value=1500)
    permintaan_min_manis = st.number_input("Permintaan Min Roti Manis", min_value=0, value=300)
    permintaan_min_tawar = st.number_input("Permintaan Min Roti Tawar", min_value=0, value=400)

    if st.button("🔍 Hitung Optimasi"):
        c = [harga_roti_manis, harga_roti_tawar]
        A = [[1, 1], [harga_roti_manis, harga_roti_tawar]]
        b = [max_kapasitas, budget]
        bounds = [(permintaan_min_manis, None), (permintaan_min_tawar, None)]
        res = linprog(c=c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

        if res.success:
            x_opt, y_opt = res.x
            total_cost = c[0]*x_opt + c[1]*y_opt
            st.success("✔ Optimasi Berhasil!")
            st.write(f"Roti Manis: {x_opt:.0f} unit")
            st.write(f"Roti Tawar: {y_opt:.0f} unit")
            st.write(f"Total Biaya: Rp{int(total_cost):,}")

            fig, ax = plt.subplots(figsize=(8, 6))
            x_vals = np.linspace(permintaan_min_manis, max_kapasitas, 400)
            y1 = max_kapasitas - x_vals
            y2 = (budget - harga_roti_manis * x_vals) / harga_roti_tawar
            ax.plot(x_vals, y1, label=f"Kapasitas ≤ {max_kapasitas}", color='blue')
            ax.plot(x_vals, y2, label="Anggaran", color='green')
            ax.axvline(permintaan_min_manis, linestyle='--', color='orange', label="Min Roti Manis")
            ax.axhline(permintaan_min_tawar, linestyle='--', color='purple', label="Min Roti Tawar")
            ax.plot(x_opt, y_opt, 'ro', label="Titik Optimal")
            ax.set_xlim(0, max_kapasitas + 100)
            ax.set_ylim(0, max_kapasitas + 100)
            ax.set_xlabel("Roti Manis (x)")
            ax.set_ylabel("Roti Tawar (y)")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)
        else:
            st.error("❌ Optimasi gagal. Silakan periksa parameter input.")

# ----------------- 2. EOQ -----------------
st.header("📦 Model Persediaan EOQ (Koil Gulung)")
with st.expander("Lihat / Sembunyikan EOQ"):
    col1, col2, col3 = st.columns(3)
    with col1:
        D = st.number_input("Permintaan Tahunan (D)", value=2000, min_value=1, key="D")
    with col2:
        S = st.number_input("Biaya Pemesanan per Kali (S)", value=2000000, min_value=1, key="S")
    with col3:
        H = st.number_input("Biaya Penyimpanan per Unit per Tahun (H)", value=50000, min_value=1, key="H")

    EOQ = np.sqrt((2 * D * S) / H)
    freq = D / EOQ
    total_cost = (D / EOQ) * S + (EOQ / 2) * H

    st.write(f"EOQ: *{EOQ:.2f} unit*")
    st.write(f"Jumlah Pesanan per Tahun: *{freq:.2f} kali*")
    st.write(f"Total Biaya Tahunan: *Rp {total_cost:,.2f}*")

    Q = np.linspace(1, 2 * EOQ, 100)
    TC = (D / Q) * S + (Q / 2) * H
    fig, ax = plt.subplots()
    ax.plot(Q, TC, label="Total Biaya")
    ax.axvline(EOQ, color="red", linestyle="--", label=f"EOQ ≈ {EOQ:.0f}")
    ax.set_xlabel("Jumlah Pemesanan (Q)")
    ax.set_ylabel("Total Biaya (Rp)")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

# ----------------- 3. Antrian M/M/1 -----------------
st.header("📊 Simulasi Model Antrian M/M/1")
with st.expander("Lihat / Sembunyikan Simulasi Antrian"):
    def mm1_metrics(lam, mu):
        if lam >= mu:
            return None, None, None, None
        Wq = lam / (mu * (mu - lam))
        W = 1 / (mu - lam)
        Lq = (lam**2) / (mu * (mu - lam))
        L = lam / (mu - lam)
        return Wq * 60, W * 60, Lq, L

    mu = st.number_input("Laju pelayanan (μ) - orang per jam", min_value=1.0, value=10.0, step=1.0)
    lam = st.slider("Laju kedatangan (λ) - orang per jam", min_value=0.1, max_value=mu - 0.1, value=6.0, step=0.1)

    Wq, W, Lq, L = mm1_metrics(lam, mu)

    if Wq is None:
        st.error("Sistem tidak stabil: λ harus lebih kecil dari μ.")
    else:
        st.write(f"*Utilisasi (ρ)*: {round(lam/mu, 2)}")
        st.write(f"- Waktu Tunggu Antrian (Wq): {Wq:.2f} menit")
        st.write(f"- Waktu Total Sistem (W): {W:.2f} menit")
        st.write(f"- Rata-rata Orang dalam Antrian (Lq): {Lq:.2f}")
        st.write(f"- Rata-rata Orang dalam Sistem (L): {L:.2f}")

        lam_vals = np.linspace(0.1, mu - 0.1, 100)
        Wq_vals, W_vals = [], []
        for l in lam_vals:
            wq, w, _, _ = mm1_metrics(l, mu)
            Wq_vals.append(wq)
            W_vals.append(w)

        fig, ax = plt.subplots()
        ax.plot(lam_vals, Wq_vals, label='Waktu Menunggu (Wq)', color='orange')
        ax.plot(lam_vals, W_vals, label='Waktu Total (W)', color='blue')
        ax.axvline(x=mu, linestyle='--', color='red', label='μ (Batas Stabilitas)')
        ax.set_xlabel("Laju Kedatangan (λ) [orang/jam]")
        ax.set_ylabel("Waktu (menit)")
        ax.set_title("Pengaruh λ terhadap Waktu Sistem")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

# ----------------- 4. Kalkulator Integral -----------------
st.header("🧮 Kalkulator Integral")
with st.expander("Lihat / Sembunyikan Kalkulator Integral"):
    fungsi_input = st.text_input("Fungsi f(x):", value="x**2")
    jenis = st.radio("Pilih jenis integral:", ["Tak Tentu", "Tentu"])
    var_input = st.text_input("Variabel integrasi (misal: x, t):", value="x")
    x = sp.symbols(var_input)

    try:
        fungsi = sp.sympify(fungsi_input)

        if jenis == "Tentu":
            a = st.number_input("Batas bawah (a):", value=0.0)
            b = st.number_input("Batas atas (b):", value=2.0)
            hasil_integral = sp.integrate(fungsi, (x, a, b))
            st.latex(r"\int_{%s}^{%s} %s \,dx = %s" % (a, b, sp.latex(fungsi), sp.latex(hasil_integral)))
            st.write(f"Hasil numerik ≈ {float(hasil_integral):.4f}")

            fx = sp.lambdify(x, fungsi, "numpy")
            x_vals = np.linspace(float(a)-1, float(b)+1, 400)
            y_vals = fx(x_vals)
            fig, ax = plt.subplots()
            ax.plot(x_vals, y_vals, label=f"f({var_input}) = {fungsi_input}")
            ax.fill_between(x_vals, y_vals, where=(x_vals >= a) & (x_vals <= b), color='skyblue', alpha=0.5)
            ax.axhline(0, color='black', linewidth=0.5)
            ax.set_title("Area di bawah kurva")
            ax.legend()
            st.pyplot(fig)

        else:
            hasil_integral = sp.integrate(fungsi, x)
            st.latex(r"\int %s \,dx = %s + C" % (sp.latex(fungsi), sp.latex(hasil_integral)))

    except Exception as e:
        st.error(f"Terjadi kesalahan dalam memproses fungsi: {e}")
