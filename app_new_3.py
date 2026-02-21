import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
from datetime import datetime
import numpy as np

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Towards the Vision - SLS Australia", 
    layout="wide", 
    page_icon="🇸🇦",
    initial_sidebar_state="expanded"
)

# ============================================================================
# INITIATIVE & SESSION CONFIGURATION
# ============================================================================

INITIATIVES = {
    "Towards the Vision": {
        "name": "Towards the Vision",
        "icon": "🎯",
        "description": "Educational initiative empowering participants with knowledge and skills aligned with Vision 2030 goals",
        "color": "#006341",
        "sessions": {
            "Cybersecurity": {
                "name": "🔐 Cybersecurity Session",
                "data_file": "sls_kpi_data_cybersecurity_updated1.json",
                "icon": "🔐",
                "vision_theme": "Digital Transformation & Innovation",
                "color": "#667eea",
                "topic_labels": ["Cybersecurity Knowledge", "Vision 2030 Contribution", "Technical Skills in Demand"]
            },
            "Finance": {
                "name": "💰 Finance Session",
                "data_file": "sls_kpi_finance_session2_ttv_data_updated1.json",
                "icon": "💰",
                "vision_theme": "Financial Sector Development",
                "color": "#f093fb",
                "topic_labels": ["Finance Knowledge", "Vision 2030 Contribution", "Technical Skills in Demand"]
            }
        }
    },
    "Misk Tracks": {
        "name": "Misk Tracks",
        "icon": "🚀",
        "description": "Leadership development programs designed to cultivate future leaders and innovators",
        "color": "#8B5CF6",
        "sessions": {
            "Awareness Study": {
                "name": "📊 Misk Tracks Awareness",
                "data_file": "misk_tracks_awareness_session.json",
                "icon": "📊",
                "vision_theme": "Baseline Awareness Assessment",
                "color": "#10b981",
                "topic_labels": [],
                "type": "awareness"  # Special type for awareness dashboard
            },
            "10x Leaders": {
                "name": "⭐ 10x Leaders Program",
                "data_file": "sls_kpi_10xleaders_session_data_updated_overall.json",
                "icon": "⭐",
                "vision_theme": "Leadership Development & Excellence",
                "color": "#f59e0b",
                "topic_labels": [],
                "type": "comprehensive"  # New comprehensive awareness analysis
            }
        }
    }
}

# ============================================================================
# STUNNING SLS BRAND CSS - SAUDI-INSPIRED
# ============================================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600;700&family=Epilogue:wght@300;400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Epilogue', sans-serif;
    }
    
    /* Animated Background with Saudi Pattern */
    .main {
        background: 
            linear-gradient(135deg, rgba(0, 132, 61, 0.03) 0%, rgba(147, 193, 63, 0.03) 100%),
            repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(0, 99, 65, 0.01) 10px, rgba(0, 99, 65, 0.01) 20px);
        animation: bgShift 20s ease-in-out infinite;
    }
    
    @keyframes bgShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* Stunning Animated Header */
    .sls-header {
        background: 
            linear-gradient(135deg, #006341 0%, #00843d 50%, #93c13f 100%);
        padding: 4rem 2rem;
        border-radius: 0 0 40px 40px;
        box-shadow: 
            0 20px 60px rgba(0, 100, 65, 0.2),
            inset 0 -1px 0 rgba(255, 255, 255, 0.2);
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
        animation: headerGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes headerGlow {
        from { box-shadow: 0 20px 60px rgba(0, 100, 65, 0.2), inset 0 -1px 0 rgba(255, 255, 255, 0.2); }
        to { box-shadow: 0 25px 70px rgba(0, 100, 65, 0.3), inset 0 -1px 0 rgba(255, 255, 255, 0.3); }
    }
    
    /* Geometric Islamic Pattern Overlay */
    .sls-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 600px;
        height: 600px;
        background: 
            radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%),
            repeating-linear-gradient(45deg, transparent, transparent 20px, rgba(255,255,255,0.05) 20px, rgba(255,255,255,0.05) 40px);
        border-radius: 50%;
        animation: rotate 30s linear infinite;
    }
    
    .sls-header::after {
        content: '';
        position: absolute;
        bottom: -30%;
        left: -5%;
        width: 500px;
        height: 500px;
        background: radial-gradient(circle, rgba(147,193,63,0.25) 0%, transparent 70%);
        border-radius: 50%;
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.25; }
        50% { transform: scale(1.1); opacity: 0.35; }
    }
    
    .initiative-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 4rem;
        font-weight: 700;
        color: white;
        text-align: center;
        margin: 0;
        position: relative;
        z-index: 1;
        text-shadow: 0 4px 20px rgba(0,0,0,0.2);
        animation: titleFloat 3s ease-in-out infinite;
    }
    
    @keyframes titleFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }
    
    .initiative-subtitle {
        font-family: 'Epilogue', sans-serif;
        font-size: 1.4rem;
        font-weight: 300;
        color: rgba(255,255,255,0.95);
        text-align: center;
        margin-top: 0.75rem;
        position: relative;
        z-index: 1;
        letter-spacing: 0.08em;
    }
    
    .mission-tagline {
        font-family: 'Epilogue', sans-serif;
        font-size: 1.15rem;
        font-weight: 600;
        color: rgba(255,255,255,0.95);
        text-align: center;
        margin-top: 1.75rem;
        padding: 1.25rem 2.5rem;
        background: rgba(255,255,255,0.18);
        border-radius: 60px;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255,255,255,0.3);
        display: inline-block;
        position: relative;
        z-index: 1;
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
        animation: taglineGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes taglineGlow {
        from { box-shadow: 0 8px 30px rgba(0,0,0,0.15); }
        to { box-shadow: 0 12px 40px rgba(147,193,63,0.3); }
    }
    
    /* Section Headers with Accent */
    .section-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a1a;
        margin: 3.5rem 0 2rem 0;
        padding-bottom: 1.25rem;
        position: relative;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 120px;
        height: 4px;
        background: linear-gradient(90deg, #006341, #93c13f);
        border-radius: 2px;
        animation: underlineGrow 1s ease-out;
    }
    
    @keyframes underlineGrow {
        from { width: 0; }
        to { width: 120px; }
    }
    
    .subsection-title {
        font-family: 'Epilogue', sans-serif;
        font-size: 0.95rem;
        font-weight: 800;
        color: #00843d;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin: 2.5rem 0 1.5rem 0;
        opacity: 0;
        animation: fadeInUp 0.6s ease-out forwards;
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Stunning KPI Cards with Depth */
    .kpi-card {
        background: 
            linear-gradient(135deg, #ffffff 0%, #f8fdf9 100%);
        padding: 2.5rem;
        border-radius: 24px;
        box-shadow: 
            0 10px 40px rgba(0, 100, 65, 0.08),
            inset 0 1px 0 rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(0, 132, 61, 0.08);
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        position: relative;
        overflow: hidden;
        opacity: 0;
        animation: cardSlideIn 0.8s ease-out forwards;
    }
    
    @keyframes cardSlideIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 5px;
        height: 100%;
        background: linear-gradient(180deg, #006341 0%, #93c13f 100%);
        box-shadow: 0 0 20px rgba(0, 99, 65, 0.3);
    }
    
    .kpi-card::after {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(147,193,63,0.05) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.5s;
    }
    
    .kpi-card:hover {
        transform: translateY(-12px) scale(1.02);
        box-shadow: 
            0 20px 60px rgba(0, 132, 61, 0.18),
            inset 0 1px 0 rgba(255, 255, 255, 1);
    }
    
    .kpi-card:hover::after {
        opacity: 1;
    }
    
    .kpi-category {
        font-family: 'Epilogue', sans-serif;
        font-size: 0.7rem;
        font-weight: 900;
        color: #00843d;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        margin-bottom: 0.75rem;
        opacity: 0.8;
    }
    
    .kpi-label {
        font-family: 'Epilogue', sans-serif;
        font-size: 1.15rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1.25rem;
        line-height: 1.4;
    }
    
    .kpi-value {
        font-family: 'Cormorant Garamond', serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #006341 0%, #00843d 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1;
        margin: 1rem 0;
        position: relative;
    }
    
    .kpi-context {
        font-family: 'Epilogue', sans-serif;
        font-size: 0.95rem;
        color: #5a6c7d;
        margin-top: 1rem;
        line-height: 1.6;
    }
    
    .kpi-trend {
        font-family: 'Epilogue', sans-serif;
        font-size: 0.85rem;
        font-weight: 700;
        color: #00843d;
        margin-top: 0.75rem;
        padding: 0.5rem 1rem;
        background: rgba(0, 132, 61, 0.08);
        border-radius: 20px;
        display: inline-block;
    }
    
    /* Gorgeous Highlight Box */
    .highlight-box {
        background: linear-gradient(135deg, #006341 0%, #00843d 100%);
        padding: 3rem;
        border-radius: 30px;
        margin: 3rem 0;
        box-shadow: 
            0 20px 60px rgba(0, 100, 65, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
        animation: boxFloat 6s ease-in-out infinite;
    }
    
    @keyframes boxFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }
    
    .highlight-box::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 500px;
        height: 500px;
        background: radial-gradient(circle, rgba(147,193,63,0.25) 0%, transparent 70%);
        border-radius: 50%;
        animation: pulseGlow 5s ease-in-out infinite;
    }
    
    @keyframes pulseGlow {
        0%, 100% { opacity: 0.25; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(1.15); }
    }
    
    .highlight-box h3 {
        font-family: 'Cormorant Garamond', serif;
        font-size: 2rem;
        font-weight: 700;
        color: white;
        margin-bottom: 2rem;
        position: relative;
        z-index: 1;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .highlight-box ul {
        list-style: none;
        padding: 0;
        margin: 0;
        position: relative;
        z-index: 1;
    }
    
    .highlight-box li {
        font-family: 'Epilogue', sans-serif;
        font-size: 1.15rem;
        color: rgba(255,255,255,0.95);
        line-height: 2;
        padding: 0.75rem 0;
        padding-left: 2.5rem;
        position: relative;
        animation: listItemSlide 0.6s ease-out forwards;
        opacity: 0;
    }
    
    .highlight-box li:nth-child(1) { animation-delay: 0.1s; }
    .highlight-box li:nth-child(2) { animation-delay: 0.2s; }
    .highlight-box li:nth-child(3) { animation-delay: 0.3s; }
    .highlight-box li:nth-child(4) { animation-delay: 0.4s; }
    
    @keyframes listItemSlide {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .highlight-box li:before {
        content: "✓";
        position: absolute;
        left: 0;
        color: #93c13f;
        font-weight: 900;
        font-size: 1.5rem;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    /* Elegant Info Box */
    .info-box {
        background: 
            linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(248,253,249,0.9) 100%);
        backdrop-filter: blur(20px);
        padding: 3rem;
        border-radius: 28px;
        border: 2px solid rgba(0, 100, 65, 0.1);
        box-shadow: 0 15px 50px rgba(0, 100, 65, 0.08);
        margin: 2.5rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .info-box::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(135deg, #006341, #93c13f);
        border-radius: 28px;
        z-index: -1;
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .info-box:hover::before {
        opacity: 0.1;
    }
    
    .info-box h3 {
        font-family: 'Cormorant Garamond', serif;
        font-size: 2rem;
        color: #1a1a1a;
        margin-bottom: 1.5rem;
    }
    
    .info-box p {
        font-family: 'Epilogue', sans-serif;
        font-size: 1.1rem;
        line-height: 1.9;
        color: #495057;
    }
    
    /* Beautiful Session Cards */
    .session-card {
        background: white;
        padding: 3.5rem 2.5rem;
        border-radius: 28px;
        text-align: center;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.08);
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        border: 2px solid transparent;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .session-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(0, 99, 65, 0.03), rgba(147, 193, 63, 0.03));
        opacity: 0;
        transition: opacity 0.5s;
    }
    
    .session-card:hover {
        transform: translateY(-15px) scale(1.03);
        box-shadow: 0 25px 60px rgba(0, 132, 61, 0.2);
        border-color: #00843d;
    }
    
    .session-card:hover::before {
        opacity: 1;
    }
    
    .session-icon {
        font-size: 5rem;
        margin-bottom: 1.75rem;
        filter: drop-shadow(0 8px 16px rgba(0,0,0,0.1));
        transition: transform 0.5s;
    }
    
    .session-card:hover .session-icon {
        transform: scale(1.1) rotate(5deg);
    }
    
    .session-name {
        font-family: 'Cormorant Garamond', serif;
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 1rem;
    }
    
    .session-theme {
        font-family: 'Epilogue', sans-serif;
        font-size: 1.05rem;
        color: #666;
        font-weight: 500;
        line-height: 1.6;
    }
    
    /* Gorgeous Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.75rem;
        background: white;
        padding: 1.25rem;
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(0, 100, 65, 0.08);
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Epilogue', sans-serif;
        font-size: 1.05rem;
        font-weight: 700;
        padding: 1rem 2rem;
        border-radius: 14px;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background: linear-gradient(135deg, #006341 0%, #00843d 100%);
        color: white;
        box-shadow: 0 6px 20px rgba(0, 100, 65, 0.35);
        transform: translateY(-2px);
    }
    
    /* Stunning Footer */
    .sls-footer {
        background: linear-gradient(135deg, #1a1a1a 0%, #2c3e50 100%);
        color: white;
        padding: 4rem 2rem;
        border-radius: 40px 40px 0 0;
        margin-top: 5rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .sls-footer::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -25%;
        width: 150%;
        height: 200%;
        background: radial-gradient(circle, rgba(0, 132, 61, 0.1) 0%, transparent 70%);
        animation: footerPulse 8s ease-in-out infinite;
    }
    
    @keyframes footerPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    .sls-footer h2 {
        font-family: 'Cormorant Garamond', serif;
        font-size: 2.5rem;
        margin-bottom: 0.75rem;
        position: relative;
        z-index: 1;
    }
    
    .sls-footer .tagline {
        font-family: 'Epilogue', sans-serif;
        font-size: 1.4rem;
        font-weight: 300;
        opacity: 0.95;
        margin-bottom: 2.5rem;
        position: relative;
        z-index: 1;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_kpi_card(category, label, value, context, trend=""):
    trend_html = f'<div class="kpi-trend">{trend}</div>' if trend else ''
    return f"""
    <div class="kpi-card">
        <div class="kpi-category">{category}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-context">{context}</div>
        {trend_html}
    </div>
    """

# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_data
def load_data(data_file):
    try:
        with open(data_file, 'r') as f:
            return json.load(f)
    except:
        st.error(f"⚠️ Data file '{data_file}' not found!")
        return None

# ============================================================================
# SESSION MANAGEMENT
# ============================================================================

if 'selected_initiative' not in st.session_state:
    st.session_state.selected_initiative = None

if 'selected_session' not in st.session_state:
    st.session_state.selected_session = None

# ============================================================================
# INITIATIVE SELECTION SCREEN
# ============================================================================

if st.session_state.selected_initiative is None:
    try:
        st.image("sls_image.jpg", use_column_width=True)
    except:
        pass
    
    st.markdown("""
    <div class="sls-header">
        <h1 class="initiative-title">Saudi Leadership Society</h1>
        <p class="initiative-subtitle">Australia Chapter</p>
        <div style="text-align: center; margin-top: 1.5rem;">
            <span class="mission-tagline">Grow • Connect • Impact</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h3>Our Initiatives</h3>
        <p>
            The Saudi Leadership Society Australia Chapter runs multiple initiatives to empower 
            Saudi students and professionals with knowledge, skills, and connections aligned with 
            <strong>Vision 2030</strong> goals.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="section-title">🌟 Select an Initiative</p>', unsafe_allow_html=True)
    
    cols = st.columns(len(INITIATIVES))
    
    for idx, (initiative_key, initiative_info) in enumerate(INITIATIVES.items()):
        with cols[idx]:
            if st.button(
                f"{initiative_info['icon']} {initiative_key}",
                key=f"btn_init_{initiative_key}",
                use_container_width=True,
                type="primary"
            ):
                st.session_state.selected_initiative = initiative_key
                st.rerun()
            
            st.markdown(f"""
            <div class="session-card">
                <div class="session-icon">{initiative_info['icon']}</div>
                <div class="session-name">{initiative_key}</div>
                <p class="session-theme">{initiative_info['description']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.stop()

# ============================================================================
# SESSION SELECTION SCREEN (within selected initiative)
# ============================================================================

if st.session_state.selected_session is None:
    initiative_key = st.session_state.selected_initiative
    initiative_info = INITIATIVES[initiative_key]
    
    try:
        st.image("sls_image.jpg", use_column_width=True)
    except:
        pass
    
    st.markdown(f"""
    <div class="sls-header">
        <h1 class="initiative-title">{initiative_info['icon']} {initiative_key}</h1>
        <p class="initiative-subtitle">{initiative_info['description']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("← Back to Initiatives", type="secondary"):
        st.session_state.selected_initiative = None
        st.rerun()
    
    st.markdown('<p class="section-title">📚 Select a Session</p>', unsafe_allow_html=True)
    
    sessions = initiative_info['sessions']
    cols = st.columns(min(len(sessions), 3))  # Max 3 columns
    
    for idx, (session_key, session_info) in enumerate(sessions.items()):
        col_idx = idx % 3
        with cols[col_idx]:
            if st.button(
                f"{session_info['icon']} {session_key}",
                key=f"btn_{session_key}",
                use_container_width=True,
                type="primary"
            ):
                st.session_state.selected_session = session_key
                st.rerun()
            
            st.markdown(f"""
            <div class="session-card">
                <div class="session-icon">{session_info['icon']}</div>
                <div class="session-name">{session_key}</div>
                <p class="session-theme">{session_info['vision_theme']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.stop()

# ============================================================================
# LOAD SELECTED SESSION
# ============================================================================

selected_initiative = st.session_state.selected_initiative
selected_session = st.session_state.selected_session

initiative_info = INITIATIVES[selected_initiative]
session_info = initiative_info['sessions'][selected_session]

try:
    st.image("sls_image.jpg", use_column_width=True)
except:
    pass

st.markdown(f"""
<div class="sls-header">
    <h1 class="initiative-title">{session_info["icon"]} {selected_session}</h1>
    <p class="initiative-subtitle">{initiative_info['name']} • {session_info['vision_theme']}</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 5])
with col1:
    if st.button("← Back", type="secondary"):
        st.session_state.selected_session = None
        st.rerun()

data = load_data(session_info['data_file'])

if data is None:
    st.error(f"Could not load data.")
    st.stop()

# Check if this is an awareness dashboard
if session_info.get('type') == 'awareness':
    # ========================================================================
    # MISK TRACKS AWARENESS DASHBOARD
    # ========================================================================
    
    metrics = data['metrics']
    viz_data = data['visualization_data']
    
    st.markdown('<p class="section-title">📊 Awareness Impact</p>', unsafe_allow_html=True)
    
    # Big stats - Before and After
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-category">BEFORE SESSION</div>
            <div class="kpi-label">Awareness Level</div>
            <div class="kpi-value">{metrics['awareness_summary']['aware_pre_pct']:.1f}%</div>
            <div class="kpi-context">Participants aware of Misk Tracks</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-category">AFTER SESSION</div>
            <div class="kpi-label">Awareness Level</div>
            <div class="kpi-value">{metrics['awareness_summary']['aware_post_pct']:.1f}%</div>
            <div class="kpi-context">Participants aware of Misk Tracks</div>
            <div class="kpi-trend">✓ {metrics['awareness_summary']['awareness_increase_pct_points']:.1f} percentage point increase</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-category">SURVEY REACH</div>
            <div class="kpi-label">Participants Surveyed</div>
            <div class="kpi-value">{metrics['total_responses']}</div>
            <div class="kpi-context">Completed both pre and post surveys</div>
            <div class="kpi-trend">✓ {metrics['match_rate_pct']:.1f}% match rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Highlight box
    st.markdown(f"""
    <div class="highlight-box">
        <h3>✨ Key Finding</h3>
        <ul>
            <li>Awareness increased by {metrics['awareness_summary']['awareness_increase_pct_points']:.1f} percentage points</li>
            <li>{metrics['awareness_summary']['aware_post_pct']:.0f}% of participants are now aware of Misk Tracks</li>
            <li>From {metrics['awareness_summary']['aware_pre_pct']:.1f}% to {metrics['awareness_summary']['aware_post_pct']:.0f}% awareness</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed breakdown
    st.markdown('<p class="section-title">📈 Awareness Breakdown</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Before Session")
        
        pre_dist = metrics['awareness_distribution']['pre']
        labels_pre = list(pre_dist.keys())
        values_pre = list(pre_dist.values())
        
        colors_map = {
            'Very Aware': '#006341',
            'Somewhat Aware': '#93c13f',
            'Heard the name only': '#fbbf24',
            'Not aware at all': '#e74c3c'
        }
        colors_pre = [colors_map.get(label, '#666') for label in labels_pre]
        
        fig_pre = go.Figure(data=[go.Pie(
            labels=labels_pre,
            values=values_pre,
            marker_colors=colors_pre,
            textfont=dict(size=14, family='Epilogue'),
            hole=0.4
        )])
        
        fig_pre.update_layout(
            height=400,
            showlegend=True,
            annotations=[dict(
                text=f"<b>{metrics['awareness_summary']['aware_pre_pct']:.1f}%</b><br>Aware",
                x=0.5, y=0.5,
                font=dict(size=20, family='Cormorant Garamond'),
                showarrow=False
            )],
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
        )
        
        st.plotly_chart(fig_pre, use_container_width=True)
    
    with col2:
        st.markdown("### After Session")
        
        post_dist = metrics['awareness_distribution']['post']
        labels_post = list(post_dist.keys())
        values_post = list(post_dist.values())
        colors_post = [colors_map.get(label, '#666') for label in labels_post]
        
        fig_post = go.Figure(data=[go.Pie(
            labels=labels_post,
            values=values_post,
            marker_colors=colors_post,
            textfont=dict(size=14, family='Epilogue'),
            hole=0.4
        )])
        
        fig_post.update_layout(
            height=400,
            showlegend=True,
            annotations=[dict(
                text=f"<b>{metrics['awareness_summary']['aware_post_pct']:.0f}%</b><br>Aware",
                x=0.5, y=0.5,
                font=dict(size=20, family='Cormorant Garamond'),
                showarrow=False
            )],
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
        )
        
        st.plotly_chart(fig_post, use_container_width=True)
    
    # Comparison chart
    st.markdown('<p class="section-title">🔄 Before vs After Comparison</p>', unsafe_allow_html=True)
    
    levels = viz_data['awareness_comparison']['levels']
    pre_scores = viz_data['awareness_comparison']['pre']
    post_scores = viz_data['awareness_comparison']['post']
    
    fig_compare = go.Figure()
    
    fig_compare.add_trace(go.Bar(
        name='Before Session',
        x=levels,
        y=pre_scores,
        marker_color='#e9ecef',
        text=[f"{s:.1f}%" for s in pre_scores],
        textposition='outside'
    ))
    
    fig_compare.add_trace(go.Bar(
        name='After Session',
        x=levels,
        y=post_scores,
        marker_color='#006341',
        text=[f"{s:.1f}%" for s in post_scores],
        textposition='outside'
    ))
    
    fig_compare.update_layout(
        barmode='group',
        yaxis_title='Percentage of Participants',
        yaxis=dict(range=[0, 80]),
        height=450,
        font=dict(family="Epilogue", color="#2c3e50"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    
    st.plotly_chart(fig_compare, use_container_width=True)
    
    # Info box about the study
    st.markdown("""
    <div class="info-box">
        <h3>📋 About This Study</h3>
        <p>
            This baseline awareness assessment was conducted to understand participants' 
            familiarity with <strong>Misk Tracks</strong> before and after the session. 
            This one-time study helps us measure the impact of our awareness initiatives 
            and plan future Misk Tracks sessions effectively.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown(f"""
    <div class='sls-footer'>
        <h2>Misk Tracks Awareness Study</h2>
        <p class="tagline">Baseline Assessment • Australia Chapter</p>
        <div style='display: flex; justify-content: center; gap: 3rem; margin: 2rem 0; flex-wrap: wrap; position: relative; z-index: 1;'>
            <div>
                <div style='font-size: 2.5rem; font-weight: 700;'>{metrics['total_responses']}</div>
                <div style='opacity: 0.8;'>Participants</div>
            </div>
            <div>
                <div style='font-size: 2.5rem; font-weight: 700;'>+{metrics['awareness_summary']['awareness_increase_pct_points']:.1f}%</div>
                <div style='opacity: 0.8;'>Awareness Increase</div>
            </div>
            <div>
                <div style='font-size: 2.5rem; font-weight: 700;'>{metrics['awareness_summary']['aware_post_pct']:.0f}%</div>
                <div style='opacity: 0.8;'>Now Aware</div>
            </div>
        </div>
        <p style='font-size: 1.1rem; margin-top: 2rem; opacity: 0.9; position: relative; z-index: 1;'>
            <strong>Building Awareness • Growing Impact</strong>
        </p>
        <p style='font-size: 0.9rem; opacity: 0.7; margin-top: 1rem; position: relative; z-index: 1;'>
            {datetime.now().strftime('%B %d, %Y')} | Misk Tracks
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.stop()  # Don't render the standard dashboard below

# Check if this is a hybrid dashboard (10x Leaders style - awareness + satisfaction)
if session_info.get('type') == 'hybrid':
    # ========================================================================
    # HYBRID DASHBOARD (10x Leaders)
    # ========================================================================
    
    metrics = data['metrics']
    chapter_metrics = metrics.get('chapter_metrics', {})
    
    REGISTERED = chapter_metrics.get('total_registered', 0)
    TARGET = chapter_metrics.get('target_attendance', 50)
    ACTUAL_ATTENDEES = chapter_metrics.get('actual_attendees', 0)
    
    st.markdown('<p class="section-title">📊 Key Performance Indicators</p>', unsafe_allow_html=True)
    
    # ROW 1: REACH & ENGAGEMENT
    st.markdown('<p class="subsection-title">Reach & Participation</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        attendance_rate = (ACTUAL_ATTENDEES / REGISTERED * 100) if REGISTERED > 0 else 0
        st.markdown(
            create_kpi_card(
                "REACH",
                "Total Participants",
                f"{ACTUAL_ATTENDEES}",
                f"Out of {REGISTERED} registered",
                f"✓ {attendance_rate:.0f}% attendance rate"
            ),
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            create_kpi_card(
                "ENGAGEMENT",
                "Completed Both Surveys",
                f"{metrics['total_responses']}",
                f"Out of {ACTUAL_ATTENDEES} participants",
                f"✓ {metrics['match_rate_pct']:.1f}% completion rate"
            ),
            unsafe_allow_html=True
        )
    
    with col3:
        target_performance = (ACTUAL_ATTENDEES / TARGET * 100) if TARGET > 0 else 0
        st.markdown(
            create_kpi_card(
                "TARGET",
                "Goal Achievement",
                f"{target_performance:.0f}%",
                f"Target was {TARGET} participants",
                f"✓ Exceeded target" if ACTUAL_ATTENDEES > TARGET else "→ Approaching target"
            ),
            unsafe_allow_html=True
        )
    
    # ROW 2: AWARENESS IMPACT
    st.markdown('<p class="subsection-title">Program Awareness</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            create_kpi_card(
                "BEFORE",
                "Initial Awareness",
                f"{metrics['awareness_summary']['aware_pre_pct']:.1f}%",
                "Knew about 10x Leaders program",
                ""
            ),
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            create_kpi_card(
                "AFTER",
                "Final Awareness",
                f"{metrics['awareness_summary']['aware_post_pct']:.1f}%",
                "Now understand 10x Leaders",
                f"✓ +{metrics['awareness_summary']['awareness_increase_pct_points']:.1f} point increase"
            ),
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            create_kpi_card(
                "GROWTH",
                "Awareness Increase",
                f"+{metrics['awareness_summary']['awareness_increase_pct_points']:.1f}%",
                "Percentage point improvement",
                "✓ Excellent impact"
            ),
            unsafe_allow_html=True
        )
    
    # ROW 3: ACTION & SATISFACTION
    st.markdown('<p class="subsection-title">Engagement & Satisfaction</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        action_pct = metrics.get('connect_members_planning_action_pct', 0)
        action_count = metrics.get('connect_total_planning_action', 0)
        st.markdown(
            create_kpi_card(
                "COMMITMENT",
                "Plan to Take Action",
                f"{action_pct:.0f}%",
                f"{action_count} participants committed",
                f"✓ Outstanding" if action_pct >= 80 else "✓ Strong" if action_pct >= 60 else "→ Growing"
            ),
            unsafe_allow_html=True
        )
    
    with col2:
        satisfaction = metrics.get('impact_avg_satisfaction', 0)
        st.markdown(
            create_kpi_card(
                "QUALITY",
                "Satisfaction Score",
                f"{satisfaction:.2f}/5.0",
                "Average participant rating",
                f"✓ Excellent" if satisfaction >= 4.5 else "✓ Very good" if satisfaction >= 4.0 else "→ Good"
            ),
            unsafe_allow_html=True
        )
    
    with col3:
        satisfied_pct = metrics.get('impact_satisfaction_pct', 0)
        st.markdown(
            create_kpi_card(
                "SATISFACTION",
                "Highly Satisfied",
                f"{satisfied_pct:.0f}%",
                "Rated 4+ stars",
                f"✓ Perfect score" if satisfied_pct >= 95 else "✓ Strong approval"
            ),
            unsafe_allow_html=True
        )
    
    # Highlights
    achievements = []
    if metrics['awareness_summary']['awareness_increase_pct_points'] >= 50:
        achievements.append(f"Massive {metrics['awareness_summary']['awareness_increase_pct_points']:.1f}% awareness increase")
    if satisfaction >= 4.5:
        achievements.append(f"Outstanding {satisfaction:.2f}/5.0 satisfaction rating")
    if ACTUAL_ATTENDEES > TARGET:
        achievements.append(f"Exceeded attendance target by {((ACTUAL_ATTENDEES-TARGET)/TARGET*100):.0f}%")
    if action_pct >= 75:
        achievements.append(f"{action_pct:.0f}% of participants committed to taking action")
    
    if achievements:
        st.markdown(f"""
        <div class="highlight-box">
            <h3>✨ Session Highlights</h3>
            <ul>
                {''.join([f'<li>{achievement}</li>' for achievement in achievements])}
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Demographics
    st.markdown('<p class="section-title">👥 Participant Demographics</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Locations")
        location_data = metrics.get('demographics_location', {})
        
        if location_data:
            fig_loc = go.Figure(data=[go.Pie(
                labels=list(location_data.keys()),
                values=list(location_data.values()),
                hole=0.4,
                marker_colors=['#006341', '#00843d', '#93c13f', '#b8d96d', '#d4e89e', '#e9f5c9']
            )])
            
            fig_loc.update_layout(
                height=400,
                showlegend=True,
                paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02)
            )
            
            st.plotly_chart(fig_loc, use_container_width=True)
    
    with col2:
        st.markdown("### How They Heard About Us")
        heard_data = metrics.get('demographics_heard_about', {})
        
        if heard_data:
            labels = list(heard_data.keys())
            values = list(heard_data.values())
            
            fig_heard = go.Figure(data=[go.Bar(
                x=labels,
                y=values,
                marker_color='#006341',
                text=values,
                textposition='outside'
            )])
            
            fig_heard.update_layout(
                height=400,
                yaxis_title='Number of Participants',
                font=dict(family="Epilogue", color="#2c3e50"),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            
            st.plotly_chart(fig_heard, use_container_width=True)
    
    # Satisfaction Distribution
    st.markdown('<p class="section-title">⭐ Participant Satisfaction</p>', unsafe_allow_html=True)
    
    sat_dist = metrics.get('impact_satisfaction_distribution', {})
    if sat_dist:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            labels = [f"{k} Stars" for k in sat_dist.keys()]
            values = list(sat_dist.values())
            colors = ['#93c13f' if int(k) >= 4 else '#f39c12' for k in sat_dist.keys()]
            
            fig_sat = go.Figure(data=[go.Bar(
                x=labels,
                y=values,
                marker_color=colors,
                text=values,
                textposition='outside',
                textfont=dict(size=16)
            )])
            
            fig_sat.update_layout(
                height=350,
                yaxis_title='Number of Participants',
                font=dict(family="Epilogue", color="#2c3e50"),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            
            st.plotly_chart(fig_sat, use_container_width=True)
        
        with col2:
            st.markdown("### Summary")
            st.metric("Average Rating", f"{satisfaction:.2f}/5.0")
            st.metric("Highly Satisfied", f"{satisfied_pct:.0f}%")
            st.metric("Total Responses", metrics['total_responses'])
    
    # Footer
    st.markdown(f"""
    <div class='sls-footer'>
        <h2>10x Leaders Program</h2>
        <p class="tagline">Misk Tracks • Australia Chapter</p>
        <div style='display: flex; justify-content: center; gap: 3rem; margin: 2rem 0; flex-wrap: wrap; position: relative; z-index: 1;'>
            <div>
                <div style='font-size: 2.5rem; font-weight: 700;'>{ACTUAL_ATTENDEES}</div>
                <div style='opacity: 0.8;'>Participants</div>
            </div>
            <div>
                <div style='font-size: 2.5rem; font-weight: 700;'>+{metrics['awareness_summary']['awareness_increase_pct_points']:.1f}%</div>
                <div style='opacity: 0.8;'>Awareness Growth</div>
            </div>
            <div>
                <div style='font-size: 2.5rem; font-weight: 700;'>{satisfaction:.2f}/5</div>
                <div style='opacity: 0.8;'>Satisfaction</div>
            </div>
        </div>
        <p style='font-size: 1.1rem; margin-top: 2rem; opacity: 0.9; position: relative; z-index: 1;'>
            <strong>Grow • Connect • Impact</strong>
        </p>
        <p style='font-size: 0.9rem; opacity: 0.7; margin-top: 1rem; position: relative; z-index: 1;'>
            {datetime.now().strftime('%B %d, %Y')} | 10x Leaders
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.stop()  # Don't render the standard dashboard below

# ============================================================================
# COMPREHENSIVE DASHBOARD (10x Leaders with Overall/Paired Analysis)
# ============================================================================

if session_info.get('type') == 'comprehensive':
    metrics = data['metrics']
    
    # Extract nested structures
    response_summary = metrics.get('response_summary', {})
    awareness_analysis = metrics.get('awareness_analysis', {})
    satisfaction = metrics.get('satisfaction', {})
    action_plan = metrics.get('action_plan', {})
    demographics = metrics.get('demographics', {})
    chapter_metrics = metrics.get('chapter_metrics', {})
    
    REGISTERED = chapter_metrics.get('total_registered', 0)
    TARGET = chapter_metrics.get('target_attendance', 50)
    ACTUAL_ATTENDEES = chapter_metrics.get('actual_attendees', 0)
    TOTAL_PRE = response_summary.get('total_pre_responses', 0)
    TOTAL_POST = response_summary.get('total_post_responses', 0)
    MATCHED = response_summary.get('completed_both_surveys', 0)
    
    st.markdown('<p class="section-title">📊 Key Performance Indicators</p>', unsafe_allow_html=True)
    
    # ROW 1: REACH & ENGAGEMENT
    st.markdown('<p class="subsection-title">Reach & Participation</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        attendance_rate = (ACTUAL_ATTENDEES / REGISTERED * 100) if REGISTERED > 0 else 0
        st.markdown(
            create_kpi_card(
                "REACH",
                "Total Participants",
                f"{ACTUAL_ATTENDEES}",
                f"Out of {REGISTERED} registered",
                f"✓ {attendance_rate:.0f}% attendance rate"
            ),
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            create_kpi_card(
                "ENGAGEMENT",
                "Survey Participation",
                f"{TOTAL_PRE} → {TOTAL_POST}",
                f"{MATCHED} completed both surveys",
                f"✓ {response_summary.get('match_rate_vs_pre_pct', 0):.1f}% completion rate"
            ),
            unsafe_allow_html=True
        )
    
    with col3:
        target_performance = (ACTUAL_ATTENDEES / TARGET * 100) if TARGET > 0 else 0
        total_hours = chapter_metrics.get('total_participant_hours', 0)
        st.markdown(
            create_kpi_card(
                "IMPACT",
                "Engagement Hours",
                f"{total_hours}",
                f"Total participant hours ({chapter_metrics.get('session_duration_hours', 0)}h session)",
                f"✓ Exceeded target by {target_performance - 100:.0f}%" if target_performance > 100 else ""
            ),
            unsafe_allow_html=True
        )
    
    # ROW 2: AWARENESS IMPACT (OVERALL)
    st.markdown('<p class="subsection-title">Overall Awareness Impact</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            create_kpi_card(
                "BEFORE",
                "Baseline Awareness",
                f"{awareness_analysis.get('overall_pre_pct', 0):.1f}%",
                f"Out of {TOTAL_PRE} pre-survey respondents",
                ""
            ),
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            create_kpi_card(
                "AFTER",
                "Post-Session Awareness",
                f"{awareness_analysis.get('overall_post_pct', 0):.1f}%",
                f"Out of {TOTAL_POST} post-survey respondents",
                f"✓ +{awareness_analysis.get('overall_increase_pct_points', 0):.1f} points"
            ),
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            create_kpi_card(
                "GROWTH",
                "Awareness Increase",
                f"+{awareness_analysis.get('overall_increase_pct_points', 0):.1f}%",
                "Percentage point improvement",
                "✓ Massive impact!"
            ),
            unsafe_allow_html=True
        )
    
    # ROW 3: PAIRED AWARENESS ANALYSIS
    st.markdown('<p class="subsection-title">Paired Awareness Analysis (Same Participants)</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            create_kpi_card(
                "PAIRED PRE",
                "Before (Matched)",
                f"{awareness_analysis.get('paired_pre_pct', 0):.1f}%",
                f"{MATCHED} participants who completed both",
                ""
            ),
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            create_kpi_card(
                "PAIRED POST",
                "After (Matched)",
                f"{awareness_analysis.get('paired_post_pct', 0):.1f}%",
                f"Same {MATCHED} participants",
                f"✓ +{awareness_analysis.get('paired_increase_pct_points', 0):.1f} points"
            ),
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            create_kpi_card(
                "PAIRED GROWTH",
                "Individual Growth",
                f"+{awareness_analysis.get('paired_increase_pct_points', 0):.1f}%",
                "True within-person change",
                "✓ Validated impact!"
            ),
            unsafe_allow_html=True
        )
    
    # ROW 4: ACTION & SATISFACTION
    st.markdown('<p class="subsection-title">Action & Satisfaction</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            create_kpi_card(
                "COMMITMENT",
                "Plan to Take Action",
                f"{action_plan.get('planning_action_pct', 0):.0f}%",
                f"{action_plan.get('total_planning_action', 0)} participants committed",
                "✓ Strong commitment"
            ),
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            create_kpi_card(
                "QUALITY",
                "Satisfaction Score",
                f"{satisfaction.get('average_score', 0):.2f}/5.0",
                "Average participant rating",
                "✓ Outstanding!"
            ),
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            create_kpi_card(
                "SATISFACTION",
                "Highly Satisfied",
                f"{satisfaction.get('satisfied_pct', 0):.0f}%",
                "Rated 4+ stars",
                "✓ Perfect score!"
            ),
            unsafe_allow_html=True
        )
    
    # HIGHLIGHTS
    achievements = []
    overall_increase = awareness_analysis.get('overall_increase_pct_points', 0)
    paired_increase = awareness_analysis.get('paired_increase_pct_points', 0)
    
    if overall_increase >= 80:
        achievements.append(f"Massive {overall_increase:.1f} percentage point awareness increase (overall)")
    if paired_increase >= 80:
        achievements.append(f"True individual growth: {paired_increase:.1f} points for matched participants")
    if satisfaction.get('average_score', 0) >= 4.5:
        achievements.append(f"Outstanding satisfaction: {satisfaction.get('average_score', 0):.2f}/5.0")
    if action_plan.get('planning_action_pct', 0) >= 75:
        achievements.append(f"{action_plan.get('planning_action_pct', 0):.0f}% committed to taking action")
    if target_performance > 100:
        achievements.append(f"Exceeded attendance target by {target_performance - 100:.0f}%")
    
    if achievements:
        st.markdown(f"""
        <div class="highlight-box">
            <h3>✨ Session Highlights</h3>
            <ul>
                {''.join([f'<li>{achievement}</li>' for achievement in achievements])}
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # METHODOLOGY EXPLANATION
    st.markdown('<p class="section-title">📊 Analysis Methodology</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-box">
            <h3>Overall Analysis</h3>
            <p style="font-size: 1.05rem; line-height: 1.8;">
            Compares <strong>all pre-survey respondents</strong> ({pre}) with 
            <strong>all post-survey respondents</strong> ({post}). 
            Shows the <span class="highlight">population-level change</span> in awareness.
            </p>
            <p style="font-size: 1.05rem; line-height: 1.8; margin-top: 1rem;">
            <strong>Result:</strong> {before:.1f}% → {after:.1f}% 
            (<span class="highlight">+{increase:.1f} points</span>)
            </p>
        </div>
        """.format(
            pre=TOTAL_PRE,
            post=TOTAL_POST,
            before=awareness_analysis.get('overall_pre_pct', 0),
            after=awareness_analysis.get('overall_post_pct', 0),
            increase=overall_increase
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h3>Paired Analysis</h3>
            <p style="font-size: 1.05rem; line-height: 1.8;">
            Analyzes only the <strong>{matched} participants who completed both surveys</strong>. 
            Shows <span class="highlight">true within-person change</span> by comparing 
            the same individuals before and after.
            </p>
            <p style="font-size: 1.05rem; line-height: 1.8; margin-top: 1rem;">
            <strong>Result:</strong> {before:.1f}% → {after:.1f}% 
            (<span class="highlight">+{increase:.1f} points</span>)
            </p>
        </div>
        """.format(
            matched=MATCHED,
            before=awareness_analysis.get('paired_pre_pct', 0),
            after=awareness_analysis.get('paired_post_pct', 0),
            increase=paired_increase
        ), unsafe_allow_html=True)
    
    # AWARENESS COMPARISON VISUALIZATION
    st.markdown('<p class="section-title">📈 Awareness Growth Comparison</p>', unsafe_allow_html=True)
    
    fig_awareness = go.Figure()
    
    categories = ['Overall (All Respondents)', 'Paired (Matched Participants)']
    pre_values = [
        awareness_analysis.get('overall_pre_pct', 0),
        awareness_analysis.get('paired_pre_pct', 0)
    ]
    post_values = [
        awareness_analysis.get('overall_post_pct', 0),
        awareness_analysis.get('paired_post_pct', 0)
    ]
    
    fig_awareness.add_trace(go.Bar(
        name='Before Session',
        x=categories,
        y=pre_values,
        marker_color='#e9ecef',
        text=[f"{v:.1f}%" for v in pre_values],
        textposition='outside',
        textfont=dict(size=14)
    ))
    
    fig_awareness.add_trace(go.Bar(
        name='After Session',
        x=categories,
        y=post_values,
        marker_color='#006341',
        text=[f"{v:.1f}%" for v in post_values],
        textposition='outside',
        textfont=dict(size=14)
    ))
    
    fig_awareness.update_layout(
        barmode='group',
        yaxis_title='Awareness Percentage',
        yaxis=dict(range=[0, 100]),
        height=450,
        font=dict(family="Epilogue", color="#2c3e50"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    
    st.plotly_chart(fig_awareness, use_container_width=True)
    
    # DEMOGRAPHICS
    st.markdown('<p class="section-title">👥 Participant Demographics</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Locations")
        location_data = demographics.get('location', {})
        
        if location_data:
            fig_loc = go.Figure(data=[go.Pie(
                labels=list(location_data.keys()),
                values=list(location_data.values()),
                hole=0.4,
                marker_colors=['#006341', '#00843d', '#93c13f', '#b8d96d', '#d4e89e', '#e9f5c9'],
                textfont=dict(size=14)
            )])
            
            fig_loc.update_layout(
                height=400,
                showlegend=True,
                paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02)
            )
            
            st.plotly_chart(fig_loc, use_container_width=True)
    
    with col2:
        st.markdown("### How They Heard About Us")
        heard_data = demographics.get('heard_about', {})
        
        if heard_data:
            labels = list(heard_data.keys())
            values = list(heard_data.values())
            
            fig_heard = go.Figure(data=[go.Bar(
                x=labels,
                y=values,
                marker_color='#006341',
                text=values,
                textposition='outside',
                textfont=dict(size=14)
            )])
            
            fig_heard.update_layout(
                height=400,
                yaxis_title='Number of Participants',
                font=dict(family="Epilogue", color="#2c3e50"),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            
            st.plotly_chart(fig_heard, use_container_width=True)
    
    # SATISFACTION DISTRIBUTION
    st.markdown('<p class="section-title">⭐ Satisfaction Distribution</p>', unsafe_allow_html=True)
    
    sat_dist = satisfaction.get('distribution', {})
    if sat_dist:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            labels = [f"{k} Stars" for k in sorted(sat_dist.keys())]
            values = [sat_dist[k] for k in sorted(sat_dist.keys())]
            colors = ['#93c13f' if int(k) >= 4 else '#f39c12' for k in sorted(sat_dist.keys())]
            
            fig_sat = go.Figure(data=[go.Bar(
                x=labels,
                y=values,
                marker_color=colors,
                text=values,
                textposition='outside',
                textfont=dict(size=16)
            )])
            
            fig_sat.update_layout(
                height=350,
                yaxis_title='Number of Participants',
                font=dict(family="Epilogue", color="#2c3e50"),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            
            st.plotly_chart(fig_sat, use_container_width=True)
        
        with col2:
            st.markdown("### Summary")
            st.metric("Average Rating", f"{satisfaction.get('average_score', 0):.2f}/5.0")
            st.metric("Highly Satisfied", f"{satisfaction.get('satisfied_pct', 0):.0f}%")
            st.metric("Total Responses", TOTAL_POST)
    
    # FOOTER
    st.markdown(f"""
    <div class='sls-footer'>
        <h2>10x Leaders Program</h2>
        <p class="tagline">Misk Tracks • Australia Chapter</p>
        <div style='display: flex; justify-content: center; gap: 3rem; margin: 2rem 0; flex-wrap: wrap; position: relative; z-index: 1;'>
            <div>
                <div style='font-size: 2.5rem; font-weight: 700;'>{ACTUAL_ATTENDEES}</div>
                <div style='opacity: 0.8;'>Participants</div>
            </div>
            <div>
                <div style='font-size: 2.5rem; font-weight: 700;'>+{paired_increase:.1f}%</div>
                <div style='opacity: 0.8;'>Awareness Growth</div>
            </div>
            <div>
                <div style='font-size: 2.5rem; font-weight: 700;'>{satisfaction.get('average_score', 0):.2f}/5</div>
                <div style='opacity: 0.8;'>Satisfaction</div>
            </div>
        </div>
        <p style='font-size: 1.1rem; margin-top: 2rem; opacity: 0.9; position: relative; z-index: 1;'>
            <strong>Leadership • Excellence • Impact</strong>
        </p>
        <p style='font-size: 0.9rem; opacity: 0.7; margin-top: 1rem; position: relative; z-index: 1;'>
            {datetime.now().strftime('%B %d, %Y')} | 10x Leaders
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.stop()

# ============================================================================
# STANDARD SESSION DASHBOARD (for regular sessions)
# ============================================================================

metrics = data['metrics']
viz_data = data.get('visualization_data', {})
chapter_metrics = metrics.get('chapter_metrics', {})

REGISTERED = chapter_metrics.get('total_registered', 0)
TARGET = chapter_metrics.get('target_attendance', 50)
ACTUAL_ATTENDEES = chapter_metrics.get('actual_attendees', 0)

# ============================================================================
# KEY PERFORMANCE INDICATORS
# ============================================================================

st.markdown('<p class="section-title">📊 Key Performance Indicators</p>', unsafe_allow_html=True)

# ROW 1: REACH & ENGAGEMENT
st.markdown('<p class="subsection-title">Reach & Participation</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    attendance_rate = (ACTUAL_ATTENDEES / REGISTERED * 100) if REGISTERED > 0 else 0
    st.markdown(
        create_kpi_card(
            "REACH",
            "Total Participants",
            f"{ACTUAL_ATTENDEES}",
            f"Out of {REGISTERED} registered",
            f"✓ {attendance_rate:.0f}% attendance rate"
        ),
        unsafe_allow_html=True
    )

with col2:
    survey_completion = (metrics['total_responses'] / ACTUAL_ATTENDEES * 100) if ACTUAL_ATTENDEES > 0 else 0
    st.markdown(
        create_kpi_card(
            "ENGAGEMENT",
            "Completed Both Surveys",
            f"{metrics['total_responses']}",
            f"Out of {ACTUAL_ATTENDEES} participants",
            "✓ High engagement" if survey_completion >= 50 else "→ Can improve"
        ),
        unsafe_allow_html=True
    )

with col3:
    target_performance = (ACTUAL_ATTENDEES / TARGET * 100) if TARGET > 0 else 0
    st.markdown(
        create_kpi_card(
            "TARGET",
            "Goal Achievement",
            f"{target_performance:.0f}%",
            f"Target was {TARGET} participants",
            f"✓ Exceeded target" if ACTUAL_ATTENDEES > TARGET else "→ Approaching target"
        ),
        unsafe_allow_html=True
    )

# ROW 2: LEARNING EFFECTIVENESS
st.markdown('<p class="subsection-title">Learning Effectiveness</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    avg_growth = metrics.get('grow_avg_knowledge_increase', 0)
    st.markdown(
        create_kpi_card(
            "KNOWLEDGE",
            "Average Growth",
            f"+{avg_growth:.2f}",
            "Points improvement (1-5 scale)",
            f"✓ Strong growth" if avg_growth >= 1.0 else "→ Moderate growth"
        ),
        unsafe_allow_html=True
    )

with col2:
    improved_pct = metrics.get('grow_members_reporting_growth_pct', 0)
    st.markdown(
        create_kpi_card(
            "LEARNING",
            "Participants Improved",
            f"{improved_pct:.0f}%",
            "Showed knowledge gain",
            f"✓ Excellent reach" if improved_pct >= 70 else "→ Good reach"
        ),
        unsafe_allow_html=True
    )

with col3:
    significant_pct = metrics.get('grow_significant_growth_pct', 0)
    st.markdown(
        create_kpi_card(
            "IMPACT",
            "Significant Growth",
            f"{significant_pct:.0f}%",
            "Gained ≥0.5 points",
            f"✓ Deep learning" if significant_pct >= 50 else "→ Solid progress"
        ),
        unsafe_allow_html=True
    )

# ROW 3: ACTION & SATISFACTION
st.markdown('<p class="subsection-title">Action & Satisfaction</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    action_pct = metrics.get('connect_members_planning_action_pct', 0)
    action_count = metrics.get('connect_total_planning_action', 0)
    st.markdown(
        create_kpi_card(
            "COMMITMENT",
            "Plan to Take Action",
            f"{action_pct:.0f}%",
            f"{action_count} participants committed",
            f"✓ Outstanding" if action_pct >= 80 else "✓ Strong" if action_pct >= 60 else "→ Growing"
        ),
        unsafe_allow_html=True
    )

with col2:
    satisfaction = metrics.get('impact_avg_satisfaction', 0)
    st.markdown(
        create_kpi_card(
            "QUALITY",
            "Satisfaction Score",
            f"{satisfaction:.2f}/5.0",
            "Average participant rating",
            f"✓ Excellent" if satisfaction >= 4.5 else "✓ Very good" if satisfaction >= 4.0 else "→ Good"
        ),
        unsafe_allow_html=True
    )

with col3:
    satisfied_pct = metrics.get('impact_satisfaction_pct', 0)
    st.markdown(
        create_kpi_card(
            "SATISFACTION",
            "Highly Satisfied",
            f"{satisfied_pct:.0f}%",
            "Rated 4+ stars",
            f"✓ Strong approval" if satisfied_pct >= 70 else "→ Positive reception"
        ),
        unsafe_allow_html=True
    )

# ============================================================================
# SESSION HIGHLIGHTS
# ============================================================================

achievements = []

if action_pct >= 80:
    achievements.append(f"{action_pct:.0f}% of participants committed to taking action")

if satisfaction >= 4.0:
    achievements.append(f"Achieved {satisfaction:.1f}/5.0 satisfaction rating")

if ACTUAL_ATTENDEES > TARGET:
    achievements.append(f"Exceeded attendance target by {((ACTUAL_ATTENDEES-TARGET)/TARGET*100):.0f}%")

if avg_growth >= 1.0:
    achievements.append(f"Strong knowledge improvement of +{avg_growth:.2f} points")

if achievements:
    st.markdown(f"""
    <div class="highlight-box">
        <h3>✨ Session Highlights</h3>
        <ul>
            {''.join([f'<li>{achievement}</li>' for achievement in achievements])}
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# PARTICIPANT JOURNEY
# ============================================================================

st.markdown('<p class="section-title">🎓 Participant Journey</p>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    funnel_fig = go.Figure()
    
    funnel_fig.add_trace(go.Funnel(
        y=['Registered', 'Attended', 'Completed Both Surveys', 'Plan to Act'],
        x=[REGISTERED, ACTUAL_ATTENDEES, metrics['total_responses'], metrics.get('connect_total_planning_action', 0)],
        textposition="inside",
        textinfo="value+percent initial",
        marker={
            "color": ['#006341', '#00843d', '#93c13f', '#b8d96d'],
            "line": {"width": 2, "color": "white"}
        }
    ))
    
    funnel_fig.update_layout(
        height=400,
        font=dict(family="Epilogue", size=14, color="#2c3e50"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.plotly_chart(funnel_fig, use_container_width=True)

with col2:
    st.markdown("### Conversion Metrics")
    
    reg_to_attend = (ACTUAL_ATTENDEES / REGISTERED * 100) if REGISTERED > 0 else 0
    attend_to_survey = (metrics['total_responses'] / ACTUAL_ATTENDEES * 100) if ACTUAL_ATTENDEES > 0 else 0
    survey_to_action = (metrics.get('connect_total_planning_action', 0) / metrics['total_responses'] * 100) if metrics['total_responses'] > 0 else 0
    
    st.metric("Registered → Attended", f"{reg_to_attend:.0f}%")
    st.metric("Attended → Surveyed", f"{attend_to_survey:.0f}%")
    st.metric("Surveyed → Committed", f"{survey_to_action:.0f}%")
    
    st.markdown("---")
    
    overall = (metrics.get('connect_total_planning_action', 0) / REGISTERED * 100) if REGISTERED > 0 else 0
    st.info(f"**Overall:** {overall:.0f}% of registrants became committed participants")

# ============================================================================
# DETAILED ANALYSIS TABS
# ============================================================================

st.markdown("---")
st.markdown('<p class="section-title">📚 Detailed Analysis</p>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🌱 Knowledge Development", "🤝 Commitment", "💡 Satisfaction"])

with tab1:
    st.markdown("### Learning Progress")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Use session-specific topic labels instead of hardcoded ones from JSON
        topics = session_info['topic_labels']
        pre_scores = viz_data['knowledge_comparison']['pre_scores']
        post_scores = viz_data['knowledge_comparison']['post_scores']
        improvements = viz_data['knowledge_comparison']['improvements']
        
        knowledge_fig = go.Figure()
        
        knowledge_fig.add_trace(go.Bar(
            name='Before Session',
            x=topics,
            y=pre_scores,
            marker_color='#e9ecef',
            text=[f"{s:.2f}" for s in pre_scores],
            textposition='outside'
        ))
        
        knowledge_fig.add_trace(go.Bar(
            name='After Session',
            x=topics,
            y=post_scores,
            marker_color='#006341',
            text=[f"{s:.2f}" for s in post_scores],
            textposition='outside'
        ))
        
        knowledge_fig.update_layout(
            barmode='group',
            yaxis_title='Knowledge Level (1-5)',
            yaxis=dict(range=[0, 6]),
            height=400,
            font=dict(family="Epilogue", color="#2c3e50"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
        )
        
        st.plotly_chart(knowledge_fig, use_container_width=True)
    
    with col2:
        st.markdown("### Key Metrics")
        st.metric("Average Growth", f"+{metrics.get('grow_avg_knowledge_increase', 0):.2f} pts")
        st.metric("Participants Improved", f"{metrics.get('grow_members_reporting_growth_pct', 0):.0f}%")
        st.metric("Significant Growth", f"{metrics.get('grow_significant_growth_pct', 0):.0f}%")
        
        st.markdown("### Growth by Topic")
        for i, topic in enumerate(topics):
            pct = (improvements[i] / pre_scores[i] * 100) if pre_scores[i] > 0 else 0
            st.markdown(f"**{topic}:** +{pct:.0f}%")

with tab2:
    st.markdown("### Action Commitment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        action_data = viz_data.get('action_plan_data', {})
        labels = list(action_data.keys())
        values = list(action_data.values())
        
        # Find the committed count safely by looking for Yes/True key, fallback to connect metric
        committed_count = metrics.get('connect_total_planning_action', 0)
        
        action_fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.6,
            marker_colors=['#006341', '#e9ecef'],
            textfont=dict(size=16, family='Epilogue')
        )])
        
        action_fig.update_layout(
            height=350,
            showlegend=True,
            annotations=[dict(
                text=f"<b>{committed_count}</b><br>Committed",
                x=0.5, y=0.5,
                font=dict(size=20, family='Cormorant Garamond'),
                showarrow=False
            )],
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        
        st.plotly_chart(action_fig, use_container_width=True)
    
    with col2:
        st.markdown("### Summary")
        st.metric("Commitment Rate", f"{metrics.get('connect_members_planning_action_pct', 0):.1f}%")
        st.metric("Total Committed", metrics.get('connect_total_planning_action', 0))
        st.metric("Would Recommend", f"{metrics.get('impact_likely_recommend_pct', 0):.1f}%")
        
        st.markdown("---")
        st.success(f"**{metrics.get('connect_total_planning_action', 0)} participants** ready to apply what they learned")

with tab3:
    st.markdown("### Participant Feedback")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        satisfaction_data = viz_data.get('satisfaction_data', {})
        
        if satisfaction_data:
            satisfaction_order = ['Very dissatisfied', 'Dissatisfied', 'Neutral', 'Satisfied', 'Very satisfied']
            sorted_items = sorted(
                satisfaction_data.items(),
                key=lambda x: satisfaction_order.index(x[0]) if x[0] in satisfaction_order else 2
            )
            labels = [item[0] for item in sorted_items]
            values = [item[1] for item in sorted_items]
            colors = ['#e74c3c', '#e67e22', '#f39c12', '#93c13f', '#006341'][:len(labels)]
            
            sat_fig = go.Figure(data=[go.Bar(
                y=labels,
                x=values,
                orientation='h',
                marker_color=colors,
                text=values,
                textposition='outside',
                textfont=dict(size=14)
            )])
            
            sat_fig.update_layout(
                xaxis_title='Number of Participants',
                height=350,
                font=dict(family="Epilogue", color="#2c3e50"),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            
            st.plotly_chart(sat_fig, use_container_width=True)
    
    with col2:
        st.markdown("### Metrics")
        st.metric("Average Rating", f"{metrics.get('impact_avg_satisfaction', 0):.2f}/5.0")
        st.metric("Highly Satisfied", f"{metrics.get('impact_satisfaction_pct', 0):.0f}%")
        st.metric("Likely to Recommend", f"{metrics.get('impact_likely_recommend_pct', 0):.1f}%")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown(f"""
<div class='sls-footer'>
    <h2>Saudi Leadership Society</h2>
    <p class="tagline">Towards the Vision • Australia Chapter</p>
    <div style='display: flex; justify-content: center; gap: 3rem; margin: 2rem 0; flex-wrap: wrap; position: relative; z-index: 1;'>
        <div>
            <div style='font-size: 2.5rem; font-weight: 700;'>{ACTUAL_ATTENDEES}</div>
            <div style='opacity: 0.8;'>Participants</div>
        </div>
        <div>
            <div style='font-size: 2.5rem; font-weight: 700;'>+{metrics.get('grow_avg_knowledge_increase', 0):.2f}</div>
            <div style='opacity: 0.8;'>Avg Growth</div>
        </div>
        <div>
            <div style='font-size: 2.5rem; font-weight: 700;'>{metrics.get('connect_total_planning_action', 0)}</div>
            <div style='opacity: 0.8;'>Taking Action</div>
        </div>
    </div>
    <p style='font-size: 1.1rem; margin-top: 2rem; opacity: 0.9; position: relative; z-index: 1;'>
        <strong>Grow • Connect • Impact</strong>
    </p>
    <p style='font-size: 0.9rem; opacity: 0.7; margin-top: 1rem; position: relative; z-index: 1;'>
        {datetime.now().strftime('%B %d, %Y')} | Vision 2030
    </p>
</div>
""", unsafe_allow_html=True)
