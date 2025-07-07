import streamlit as st
import asyncio
from server.shop import getproduct

st.set_page_config(
    page_title="Shop Assist 🛒",
    page_icon="🛒",
    layout="centered",
)

# ---------- Custom CSS for dark mode, glassmorphism, and professional look ----------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, .stApp {
        background: #181c24 !important;
        color: #e6e6e6 !important;
        font-family: 'Inter', 'Segoe UI', 'Roboto', Arial, sans-serif;
    }
    .card {
        background: rgba(30, 34, 44, 0.95);
        border-radius: 18px;
        box-shadow: 0 8px 32px 0 rgba(0,0,0,0.25);
        padding: 0;
        margin: 2.5rem auto 2rem auto;
        width: 80vw;
        max-width: 900px;
        backdrop-filter: blur(6px);
        border: 1.5px solid rgba(80,80,120,0.18);
    }
    .card-header {
        background: linear-gradient(90deg, #232a3a 60%, #2d3a5a 100%);
        color: #fff;
        border-radius: 18px 18px 0 0;
        padding: 1.5rem 2rem 1.2rem 2rem;
        font-size: 2.1rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        letter-spacing: 0.01em;
        border-bottom: 1px solid #232a3a;
    }
    .card-header .icon {
        font-size: 2.2rem;
        margin-right: 0.7rem;
        filter: drop-shadow(0 2px 8px #2d3a5a);
    }
    .card-body {
        padding: 2rem 2rem 1.5rem 2rem;
    }
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stTextArea>div>textarea {
        background: #232a3a !important;
        color: #e6e6e6 !important;
        border-radius: 8px !important;
        border: 1.5px solid #2d3a5a !important;
        font-size: 1.08rem;
    }
    .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus, .stTextArea>div>textarea:focus {
        border: 1.5px solid #7b61ff !important;
        outline: none !important;
    }
    div.stButton > button {
        background: linear-gradient(90deg, #7b61ff 0%, #4f8cff 100%);
        color: #fff;
        border-radius: 8px;
        padding: 0.85em 2.2em;
        font-weight: 600;
        font-size: 1.1rem;
        border: none;
        margin-top: 1.2em;
        box-shadow: 0 2px 12px 0 rgba(162,89,255,0.10);
        transition: background 0.2s, transform 0.2s;
    }
    div.stButton > button:hover {
        background: linear-gradient(90deg, #4f8cff 0%, #7b61ff 100%);
        transform: scale(1.04);
    }
    .stTextInput, .stNumberInput, .stTextArea {
        border-radius: 8px !important;
    }
    .result-header {
        background: linear-gradient(90deg, #1e824c 60%, #27ae60 100%);
        color: #fff;
        border-radius: 18px 18px 0 0;
        padding: 1.2rem 2rem 1rem 2rem;
        font-size: 1.3rem;
        font-weight: 600;
        letter-spacing: 0.01em;
        border-bottom: 1px solid #1e824c;
        display: flex;
        align-items: center;
    }
    .result-header .icon {
        font-size: 1.5rem;
        margin-right: 0.6rem;
    }
    pre {
        background: #232a3a !important;
        color: #e6e6e6 !important;
        padding: 1rem;
        border-radius: 8px;
        font-size: 1.05rem;
    }
    /* Remove Streamlit's main menu and footer for a clean look */
    #MainMenu, footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ---------- Card with header and form ----------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown(
    '<div class="card-header"><span class="icon">🛒</span>Shop Assist</div>',
    unsafe_allow_html=True
)
st.markdown('<div class="card-body">', unsafe_allow_html=True)

with st.form("shop_assist_form"):
    prod = st.text_input("Product Name", placeholder="e.g., Wireless Earbuds")
    minp = st.number_input("Min Price", min_value=1.0, value=1.0)
    maxp = st.number_input("Max Price", min_value=1.0, value=9999999.0)
    specific_features = st.text_area(
        "Specific Features",
        placeholder="e.g., Noise cancellation, waterproof..."
    )
    submitted = st.form_submit_button("🔍 Search")

st.markdown('</div>', unsafe_allow_html=True)  # Close card-body
st.markdown('</div>', unsafe_allow_html=True)  # Close card

# ---------- Result Card ----------
if submitted:
    st.markdown('<div class="card" style="margin-top:2rem;">', unsafe_allow_html=True)
    st.markdown('<div class="result-header"><span class="icon">📦</span>Product Listings</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-body">', unsafe_allow_html=True)
    with st.spinner("Fetching product listings..."):
        result = asyncio.run(getproduct(prod, specific_features, minp, maxp))
    st.code(result)
    st.markdown('</div>', unsafe_allow_html=True)  # Close card-body
    st.markdown('</div>', unsafe_allow_html=True)  # Close card 