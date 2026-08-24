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
        background-color: #0b1f3a;
    }

    /* Main container */
    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* Hero */
    .hero-box {
        background: linear-gradient(135deg, #061426, #16345c);
        padding: 35px;
        border-radius: 25px;
        margin-bottom: 25px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.25);
    }

    .hero-title {
        color: white;
        font-size: 2.3rem;
        font-weight: 800;
        margin: 0;
    }

    .hero-subtitle {
        color: #cbd5e1;
        font-size: 1rem;
        margin-top: 8px;
    }

    /* Score */
    .score-box {
        background: white;
        border-radius: 22px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        border: 1px solid #dbeafe;
        margin-bottom: 30px;
    }

    .score-title {
        color: #475569;
        font-size: 0.9rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .score-value {
        color: #0b1f3a;
        font-size: 3rem;
        font-weight: 900;
        margin-top: 5px;
    }

    /* Section title */
    .section-title {
        color: white;
        font-size: 1.5rem;
        font-weight: 800;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    /* Judul kriteria */
    .stMarkdown h3 {
        color: white !important;
        font-size: 1.35rem !important;
        font-weight: 800 !important;
        margin-top: 25px !important;
        margin-bottom: 12px !important;
    }

    /* Label */
    .stMarkdown p {
        color: #e2e8f0;
    }

    .description-title {
        color: #e2e8f0 !important;
        font-weight: 700;
    }

    /* Description box */
    .description-box {
        background: #f8fafc;
        border-left: 5px solid #2563eb;
        border-radius: 10px;
        padding: 12px 15px;
        margin-bottom: 10px;
        color: #374151;
        line-height: 1.6;
    }

    .point-label {
        font-weight: 800;
        color: #0b1f3a;
    }

    /* Selectbox */
    div[data-baseweb="select"] > div {
        background-color: white;
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

    st.markdown(
    f"""
    <div style="
        font-size: 1.4rem;
        font-weight: 800;
        color: #111827;
        margin-top: 25px;
        margin-bottom: 12px;
    ">
        📌 {nama}
    </div>
    """,
    unsafe_allow_html=True
)

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

st.markdown(
    '<div class="section-title">🏆 Total Score</div>',
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="score-box">
        <div class="score-title">
            TOTAL SKOR
        </div>
        <div class="score-value">
            {total_score} poin
        </div>
    </div>
    """,
    unsafe_allow_html=True
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
