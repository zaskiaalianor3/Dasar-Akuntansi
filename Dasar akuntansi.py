
import streamlit as st
import pandas as pd

# ================= CSS =================
st.markdown("""
<style>
body {background-color:#f5f7fa;}
.main {background:white;padding:20px;border-radius:10px;}
.stButton>button {background:#2ecc71;color:white;border-radius:8px;}
</style>
""", unsafe_allow_html=True)

st.title("📊 Aplikasi Akuntansi Sederhana")

# ================= SESSION =================
if "data" not in st.session_state:
    st.session_state.data = []

# ================= INPUT =================
st.subheader("➕ Input Transaksi")

with st.form("form"):
    tanggal = st.date_input("Tanggal")
    akun = st.text_input("Nama Akun")
    debit = st.number_input("Debit", min_value=0.0)
    kredit = st.number_input("Kredit", min_value=0.0)
    simpan = st.form_submit_button("Simpan")

    if simpan:
        st.session_state.data.append({
            "Tanggal": tanggal,
            "Akun": akun,
            "Debit": debit,
            "Kredit": kredit
        })
        st.success("Transaksi disimpan")

df = pd.DataFrame(st.session_state.data)

# ================= JURNAL UMUM =================
st.subheader("📘 Jurnal Umum")
if not df.empty:
    st.table(df)
else:
    st.info("Belum ada transaksi")

# ================= BUKU BESAR =================
st.subheader("📗 Buku Besar")
if not df.empty:
    buku_besar = df.groupby("Akun")[["Debit", "Kredit"]].sum().reset_index()
    st.table(buku_besar)

# ================= LABA RUGI =================
st.subheader("📈 Laporan Laba Rugi")
if not df.empty:
    total_debit = df["Debit"].sum()
    total_kredit = df["Kredit"].sum()
    laba = total_kredit - total_debit

    laba_rugi_df = pd.DataFrame({
        "Keterangan": ["Total Pendapatan", "Total Beban", "Laba / Rugi Bersih"],
        "Jumlah": [total_kredit, total_debit, laba]
    })

    c1, c2, c3 = st.columns(3)
    c1.metric("Pendapatan", f"Rp {total_kredit:,.0f}")
    c2.metric("Beban", f"Rp {total_debit:,.0f}")
    c3.metric("Laba / Rugi", f"Rp {laba:,.0f}")

    st.table(laba_rugi_df)

# ================= NERACA =================
st.subheader("📙 Neraca")
if not df.empty:
    aset = df["Debit"].sum()
    kewajiban_modal = df["Kredit"].sum()

    neraca = pd.DataFrame({
        "Keterangan": ["Total Aset", "Total Kewajiban + Modal"],
        "Jumlah": [aset, kewajiban_modal]
    })
    st.table(neraca)

# ================= SIMPAN KE EXCEL =================
st.subheader("💾 Simpan ke Excel")

if not df.empty:
    excel_file = "laporan_akuntansi.xlsx"

    with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Jurnal Umum", index=False)
        buku_besar.to_excel(writer, sheet_name="Buku Besar", index=False)
        laba_rugi_df.to_excel(writer, sheet_name="Laba Rugi", index=False)
        neraca.to_excel(writer, sheet_name="Neraca", index=False)

    with open(excel_file, "rb") as file:
        st.download_button(
            label="📥 Download Excel",
            data=file,
            file_name=excel_file,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("Isi data terlebih dahulu untuk menyimpan Excel")

st.markdown("---")
st.caption("© 2025 Aplikasi Akuntansi Sederhana")
