"""Premium CSS styling for Streamlit interface.

Inspired by Apple, Vercel, Linear, and Stripe design languages.
"""

PREMIUM_CSS = """
<style>
    /* Global Reset & Typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Typography */
    h1 {
        font-weight: 700 !important;
        font-size: 2rem !important;
        color: #111827 !important;
        letter-spacing: -0.025em !important;
    }
    
    h2 {
        font-weight: 600 !important;
        font-size: 1.5rem !important;
        color: #1f2937 !important;
        letter-spacing: -0.025em !important;
        margin-top: 2rem !important;
    }
    
    h3 {
        font-weight: 600 !important;
        font-size: 1.125rem !important;
        color: #374151 !important;
    }
    
    p, li {
        color: #4b5563 !important;
        line-height: 1.6 !important;
    }
    
    /* Cards */
    .stCard {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease;
    }
    
    .stCard:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        transform: translateY(-1px);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #111827 !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        color: #6b7280 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: #111827 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.625rem 1.25rem !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1) !important;
    }
    
    .stButton > button:hover {
        background: #374151 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Secondary button */
    .stButton > button[kind="secondary"] {
        background: white !important;
        color: #374151 !important;
        border: 1px solid #e5e7eb !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: #f9fafb !important;
        border-color: #d1d5db !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #f9fafb !important;
        border-right: 1px solid #e5e7eb !important;
    }
    
    [data-testid="stSidebar"] .sidebar-content {
        padding: 2rem 1.5rem !important;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: white;
        border: 2px dashed #d1d5db;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        transition: all 0.2s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #6366f1;
        background: #f5f3ff;
    }
    
    /* DataFrames */
    .stDataFrame {
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: #f3f4f6;
        border-radius: 8px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        color: #6b7280;
    }
    
    .stTabs [aria-selected="true"] {
        background: white !important;
        color: #111827 !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Alerts */
    .stAlert {
        border-radius: 8px !important;
        border: none !important;
        padding: 1rem 1.25rem !important;
    }
    
    .stAlert [data-testid="stMarkdownContainer"] {
        color: inherit !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        font-weight: 600 !important;
        color: #374151 !important;
        background: #f9fafb !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
        border: 1px solid #e5e7eb !important;
    }
    
    /* Selectbox & Inputs */
    .stSelectbox > div > div,
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        border-radius: 8px !important;
        border: 1px solid #e5e7eb !important;
        font-size: 0.875rem !important;
    }
    
    .stSelectbox > div > div:focus-within,
    .stTextInput > div > div > input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f3f4f6;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #d1d5db;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #9ca3af;
    }
    
    /* Custom divider */
    .premium-divider {
        height: 1px;
        background: linear-gradient(to right, transparent, #e5e7eb, transparent);
        margin: 2rem 0;
    }
    
    /* Loading animation */
    @keyframes pulse-soft {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    
    .loading-pulse {
        animation: pulse-soft 1.5s ease-in-out infinite;
    }
</style>
"""


def inject_custom_css() -> None:
    """Inject premium CSS into Streamlit app."""
    import streamlit as st
    st.markdown(PREMIUM_CSS, unsafe_allow_html=True)
