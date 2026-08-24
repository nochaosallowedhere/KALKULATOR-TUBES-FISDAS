import streamlit as st
from rubric_data import rubrik_penilaian

st.set_page_config(
    page_title="Kalkulator Rubrik Penilaian",
    layout="wide"
)

st.title("Kalkulator Rubrik Penilaian Tugas Besar")

total_score = 0
selected_scores = {}

st.subheader("Pilih Poin untuk Setiap Kriteria:")

for i, kriteria in enumerate(rubrik_penilaian):

    nama = kriteria['nama_kriteria']
    poin_opsi = kriteria['poin_tersedia']

    # Judul kriteria
    st.markdown(f"### {nama}")

    # Urutkan poin dari terbesar ke terkecil
    sorted_poin_opsi = sorted(
        poin_opsi.items(),
        key=lambda item: item[0],
        reverse=True
    )

    # Tampilkan seluruh deskripsi terlebih dahulu
    st.markdown("**Deskripsi:**")

    for poin, deskripsi in sorted_poin_opsi:
        st.markdown(
            f"**{poin} poin:** {deskripsi}"
        )

    # Dropdown pilihan poin
    pilihan_poin = [poin for poin, deskripsi in sorted_poin_opsi]

    pilihan = st.selectbox(
        "Pilih poin:",
        pilihan_poin,
        format_func=lambda x: f"{x} poin",
        key=f"selectbox_{i}"
    )

    # Simpan nilai
    selected_scores[nama] = pilihan
    total_score += pilihan

st.markdown("---")
st.success(f"## Total Poin: {total_score}")
