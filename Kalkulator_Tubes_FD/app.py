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

for kriteria in rubrik_penilaian:
    nama = kriteria['nama_kriteria']
    poin_opsi = kriteria['poin_tersedia']

    # Prepare options for st.selectbox
    options = []
    # Sort options by points in descending order for better readability
    sorted_poin_opsi = sorted(poin_opsi.items(), key=lambda item: item[0], reverse=True)
    for poin, deskripsi in sorted_poin_opsi:
        options.append(f"{poin} poin: {deskripsi}")

    # Streamlit selectbox for each criterion
    selected_option_str = st.selectbox(
        f"**{nama}**",
        options,
        key=f"selectbox_{nama}"
    )

    # Extract the numeric score from the selected string
    selected_poin = int(selected_option_str.split(' ')[0])
    selected_scores[nama] = selected_poin
    total_score += selected_poin

st.markdown("--- ")
st.success(f"## Total Poin: {total_score}")
