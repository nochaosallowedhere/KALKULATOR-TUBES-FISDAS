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

st.markdown("""
<style>

    /* =========================
       BACKGROUND
    ========================= */

    .stApp {
        background-color: #0b1f3a;
    }

    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* =========================
       SEMUA FONT PUTIH
       ========================= */

    .stApp,
    .stApp p,
    .stApp span,
    .stApp label,
    .stApp div {
        color: white;
    }


    /* =========================
       HERO
       ========================= */

    .hero-box {
        background: linear-gradient(135deg, #061426, #16345c);
        padding: 35px;
        border-radius: 25px;
        margin-bottom: 25px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.25);
    }

    .hero-title {
        color: white !important;
        font-size: 2.3rem;
        font-weight: 800;
        margin: 0;
    }

    .hero-subtitle {
        color: white !important;
        font-size: 1rem;
        margin-top: 8px;
    }


    /* =========================
       SECTION TITLE
       ========================= */

    .section-title {
        color: white !important;
        font-size: 1.5rem;
        font-weight: 800;
        margin-top: 25px;
        margin-bottom: 15px;
    }


    /* =========================
       JUDUL KRITERIA
       ========================= */

    .stMarkdown h3 {
        color: white !important;
        font-size: 1.35rem !important;
        font-weight: 800 !important;
        margin-top: 25px !important;
        margin-bottom: 12px !important;
    }


    /* =========================
       DESKRIPSI
       ========================= */

    .description-box {
        background: #16345c;
        border-left: 5px solid #60a5fa;
        border-radius: 10px;
        padding: 12px 15px;
        margin-bottom: 10px;
        color: white !important;
        line-height: 1.6;
    }

    .description-box * {
        color: white !important;
    }

    .point-label {
        font-weight: 800;
        color: white !important;
    }


    /* =========================
       SELECTBOX
       ========================= */

    div[data-baseweb="select"] > div {
        background-color: #16345c !important;
        color: white !important;
        border: 1px solid #60a5fa;
    }

    div[data-baseweb="select"] span {
        color: white !important;
    }

    div[data-baseweb="select"] svg {
        fill: white !important;
    }


    /* =========================
       SCORE BOX
       ========================= */

    .score-box {
        background: #16345c;
        border-radius: 22px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.20);
        border: 1px solid #60a5fa;
        margin-bottom: 30px;
    }

    .score-title {
        color: white !important;
        font-size: 0.9rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .score-value {
        color: white !important;
        font-size: 3rem;
        font-weight: 900;
        margin-top: 5px;
    }


    /* =========================
       REKAP
       ========================= */

    .stMarkdown strong {
        color: white !important;
    }


    /* =========================
       DIVIDER
       ========================= */

    hr {
        border-color: #315477 !important;
    }


    /* =========================
       CAPTION
       ========================= */

    .stCaption,
    [data-testid="stCaptionContainer"] {
        color: white !important;
    }


    /* =========================
       MOBILE
       ========================= */

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
        <div class="hero-title">📋 Kalkulator Tubes FISDAS</div>
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

st.markdown(
    """
    <div style="
        color: white;
        font-size: 1.35rem;
        font-weight: 800;
        margin-top: 25px;
        margin-bottom: 12px;
    ">
        BAB I
    </div>
    """,
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
        <div class="score-title">TOTAL SCORE</div>
        <div class="score-value">{total_score} poin</div>
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
    "THE REAL ASSISTANT"
)
