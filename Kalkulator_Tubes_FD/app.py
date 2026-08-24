import streamlit as st
from rubric_data import rubrik_penilaian

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Rubric Scoreboard",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* ==============================
       GLOBAL
    ============================== */

    .stApp {
        background: #f6f7fb;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* ==============================
       HEADER
       ============================== */

    .hero {
        padding: 2rem 2.2rem;
        border-radius: 24px;
        background: linear-gradient(
            135deg,
            #111827 0%,
            #1f2937 50%,
            #374151 100%
        );
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 12px 30px rgba(0,0,0,0.12);
    }

    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
    }

    .hero-subtitle {
        font-size: 1rem;
        opacity: 0.75;
    }

    /* ==============================
       SCORE CARD
       ============================== */

    .score-card {
        background: white;
        border-radius: 22px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid #e5e7eb;
        box-shadow: 0 8px 24px rgba(0,0,0,0.06);
        text-align: center;
    }

    .score-label {
        font-size: 0.9rem;
        color: #6b7280;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .score-number {
        font-size: 3rem;
        font-weight: 900;
        color: #111827;
        margin: 0.2rem 0;
    }

    .score-max {
        font-size: 1rem;
        color: #9ca3af;
    }

    /* ==============================
       SECTION
       ============================== */

    .section-title {
        font-size: 1.5rem;
        font-weight: 800;
        color: #111827;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }

    /* ==============================
       RUBRIC CARD
       ============================== */

    .rubric-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 6px 20px rgba(0,0,0,0.05);
    }

    .rubric-title {
        font-size: 1.2rem;
        font-weight: 800;
        color: #111827;
        margin-bottom: 1rem;
    }

    .description-title {
        font-size: 0.85rem;
        font-weight: 700;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 0.7rem;
    }

    .description-item {
        background: #f9fafb;
        border-left: 4px solid #374151;
        border-radius: 10px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
        color: #374151;
        line-height: 1.55;
    }

    .point-badge {
        font-weight: 800;
        color: #111827;
    }

    /* ==============================
       RECAP
       ============================== */

    .recap-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.7rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    }

    .recap-name {
        font-weight: 700;
        color: #374151;
    }

    .recap-score {
        font-weight: 900;
        color: #111827;
    }

    /* ==============================
       MOBILE
       ============================== */

    @media (max-width: 768px) {

        .block-container {
            padding: 1rem;
        }

        .hero {
            padding: 1.4rem;
            border-radius: 18px;
        }

        .hero-title {
            font-size: 1.6rem;
        }

        .score-number {
            font-size: 2.4rem;
        }

        .rubric-card {
            padding: 1rem;
            border-radius: 16px;
        }

    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="hero">
    <div class="hero-title">
        📋 Rubric Scoreboard
    </div>
    <div class="hero-subtitle">
        Kalkulator Rubrik Penilaian Tugas Besar
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# INITIALIZATION
# =========================================================

total_score = 0
selected_scores = {}

# =========================================================
# CALCULATE MAX SCORE
# =========================================================

max_score = 0

for kriteria in rubrik_penilaian:
    poin_opsi = kriteria["poin_tersedia"]

    if poin_opsi:
        max_score += max(poin_opsi.keys())


# =========================================================
# SCORE DISPLAY
# =========================================================

score_placeholder = st.empty()


# =========================================================
# RUBRIC SECTION
# =========================================================

st.markdown(
    '<div class="section-title">📝 Penilaian Rubrik</div>',
    unsafe_allow_html=True
)


for i, kriteria in enumerate(rubrik_penilaian):

    nama = kriteria["nama_kriteria"]
    poin_opsi = kriteria["poin_tersedia"]

    # Sort points descending
    sorted_poin_opsi = sorted(
        poin_opsi.items(),
        key=lambda item: item[0],
        reverse=True
    )

    # -----------------------------------------
    # CARD START
    # -----------------------------------------

    st.markdown(
        f"""
        <div class="rubric-card">

            <div class="rubric-title">
                📌 {nama}
            </div>

            <div class="description-title">
                Deskripsi Kriteria
            </div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------
    # DESCRIPTION
    # -----------------------------------------

    for poin, deskripsi in sorted_poin_opsi:

        st.markdown(
            f"""
            <div class="description-item">
                <span class="point-badge">{poin} poin</span><br>
                {deskripsi}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------------------
    # SCORE SELECTOR
    # -----------------------------------------

    pilihan_poin = [
        poin for poin, deskripsi in sorted_poin_opsi
    ]

    pilihan = st.selectbox(
        "🎯 Pilih skor",
        pilihan_poin,
        format_func=lambda x: f"{x} poin",
        key=f"selectbox_{i}"
    )

    selected_scores[nama] = pilihan
    total_score += pilihan

    st.markdown("")


# =========================================================
# FINAL SCORE
# =========================================================

percentage = 0

if max_score > 0:
    percentage = (total_score / max_score) * 100


score_placeholder.markdown(
    f"""
    <div class="score-card">

        <div class="score-label">
            Total Skor
        </div>

        <div class="score-number">
            {total_score}
            <span class="score-max">/ {max_score}</span>
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# PROGRESS BAR
# =========================================================

st.progress(
    min(total_score / max_score, 1.0) if max_score > 0 else 0
)

st.caption(
    f"Progress penilaian: **{percentage:.1f}%**"
)


# =========================================================
# RECAP
# =========================================================

st.markdown(
    '<div class="section-title">📊 Rekap Penilaian</div>',
    unsafe_allow_html=True
)


for nama, skor in selected_scores.items():

    st.markdown(
        f"""
        <div class="recap-card">

            <span class="recap-name">
                {nama}
            </span>

            <span style="float:right;" class="recap-score">
                {skor} poin
            </span>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "Rubric Scoreboard • Kalkulator Penilaian Tugas Besar"
)
