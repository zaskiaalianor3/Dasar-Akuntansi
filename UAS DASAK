import streamlit as st
import pandas as pd
from io import BytesIO

# ===================== KONFIGURASI =====================
st.set_page_config(
    page_title="Aplikasi Akuntansi",
    layout="wide",
    page_icon="📊"
)

# ===================== CSS MODERN (BIRU PUTIH) =====================
st.markdown("""
<style>
/* ===== Background App ===== */
.stApp {
    background-color: #F8FAFC;
}

/* ===== Sidebar ===== */
section[data-testid="stSidebar"] {
    background-color: #1E3A8A;
}

/* Default teks sidebar */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* ===== RADIO MENU ===== */
div[data-testid="stRadio"] > div {
    background-color: white;
    border-radius: 14px;
    padding: 10px;
}

/* Item menu */
div[data-testid="stRadio"] label {
    padding: 12px 16px;
    border-radius: 10px;
    font-weight: 600;
    color: #1E293B !important;
}

/* HOVER */
div[data-testid="stRadio"] label:hover {
    background-color: #E0E7FF;
    color: #1E3A8A !important;
}

/* ITEM TERPILIH (INI YANG PENTING) */
div[data-testid="stRadio"] label[data-selected="true"] {
    background-color: #2563EB !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)


# ===================== SESSION STATE =====================
if "data" not in st.session_state:
    st.session_state.data = []

if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

# ===================== MASTER JENIS AKUN =====================
JENIS_AKUN_MAP = {
    "kas": "Aset",
    "piutang": "Aset",
    "perlengkapan": "Aset",
    "utang": "Kewajiban",
    "utang usaha": "Kewajiban",
    "modal": "Ekuitas",
    "pendapatan": "Pendapatan",
    "penjualan": "Pendapatan",
    "beban": "Beban",
    "belanja": "Beban"
}

def jenis_akun(akun):
    return JENIS_AKUN_MAP.get(akun.lower(), "Lainnya")

def rupiah(x):
    return f"Rp {x:,.0f}".replace(",", ".")

# ===================== SIDEBAR =====================
menu = st.sidebar.selectbox(
    "Menu",
    [
        "Home & Jurnal",
        "Lihat Semua",
        "Buku Besar",
        "Laba Rugi",
        "Neraca",
        "Export Excel"
    ]
)

df = pd.DataFrame(st.session_state.data)

# ===================== HOME + JURNAL UMUM =====================
if menu == "Home & Jurnal":
    st.title("APLIKASI AKUNTANSI SEDERHANA")
    st.write("Input transaksi dan lihat laporan secara otomatis")

    # ===== DASHBOARD =====
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Transaksi", len(df))
    col2.metric("Total Debit", rupiah(df[df["Posisi"] == "Debit"]["Jumlah"].sum()) if not df.empty else "Rp 0")
    col3.metric("Total Kredit", rupiah(df[df["Posisi"] == "Kredit"]["Jumlah"].sum()) if not df.empty else "Rp 0")

    st.divider()

    # ===== FORM JURNAL =====
    st.subheader("Input Jurnal Umum")
    with st.container(border=True):
        with st.form("form_jurnal"):
            col1, col2 = st.columns(2)
            with col1:
                tanggal = st.date_input("Tanggal")
                akun = st.text_input("Nama Akun")
            with col2:
                posisi = st.radio("Posisi", ["Debit", "Kredit"], horizontal=True)
                jumlah = st.number_input("Jumlah", min_value=0.0)

            simpan = st.form_submit_button("Simpan Transaksi")

            if simpan:
                st.session_state.data.append({
                    "Tanggal": tanggal,
                    "Akun": akun,
                    "Posisi": posisi,
                    "Jumlah": jumlah
                })
                st.success("Transaksi berhasil disimpan")
                st.experimental_rerun()

    # ===== TABEL JURNAL =====
    st.divider()
    st.subheader("Jurnal Umum")

    if not df.empty:
        st.dataframe(df, use_container_width=True)

        st.subheader("Edit / Hapus Transaksi")
        pilih = st.selectbox("Pilih Transaksi", df.index)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Hapus"):
                st.session_state.data.pop(pilih)
                st.experimental_rerun()

        with col2:
            if st.button("Edit"):
                st.session_state.edit_index = pilih

        if st.session_state.edit_index == pilih:
            row = df.loc[pilih]
            with st.form("form_edit"):
                tgl = st.date_input("Tanggal", row["Tanggal"])
                akun_baru = st.text_input("Akun", row["Akun"])
                posisi_baru = st.radio(
                    "Posisi",
                    ["Debit", "Kredit"],
                    index=0 if row["Posisi"] == "Debit" else 1
                )
                jumlah_baru = st.number_input("Jumlah", value=row["Jumlah"])

                update = st.form_submit_button("Update")
                if update:
                    st.session_state.data[pilih] = {
                        "Tanggal": tgl,
                        "Akun": akun_baru,
                        "Posisi": posisi_baru,
                        "Jumlah": jumlah_baru
                    }
                    st.session_state.edit_index = None
                    st.experimental_rerun()
    else:
        st.info("Belum ada transaksi")

# ===================== LIHAT SEMUA =====================
elif menu == "Lihat Semua":
    st.title("Semua Laporan")

    if df.empty:
        st.warning("Belum ada transaksi")
    else:
        df["Jenis Akun"] = df["Akun"].apply(jenis_akun)
        df["Debit"] = df.apply(lambda x: x["Jumlah"] if x["Posisi"] == "Debit" else 0, axis=1)
        df["Kredit"] = df.apply(lambda x: x["Jumlah"] if x["Posisi"] == "Kredit" else 0, axis=1)
        df["Saldo"] = df["Debit"] - df["Kredit"]

        st.subheader("Jurnal Umum")
        st.dataframe(df[["Tanggal", "Akun", "Posisi", "Jumlah"]], use_container_width=True)

        st.subheader("Buku Besar")
        buku_besar = df.groupby(["Jenis Akun", "Akun"])[["Debit", "Kredit", "Saldo"]].sum().reset_index()
        st.dataframe(buku_besar, use_container_width=True)

        st.subheader("Laba Rugi")
        pendapatan = df[(df["Jenis Akun"] == "Pendapatan") & (df["Posisi"] == "Kredit")]["Jumlah"].sum()
        beban = df[(df["Jenis Akun"] == "Beban") & (df["Posisi"] == "Debit")]["Jumlah"].sum()
        laba = pendapatan - beban

        col1, col2, col3 = st.columns(3)
        col1.metric("Pendapatan", rupiah(pendapatan))
        col2.metric("Beban", rupiah(beban))
        col3.metric("Laba Bersih", rupiah(laba))

        st.subheader("Neraca")
        neraca = df.groupby(["Jenis Akun", "Akun"])["Saldo"].sum().reset_index()

        col1, col2 = st.columns(2)
        col1.dataframe(neraca[neraca["Jenis Akun"] == "Aset"], use_container_width=True)
        col2.dataframe(
            neraca[neraca["Jenis Akun"].isin(["Kewajiban", "Ekuitas"])],
            use_container_width=True
        )

# ===================== BUKU BESAR =====================
elif menu == "Buku Besar":
    st.title("Buku Besar")
    if not df.empty:
        df["Jenis Akun"] = df["Akun"].apply(jenis_akun)
        df["Debit"] = df.apply(lambda x: x["Jumlah"] if x["Posisi"] == "Debit" else 0, axis=1)
        df["Kredit"] = df.apply(lambda x: x["Jumlah"] if x["Posisi"] == "Kredit" else 0, axis=1)
        st.dataframe(
            df.groupby(["Jenis Akun", "Akun"])[["Debit", "Kredit"]].sum().reset_index(),
            use_container_width=True
        )
    else:
        st.info("Belum ada transaksi")

# ===================== LABA RUGI =====================
elif menu == "Laba Rugi":
    st.title("Laporan Laba Rugi")
    if not df.empty:
        df["Jenis Akun"] = df["Akun"].apply(jenis_akun)
        pendapatan = df[(df["Jenis Akun"] == "Pendapatan") & (df["Posisi"] == "Kredit")]["Jumlah"].sum()
        beban = df[(df["Jenis Akun"] == "Beban") & (df["Posisi"] == "Debit")]["Jumlah"].sum()
        st.metric("Laba Bersih", rupiah(pendapatan - beban))
    else:
        st.info("Belum ada transaksi")

# ===================== NERACA =====================
elif menu == "Neraca":
    st.title("Neraca")
    if not df.empty:
        df["Jenis Akun"] = df["Akun"].apply(jenis_akun)
        df["Saldo"] = df.apply(lambda x: x["Jumlah"] if x["Posisi"] == "Debit" else -x["Jumlah"], axis=1)
        st.dataframe(
            df.groupby(["Jenis Akun", "Akun"])["Saldo"].sum().reset_index(),
            use_container_width=True
        )
    else:
        st.info("Belum ada transaksi")

# ===================== EXPORT EXCEL =====================
elif menu == "Export Excel":
    st.title("Export Excel")

    if df.empty:
        st.warning("Belum ada data")
    else:
        df["Jenis Akun"] = df["Akun"].apply(jenis_akun)
        df["Debit"] = df.apply(lambda x: x["Jumlah"] if x["Posisi"] == "Debit" else 0, axis=1)
        df["Kredit"] = df.apply(lambda x: x["Jumlah"] if x["Posisi"] == "Kredit" else 0, axis=1)
        df["Saldo"] = df["Debit"] - df["Kredit"]

        buku_besar = df.groupby(["Jenis Akun", "Akun"])[["Debit", "Kredit", "Saldo"]].sum().reset_index()
        neraca = df.groupby(["Jenis Akun", "Akun"])["Saldo"].sum().reset_index()

        laba_rugi = pd.DataFrame({
            "Keterangan": ["Pendapatan", "Beban", "Laba Bersih"],
            "Jumlah": [
                df[(df["Jenis Akun"] == "Pendapatan") & (df["Posisi"] == "Kredit")]["Jumlah"].sum(),
                df[(df["Jenis Akun"] == "Beban") & (df["Posisi"] == "Debit")]["Jumlah"].sum(),
                (df[(df["Jenis Akun"] == "Pendapatan") & (df["Posisi"] == "Kredit")]["Jumlah"].sum()
                 - df[(df["Jenis Akun"] == "Beban") & (df["Posisi"] == "Debit")]["Jumlah"].sum())
            ]
        })

        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df[["Tanggal", "Akun", "Posisi", "Jumlah"]].to_excel(writer, "Jurnal Umum", index=False)
            buku_besar.to_excel(writer, "Buku Besar", index=False)
            laba_rugi.to_excel(writer, "Laba Rugi", index=False)
            neraca.to_excel(writer, "Neraca", index=False)

        st.download_button(
            "Download Excel",
            data=output.getvalue(),
            file_name="laporan_akuntansi.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
