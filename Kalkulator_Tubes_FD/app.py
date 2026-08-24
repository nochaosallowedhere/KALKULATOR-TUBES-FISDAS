import streamlit as st
from rubric_data import rubrik_penilaian

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Kalkulator Tubes Fisdas",
    page_icon="📋",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* Background */
    .stApp {
        background-color: #f5f7fb;
    }

    /* Main container */
    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* Hero */
    .hero-box {
        background: linear-gradient(135deg, #111827, #374151);
        padding: 35px;
        border-radius: 25px;
        margin-bottom: 25px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.15);
    }

    .hero-title {
        color: white;
        font-size: 2.3rem;
        font-weight: 800;
        margin: 0;
    }

    .hero-subtitle {
        color: #d1d5db;
        font-size: 1rem;
        margin-top: 8px;
    }

    /* Score */
    .score-box {
        background: white;
        border-radius: 22px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        border: 1px solid #e5e7eb;
        margin-bottom: 30px;
    }

    .score-title {
        color: #6b7280;
        font-size: 0.9rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .score-value {
        color: #111827;
        font-size: 3rem;
        font-weight: 900;
        margin-top: 5px;
    }

    /* Section title */
    .section-title {
        color: #111827;
        font-size: 1.5rem;
        font-weight: 800;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    /* Description box */
    .description-box {
        background: #f8fafc;
        border-left: 5px solid #374151;
        border-radius: 10px;
        padding: 12px 15px;
        margin-bottom: 10px;
        color: #374151;
        line-height: 1.6;
    }

    .point-label {
        font-weight: 800;
        color: #111827;
    }

    /* Mobile */
    @media (max-width: 768px) {

        .block-container {
            padding: 1rem;
        }

        .hero-box {
            padding: 22px;
            border-radius: 18px;
        }

        .hero-title {
            font-size: 1.7rem;
        }

        .score-value {
            font-size: 2.4rem;
        }

    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="hero-box">
        <div class="hero-title">📋 Rubric Scoreboard</div>
        <div class="hero-subtitle">
            Kalkulator Rubrik Penilaian Tugas Besar
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# INITIAL DATA
# =========================================================

total_score = 0
selected_scores = {}

max_score = 0

for kriteria in rubrik_penilaian:

    poin_opsi = kriteria["poin_tersedia"]

    if poin_opsi:
        max_score += max(poin_opsi.keys())


# =========================================================
# PENILAIAN
# =========================================================

st.markdown(
    '<div class="section-title">📝 Penilaian Rubrik</div>',
    unsafe_allow_html=True
)


for i, kriteria in enumerate(rubrik_penilaian):

    nama = kriteria["nama_kriteria"]
    poin_opsi = kriteria["poin_tersedia"]

    # Urutkan poin
    sorted_poin_opsi = sorted(
        poin_opsi.items(),
        key=lambda item: item[0],
        reverse=True
    )

    # -----------------------------------------
    # NAMA KRITERIA
    # -----------------------------------------

    st.markdown(f"### 📌 {nama}")

    # -----------------------------------------
    # DESKRIPSI
    # -----------------------------------------

    st.markdown("**Deskripsi Kriteria:**")

    for poin, deskripsi in sorted_poin_opsi:

        st.markdown(
            f"""
            <div class="description-box">
                <span class="point-label">{poin} poin</span><br>
                {deskripsi}
            </div>
            """,
            unsafe_allow_html=True
        )

    # -----------------------------------------
    # PILIH SKOR
    # -----------------------------------------

    pilihan_poin = [
        poin for poin, deskripsi in sorted_poin_opsi
    ]

    pilihan = st.selectbox(
        "🎯 Pilih skor:",
        pilihan_poin,
        format_func=lambda x: f"{x} poin",
        key=f"selectbox_{i}"
    )

    selected_scores[nama] = pilihan
    total_score += pilihan

    st.divider()


# =========================================================
# TOTAL SCORE
# =========================================================

percentage = 0

if max_score > 0:
    percentage = total_score / max_score


st.markdown(
    '<div class="section-title">🏆 Hasil Penilaian</div>',
    unsafe_allow_html=True
)


# Gunakan komponen Streamlit, bukan HTML
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "TOTAL SKOR",
        f"{total_score} / {max_score}"
    )

with col2:
    st.metric(
        "PERSENTASE",
        f"{percentage * 100:.1f}%"
    )

with col3:
    if percentage >= 0.8:
        status = "Sangat Baik"
    elif percentage >= 0.6:
        status = "Baik"
    elif percentage >= 0.4:
        status = "Cukup"
    else:
        status = "Perlu Perbaikan"

    st.metric(
        "STATUS",
        status
    )


# Progress
st.progress(
    min(percentage, 1.0)
)

st.caption(
    f"Progress penilaian: {percentage * 100:.1f}%"
)


# =========================================================
# REKAP
# =========================================================

st.markdown(
    '<div class="section-title">📊 Rekap Penilaian</div>',
    unsafe_allow_html=True
)

for nama, skor in selected_scores.items():

    st.write(
        f"**{nama}** — {skor} poin"
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "📋 Rubric Scoreboard • Kalkulator Penilaian Tugas Besar"
)
