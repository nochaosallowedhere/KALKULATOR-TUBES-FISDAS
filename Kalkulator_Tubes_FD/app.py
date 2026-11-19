import base64
import mimetypes
from pathlib import Path
import streamlit as st
from rubric_data import rubrik_penilaian, rubrik_tp_ta

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Kalkulator Tubes Fisdas",
    page_icon="🧮",
    layout="wide"
)

# =========================================================
# KONFIGURASI WATERMARK OTOMATIS DARI SERVER
# =========================================================

WATERMARK_CANDIDATES = [
    "watermark.png",
    "watermark.jpg",
    "watermark.jpeg",
    "watermark.webp",
]
WATERMARK_OPACITY = 0.10   # Atur transparansi watermark (0.03 - 0.35)
WATERMARK_SIZE = 260       # Ukuran pola watermark dalam px


def load_server_watermark() -> tuple[bytes, str] | None:
    """Membaca file watermark langsung dari folder server."""
    base_dir = Path(__file__).resolve().parent
    for filename in WATERMARK_CANDIDATES:
        path = base_dir / filename
        if path.exists() and path.is_file():
            mime = mimetypes.guess_type(path.name)[0] or "image/png"
            return path.read_bytes(), mime
    return None


def parse_persentase_int(raw_value: str) -> int | None:
    """Validasi input harus berupa integer dari 0 sampai 100."""
    cleaned = raw_value.strip()
    if cleaned.endswith("%"):
        cleaned = cleaned[:-1].strip()
    if not cleaned:
        return None
    if not cleaned.isdigit():
        return None
    val = int(cleaned)
    if 0 <= val <= 100:
        return val
    return None


watermark_data_uri = ""
server_wm = load_server_watermark()
if server_wm is not None:
    raw_bytes, mime_type = server_wm
    b64_img = base64.b64encode(raw_bytes).decode("utf-8")
    watermark_data_uri = f"data:{mime_type};base64,{b64_img}"

watermark_css = ""
if watermark_data_uri:
    watermark_css = f"""
    .watermark-overlay {{
        position: fixed;
        inset: 0;
        background-image: url("{watermark_data_uri}");
        background-repeat: repeat;
        background-size: {WATERMARK_SIZE}px auto;
        opacity: {WATERMARK_OPACITY};
        pointer-events: none;
        z-index: 0;
    }}

    .stApp > div:first-child {{
        position: relative;
        z-index: 1;
    }}
    """

st.markdown(f"""
<style>

    /* =========================
       BACKGROUND & WATERMARK
    ========================= */

    .stApp {{
        background-color: #0b1f3a;
    }}

    {watermark_css}

    .block-container {{
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 4rem;
        position: relative;
        z-index: 1;
    }}


    /* =========================
       SEMUA FONT PUTIH
    ========================= */

    .stApp,
    .stApp p,
    .stApp span,
    .stApp label,
    .stApp div {{
        color: white;
    }}


    /* =========================
       HERO
    ========================= */

    .hero-box {{
        background: linear-gradient(135deg, #061426, #16345c);
        padding: 35px;
        border-radius: 25px;
        margin-bottom: 25px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.25);
    }}

    .hero-title {{
        color: white !important;
        font-size: 2.3rem;
        font-weight: 800;
        margin: 0;
    }}

    .hero-subtitle {{
        color: white !important;
        font-size: 1rem;
        margin-top: 8px;
    }}


    /* =========================
       SECTION TITLE
    ========================= */

    .section-title {{
        color: white !important;
        font-size: 1.5rem;
        font-weight: 800;
        margin-top: 25px;
        margin-bottom: 15px;
    }}


    /* =========================
       JUDUL KRITERIA
    ========================= */

    .stMarkdown h3 {{
        color: white !important;
        font-size: 1.35rem !important;
        font-weight: 800 !important;
        margin-top: 25px !important;
        margin-bottom: 12px !important;
    }}


    /* =========================
       DESKRIPSI
    ========================= */

    .description-box {{
        background: #16345c;
        border-left: 5px solid #60a5fa;
        border-radius: 10px;
        padding: 12px 15px;
        margin-bottom: 10px;
        color: white !important;
        line-height: 1.6;
    }}

    .description-box * {{
        color: white !important;
    }}

    .point-label {{
        font-weight: 800;
        color: white !important;
    }}


    /* =========================
       SELECTBOX & TEXT INPUT
    ========================= */

    div[data-baseweb="select"] > div {{
        background-color: #16345c !important;
        color: white !important;
        border: 1px solid #60a5fa;
    }}

    div[data-baseweb="select"] span {{
        color: white !important;
    }}

    div[data-baseweb="select"] svg {{
        fill: white !important;
    }}

    div[data-baseweb="input"] > div {{
        background-color: #16345c !important;
        color: white !important;
        border: 1px solid #60a5fa;
    }}

    div[data-baseweb="input"] input {{
        color: white !important;
    }}


    /* =========================
       SCORE BOX
    ========================= */

    .score-box {{
        background: #16345c;
        border-radius: 22px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.20);
        border: 1px solid #60a5fa;
        margin-bottom: 20px;
    }}

    .score-title {{
        color: white !important;
        font-size: 0.9rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    .score-value {{
        color: white !important;
        font-size: 3rem;
        font-weight: 900;
        margin-top: 5px;
    }}


    /* =========================
       REKAP
    ========================= */

    .stMarkdown strong {{
        color: white !important;
    }}


    /* =========================
       DIVIDER
    ========================= */

    hr {{
        border-color: #315477 !important;
    }}


    /* =========================
       CAPTION
    ========================= */

    .stCaption,
    [data-testid="stCaptionContainer"] {{
        color: white !important;
    }}


    /* =========================
       MOBILE
    ========================= */

    @media (max-width: 768px) {{

        .block-container {{
            padding: 1rem;
        }}

        .hero-box {{
            padding: 22px;
            border-radius: 18px;
        }}

        .hero-title {{
            font-size: 1.7rem;
        }}

        .score-value {{
            font-size: 2.4rem;
        }}

    }}

</style>
""", unsafe_allow_html=True)

if watermark_data_uri:
    st.markdown('<div class="watermark-overlay"></div>', unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="hero-box">
        <div class="hero-title">🧮 Kalkulator Tubes FISDAS</div>
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
# PENILAIAN TP TA (SEBELUM BAB 1)
# =========================================================

st.markdown(
    '<div class="section-title">📋 Penilaian Rubrik</div>',
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div style="
        color: white;
        font-size: 1.35rem;
        font-weight: 800;
        margin-top: 15px;
        margin-bottom: 8px;
    ">
        {rubrik_tp_ta["nama_kriteria"]} — {rubrik_tp_ta["keterangan"]}
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="description-box">
        <span class="point-label">Indeks Kelengkapan Tubes (Total Indeks = 100)</span><br>
        • Indeks 50 jika laporan terpenuhi<br>
        • Indeks 30 jika membawa maket/prototype<br>
        • Indeks 20 jika membuat PPT
    </div>
    """,
    unsafe_allow_html=True
)

tp_ta_score = 0
tp_ta_checked = []

for komp in rubrik_tp_ta["komponen"]:
    is_checked = st.checkbox(
        f"{komp['label']} (Indeks {komp['poin']})",
        key=f"tp_ta_{komp['id']}"
    )
    if is_checked:
        tp_ta_score += komp["poin"]
        tp_ta_checked.append(f"{komp['label']} [{komp['poin']}]")

st.info(
    f"Skor **{rubrik_tp_ta['nama_kriteria']}**: **{tp_ta_score} / 100**"
    + (f" ({', '.join(tp_ta_checked)})" if tp_ta_checked else "")
)

selected_scores[rubrik_tp_ta["nama_kriteria"]] = tp_ta_score
total_score += tp_ta_score

st.divider()

# =========================================================
# PENILAIAN BAB 1 DST.
# =========================================================

for i, kriteria in enumerate(rubrik_penilaian):

    nama = kriteria["nama_kriteria"]
    poin_opsi = kriteria["poin_tersedia"]

    # -----------------------------------------
    # JUDUL KRITERIA
    # -----------------------------------------

    st.markdown(
        f"""
        <div style="
            color: white;
            font-size: 1.35rem;
            font-weight: 800;
            margin-top: 25px;
            margin-bottom: 12px;
        ">
            {nama}
        </div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------
    # URUTKAN POIN
    # -----------------------------------------

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
# INPUT PERSENTASE (0 - 100%)
# =========================================================

st.markdown(
    '<div class="section-title">📈 Persentase Value (0 - 100%)</div>',
    unsafe_allow_html=True
)

raw_persen = st.text_input(
    "Masukkan nilai persentase (bilangan bulat 0 - 100%):",
    placeholder="Contoh: 85",
    key="persentase_input"
)

persentase_valid: int |
