import streamlit as st
import pandas as pd
from io import BytesIO

# ===================== KONFIGURASI =====================
st.set_page_config(
    page_title="Aplikasi Laporan Keuangan",
    layout="wide",
    page_icon="📊"
)

# ===================== CSS UI =====================
st.markdown("""
<style>
.main { background-color: #f8f9fa; }
h1, h2, h3 { color: #2c3e50; }
.card {
    padding: 20px;
    border-radius: 12px;
    background: white;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}
section[data-testid="stSidebar"] {
    background-color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

# ===================== SESSION =====================
if "data" not in st.session_state:
    st.session_state.data = []

# ===================== MODE =====================
mode = st.sidebar.radio(
    "Mode Tampilan",
    ["Mode Tugas Dasar", "Mode Aplikasi Sederhana"]
)

def info_tugas(teks):
    if mode == "Mode Tugas Dasar":
        st.info(teks)

# ===================== MASTER AKUN =====================
JENIS_AKUN_MAP = {
    "kas": "Aset",
    "bank": "Aset",
    "piutang": "Aset",

    "utang": "Kewajiban",
    "utang usaha": "Kewajiban",

    "modal": "Ekuitas",
    "prive": "Ekuitas",

    "pendapatan": "Pendapatan",
    "penjualan": "Pendapatan",

    "beban": "Beban",
    "belanja": "Beban"
}

def jenis_akun(akun):
    return JENIS_AKUN_MAP.get(akun.lower(), "Lainnya")

def rupiah(x):
    return f"Rp {x:,.0f}".replace(",", ".")

# ===================== LOGIKA AKUNTANSI =====================
def hitung_laba_rugi(df):
    pendapatan = df[(df["Jenis Akun"] == "Pendapatan") & (df["Posisi"] == "Kredit")]["Jumlah"].sum()
    beban = df[(df["Jenis Akun"] == "Beban") & (df["Posisi"] == "Debit")]["Jumlah"].sum()
    return pendapatan, beban, pendapatan - beban

def hitung_saldo(row):
    if row["Jenis Akun"] in ["Aset", "Beban"]:
        return row["Jumlah"] if row["Posisi"] == "Debit" else -row["Jumlah"]
    else:
        return row["Jumlah"] if row["Posisi"] == "Kredit" else -row["Jumlah"]

# ===================== MENU =====================
menu = st.sidebar.selectbox(
    "Menu",
    ["Jurnal Umum", "Buku Besar", "Laba Rugi", "Neraca", "Lihat Semua", "Export Excel"]
)

df = pd.DataFrame(st.session_state.data)

# ===================== JURNAL UMUM =====================
if menu == "Jurnal Umum":
    st.markdown("<h1> Jurnal Umum</h1>", unsafe_allow_html=True)
    info_tugas("Jurnal umum digunakan untuk mencatat seluruh transaksi keuangan berdasarkan debit dan kredit.")

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    with st.form("form_jurnal"):
        col1, col2 = st.columns(2)
        with col1:
            tanggal = st.date_input("Tanggal")
            akun = st.text_input("Nama Akun")
        with col2:
            posisi = st.radio("Posisi", ["Debit", "Kredit"])
            jumlah = st.number_input("Jumlah", min_value=0.0)

        simpan = st.form_submit_button("Simpan")
        if simpan:
            st.session_state.data.append({
                "Tanggal": tanggal,
                "Akun": akun,
                "Posisi": posisi,
                "Jumlah": jumlah
            })
            st.success("Transaksi berhasil disimpan")
    st.markdown("</div>", unsafe_allow_html=True)

    if not df.empty:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Data Jurnal")
        st.dataframe(df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ===================== BUKU BESAR =====================
elif menu == "Buku Besar":
    st.markdown("<h1> Buku Besar</h1>", unsafe_allow_html=True)
    info_tugas("Buku besar mengelompokkan transaksi ke masing-masing akun untuk mengetahui saldo.")

    if not df.empty:
        df["Jenis Akun"] = df["Akun"].apply(jenis_akun)
        df["Debit"] = df.apply(lambda x: x["Jumlah"] if x["Posisi"] == "Debit" else 0, axis=1)
        df["Kredit"] = df.apply(lambda x: x["Jumlah"] if x["Posisi"] == "Kredit" else 0, axis=1)
        df["Saldo"] = df.apply(hitung_saldo, axis=1)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.dataframe(
            df.groupby(["Jenis Akun", "Akun"])[["Debit", "Kredit", "Saldo"]].sum().reset_index(),
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Belum ada transaksi")

# ===================== LABA RUGI =====================
elif menu == "Laba Rugi":
    st.markdown("<h1> Laporan Laba Rugi</h1>", unsafe_allow_html=True)
    info_tugas("Laporan laba rugi menunjukkan perbandingan pendapatan dan beban dalam satu periode.")

    if not df.empty:
        df["Jenis Akun"] = df["Akun"].apply(jenis_akun)
        pendapatan, beban, laba = hitung_laba_rugi(df)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Pendapatan", rupiah(pendapatan))
        col2.metric("Beban", rupiah(beban))
        col3.metric("Laba Bersih", rupiah(laba))
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Belum ada transaksi")

# ===================== NERACA (OPSI 3) =====================
elif menu == "Neraca":
    st.markdown("<h1> Neraca</h1>", unsafe_allow_html=True)
    info_tugas(
        "Neraca disajikan setelah penutupan periode. "
        "Pendapatan dan beban telah ditutup ke ekuitas (laba ditahan)."
    )

    if not df.empty:
        df["Jenis Akun"] = df["Akun"].apply(jenis_akun)
        df["Saldo"] = df.apply(hitung_saldo, axis=1)

        pendapatan, beban, laba = hitung_laba_rugi(df)

        neraca = df[df["Jenis Akun"].isin(["Aset", "Kewajiban", "Ekuitas"])] \
            .groupby(["Jenis Akun", "Akun"])["Saldo"].sum().reset_index()

        neraca = pd.concat([
            neraca,
            pd.DataFrame([{
                "Jenis Akun": "Ekuitas",
                "Akun": "Laba Ditahan",
                "Saldo": laba
            }])
        ], ignore_index=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("ASET")
            aset = neraca[neraca["Jenis Akun"] == "Aset"]
            st.dataframe(aset, use_container_width=True)
            st.metric("Total Aset", rupiah(aset["Saldo"].sum()))
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("KEWAJIBAN & EKUITAS")
            kew_eku = neraca[neraca["Jenis Akun"].isin(["Kewajiban", "Ekuitas"])]
            st.dataframe(kew_eku, use_container_width=True)
            st.metric("Total Kewajiban + Ekuitas", rupiah(kew_eku["Saldo"].sum()))
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Belum ada transaksi")

# ===================== LIHAT SEMUA =====================
elif menu == "Lihat Semua":
    st.markdown("<h1> Lihat Semua Laporan</h1>", unsafe_allow_html=True)

    info_tugas(
        "Halaman ini menampilkan seluruh proses akuntansi mulai dari jurnal umum, "
        "buku besar, laporan laba rugi, hingga neraca setelah penutupan."
    )

    if not df.empty:
        # ===== PREPARASI DATA =====
        df["Jenis Akun"] = df["Akun"].apply(jenis_akun)
        df["Debit"] = df.apply(lambda x: x["Jumlah"] if x["Posisi"] == "Debit" else 0, axis=1)
        df["Kredit"] = df.apply(lambda x: x["Jumlah"] if x["Posisi"] == "Kredit" else 0, axis=1)
        df["Saldo"] = df.apply(hitung_saldo, axis=1)

        pendapatan, beban, laba = hitung_laba_rugi(df)

        # ===== JURNAL UMUM =====
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Jurnal Umum")
        st.dataframe(df[["Tanggal", "Akun", "Posisi", "Jumlah"]], use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # ===== BUKU BESAR =====
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Buku Besar")
        buku_besar = df.groupby(["Jenis Akun", "Akun"])[["Debit", "Kredit", "Saldo"]].sum().reset_index()
        st.dataframe(buku_besar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # ===== LABA RUGI =====
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Laporan Laba Rugi")
        col1, col2, col3 = st.columns(3)
        col1.metric("Pendapatan", rupiah(pendapatan))
        col2.metric("Beban", rupiah(beban))
        col3.metric("Laba Bersih", rupiah(laba))
        st.markdown("</div>", unsafe_allow_html=True)

        # ===== NERACA =====
        neraca = df[df["Jenis Akun"].isin(["Aset", "Kewajiban", "Ekuitas"])] \
            .groupby(["Jenis Akun", "Akun"])["Saldo"].sum().reset_index()

        neraca = pd.concat([
            neraca,
            pd.DataFrame([{
                "Jenis Akun": "Ekuitas",
                "Akun": "Laba Ditahan",
                "Saldo": laba
            }])
        ], ignore_index=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Neraca (Setelah Penutupan)")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**ASET**")
            st.dataframe(neraca[neraca["Jenis Akun"] == "Aset"], use_container_width=True)

        with col2:
            st.markdown("**KEWAJIBAN & EKUITAS**")
            st.dataframe(
                neraca[neraca["Jenis Akun"].isin(["Kewajiban", "Ekuitas"])],
                use_container_width=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.info("Belum ada transaksi")

# ===================== EXPORT =====================
elif menu == "Export Excel":
    st.title("Export Excel")

    if not df.empty:
        df["Jenis Akun"] = df["Akun"].apply(jenis_akun)
        df["Saldo"] = df.apply(hitung_saldo, axis=1)
        pendapatan, beban, laba = hitung_laba_rugi(df)

        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, "Jurnal Umum", index=False)
        st.download_button("Download Excel", output.getvalue(), "laporan.xlsx")
