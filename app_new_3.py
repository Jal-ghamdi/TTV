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
            },
            "Health": {
                "name": "🏥 Health Session",
                "data_file": "sls_kpi_health_session3_ttv_data_updated.json",
                "icon": "🏥",
                "vision_theme": "Health Sector Development",
                "color": "#10b981",
                "topic_labels": ["Health Sector Knowledge", "Vision 2030 Contribution", "Job Market Awareness", "In-Demand Skills"],
                "type": "health"
            },
            "Nursing": {
                "name": "💉 Nursing Session",
                "data_file": "sls_kpi_nursing_final.json",
                "icon": "💉",
                "vision_theme": "Nursing Sector Development",
                "color": "#0ea5e9",
                "topic_keys": ["grow_nursing_knowledge", "grow_vision2030", "grow_job_market", "grow_skills"],
                "topic_labels": ["Nursing Knowledge", "Vision 2030 Contribution", "Job Market Awareness", "In-Demand Skills"],
                "type": "health"
        }
            #"Health": {
               # "name": "🏥 Health Session",
               # "data_file": "sls_kpi_health_session3_ttv_data_updated.json",
               # "icon": "🏥",
               # "vision_theme": "Health Sector Development",
               # "color": "#10b981",
               # "topic_labels": ["Health Sector Knowledge", "Vision 2030 Contribution", "Job Market Awareness", "In-Demand Skills"],
               # "type": "health"
            #}
        }
    },
    "Misk Tracks": {
        "name": "Misk Tracks",
        "icon": "🚀",
        "description": "An initiative highlighting Misk Foundation's four tracks — Leadership, Entrepreneurship, Skills, and Community — to help Saudi students in Australia explore programs aligned with their academic and career goals.",
        "color": "#8B5CF6",
        "sessions": {
            "Awareness Study": {
                "name": "📊 Misk Tracks Awareness",
                "data_file": "misk_tracks_awareness_session.json",
                "icon": "📊",
                "vision_theme": "Baseline Awareness Assessment",
                "color": "#10b981",
                "topic_labels": [],
                "type": "awareness"
            },
            "10x Leaders": {
                "name": "⭐ 10x Leaders Program",
                "data_file": "sls_kpi_10xleaders_session_data_updated_overall.json",
                "icon": "⭐",
                "vision_theme": "Leadership Development & Excellence",
                "color": "#f59e0b",
                "topic_labels": [],
                "type": "comprehensive"
            }
        }
    },
    "Leaders Network Circles": {
    "name": "Leaders Network Circles",
    "icon": "🔗",
    "description": "Professional networking circles connecting Saudi health students and professionals in Australia across Growth, Connection, and Impact circles — aligned with Vision 2030.",
    "color": "#0d3b6e",
    "sessions": {
        "Health Sector Session 1": {
            "name": "🏥 Health Sector — Session 1",
            "data_file": "lnc_health_session1_data.json",
            "icon": "🏥",
            "vision_theme": "Professional Networking & Career Development",
            "color": "#0d3b6e",
            "topic_labels": [],
            "type": "lnc"
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

    .kpi-trend-warn {
        font-family: 'Epilogue', sans-serif;
        font-size: 0.85rem;
        font-weight: 700;
        color: #b45309;
        margin-top: 0.75rem;
        padding: 0.5rem 1rem;
        background: rgba(180, 83, 9, 0.08);
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

def create_kpi_card(category, label, value, context, trend="", warn=False):
    if trend:
        trend_class = "kpi-trend-warn" if warn else "kpi-trend"
        trend_html = f'<div class="{trend_class}">{trend}</div>'
    else:
        trend_html = ''
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
    st.markdown(
    '<p class="section-title" style="color:white; font-size:24px; font-weight:bold;">🌟 Select an Initiative</p>',
    unsafe_allow_html=True
)
    
    #st.markdown('<p class="section-title">🌟 Select an Initiative</p>', unsafe_allow_html=True)
    
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
    cols = st.columns(min(len(sessions), 3))
    
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



# =====================================
# LEADERS NETWORK CIRCLES 
# =====================================
# ============================================================================
# LEADERS NETWORK CIRCLES DASHBOARD
# ============================================================================
if session_info.get('type') == 'lnc':

    # ── HARD-CODED SURVEY DATA (27 respondents, pre + post) ──────────────────
    lnc = {
        "participants": 27,
        "pre": {
            "registration_excellent_pct": 77.8,
            "atmosphere_comfortable_pct": 63.0,
            "atmosphere_overwhelming_pct": 22.2,
            "experience_very_good_pct": 66.7,
            "nps_promoters": 12, "nps_passives": 9, "nps_detractors": 6,
            "confidence": {
                "Extremely confident": 12,
                "Somewhat confident": 5,
                "Neutral": 9,
                "Somewhat not confident": 1,
                "Extremely not confident": 0
            },
            "barriers": {
                "Difficulty finding relevant people": 10,
                "Not knowing how to start conversations": 8,
                "Shyness / anxiety": 6,
                "Other": 3
            },
            "goals": {
                "Friendships": 20, "Professional network": 21,
                "Mentor": 13, "Research / projects": 10, "Saudi community": 14
            },
            "connection_targets": {"1-2": 8, "3-5": 9, "6-9": 5, "10-12": 2, "12+": 3},
            "heard_about": {
                "Friend/colleague referral": 13, "WhatsApp": 10,
                "Other": 2, "Snapchat": 2, "LinkedIn": 0
            }
        },
        "post": {
            "format_excellent_pct": 85.2,
            "atmosphere_comfortable_pct": 85.2,
            "atmosphere_overwhelming_pct": 0,
            "experience_very_good_pct": 88.9,
            "nps_promoters": 17, "nps_passives": 8, "nps_detractors": 2,
            "confidence_improved_significantly": 19,
            "confidence_improved_slightly": 7,
            "confidence_no_change": 1,
            "network_expanded_significantly_pct": 66.7,
            "network_expanded_moderately_pct": 22.2,
            "career_opps_yes_pct": 51.9,
            "career_opps_possibly_pct": 22.2,
            "business_opps_significantly": 15,
            "research_opps_yes": 8, "research_opps_maybe": 11, "research_opps_no": 8,
            "recommend_highly_pct": 74.1,
            "recommend_slightly_pct": 18.5,
            "linkedin_connections": {"1-2": 3, "3-5": 9, "6-9": 9, "10-12": 4, "12+": 2},
            "meaningful_connections": {"1-2": 9, "3-5": 8, "6-9": 5, "10-12": 2, "12+": 3},
            "goals_achieved": {
                "Friendships": 22, "Professional network": 24,
                "Mentor": 9, "Research / projects": 9, "Saudi community": 15
            },
            "barriers_overcome": {
                "Difficulty finding relevant people": 9,
                "Not knowing how to start conversations": 8,
                "Shyness / anxiety": 6, "Other": 4
            },
            "circles_helped": {
                "Easier to engage": 20,
                "Better health sector understanding": 16,
                "Insights into future of health sector": 15,
                "Identified skills to develop": 9,
                "Not helpful": 3
            },
            "compared_to_other_events": {
                "First event": 9, "Much better": 6, "Somewhat better": 7,
                "About the same": 4, "Needs improvement": 1
            }
        }
    }

    p = lnc["pre"]
    q = lnc["post"]
    N = lnc["participants"]

    st.markdown('<p class="section-title">📊 Key Performance Indicators</p>', unsafe_allow_html=True)
    st.markdown('<p class="subsection-title">Reach & Engagement</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(create_kpi_card("REACH", "Total Participants", str(N),
            "Attended & completed both surveys",
            "✓ 100% survey completion"), unsafe_allow_html=True)
    with col2:
        st.markdown(create_kpi_card("FORMAT", "Circles Format Rating",
            f"{q['format_excellent_pct']:.0f}%",
            "Rated Excellent",
            "✓ Up from Very Good pre-event"), unsafe_allow_html=True)
    with col3:
        nps_pre  = round((p['nps_promoters'] - p['nps_detractors']) / N * 100)
        nps_post = round((q['nps_promoters'] - q['nps_detractors']) / N * 100)
        st.markdown(create_kpi_card("NPS", "Net Promoter Score",
            f"{nps_post}",
            f"Post-event (was {nps_pre} pre-event)",
            f"✓ +{nps_post - nps_pre} point improvement"), unsafe_allow_html=True)

    st.markdown('<p class="subsection-title">Networking Outcomes</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        conf_pct = round((q['confidence_improved_significantly'] + q['confidence_improved_slightly']) / N * 100)
        st.markdown(create_kpi_card("CONFIDENCE", "Confidence Boosted",
            f"{conf_pct}%",
            f"{q['confidence_improved_significantly']} significantly, {q['confidence_improved_slightly']} slightly",
            "✓ Strong impact"), unsafe_allow_html=True)
    with col2:
        career_pct = round((q['career_opps_yes_pct'] + q['career_opps_possibly_pct']))
        st.markdown(create_kpi_card("CAREERS", "Career Opportunities",
            f"{career_pct:.0f}%",
            "Identified definite or possible career opps",
            "✓ High value"), unsafe_allow_html=True)
    with col3:
        rec_pct = q['recommend_highly_pct'] + q['recommend_slightly_pct']
        st.markdown(create_kpi_card("ADVOCACY", "Would Recommend",
            f"{rec_pct:.0f}%",
            f"{round(q['recommend_highly_pct']*N/100)} highly recommend",
            "✓ Outstanding word-of-mouth"), unsafe_allow_html=True)

    # ── HIGHLIGHT BOX ─────────────────────────────────────────────────────────
    achievements = [
        f"{q['format_excellent_pct']:.0f}% rated the Circles networking format as Excellent",
        f"Professional network expansion exceeded intent: 21 aimed → 24 achieved",
        f"Atmosphere anxiety dropped from 22% to 0% — format removed the awkwardness",
        f"NPS improved from {nps_pre} to {nps_post} — a {nps_post-nps_pre} point jump",
        f"{round(q['confidence_improved_significantly']/N*100)}% significantly improved their networking confidence"
    ]
    st.markdown(f"""
    <div class="highlight-box">
        <h3>✨ Leaders Network Circles — Session Highlights</h3>
        <ul>{''.join([f'<li>{a}</li>' for a in achievements])}</ul>
    </div>
    """, unsafe_allow_html=True)

    # ── DETAILED TABS ──────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<p class="section-title">📚 Detailed Analysis</p>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "🌐 Experience", "🤝 Connections", "💼 Outcomes", "👥 Demographics"
    ])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Atmosphere — Before vs After")
            atm_fig = go.Figure()
            atm_labels = ["Comfortable & friendly", "Professional & organized", "Overwhelming"]
            atm_pre  = [17, 11, 6]
            atm_post = [23, 11, 0]
            atm_fig.add_trace(go.Bar(name='Before', x=atm_labels, y=atm_pre,
                marker_color='#e9ecef', text=atm_pre, textposition='outside'))
            atm_fig.add_trace(go.Bar(name='After', x=atm_labels, y=atm_post,
                marker_color='#0d3b6e', text=atm_post, textposition='outside'))
            atm_fig.update_layout(barmode='group', height=360, yaxis=dict(range=[0,30]),
                font=dict(family="Epilogue", color="#2c3e50"),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5))
            st.plotly_chart(atm_fig, use_container_width=True)
        with col2:
            st.markdown("### Overall Experience")
            exp_fig = go.Figure(data=[go.Bar(
                x=["Very Good", "Average", "Below Avg", "Very Poor"],
                y=[18, 9, 0, 0],
                name="Before",
                marker_color="#e9ecef",
                text=[18,9,0,0], textposition='outside'
            )])
            exp_fig.add_trace(go.Bar(
                x=["Very Good", "Average", "Below Avg", "Very Poor"],
                y=[24, 2, 0, 1],
                name="After",
                marker_color="#0d3b6e",
                text=[24,2,0,1], textposition='outside'
            ))
            exp_fig.update_layout(barmode='group', height=360, yaxis=dict(range=[0,30]),
                font=dict(family="Epilogue", color="#2c3e50"),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5))
            st.plotly_chart(exp_fig, use_container_width=True)

        st.markdown("### NPS Shift")
        nps_fig = go.Figure(data=[go.Bar(
            x=["Promoters", "Passives", "Detractors"],
            y=[p['nps_promoters'], p['nps_passives'], p['nps_detractors']],
            name="Before", marker_color=["#93c13f","#f39c12","#e74c3c"],
            text=[p['nps_promoters'], p['nps_passives'], p['nps_detractors']],
            textposition='outside'
        )])
        nps_fig.add_trace(go.Bar(
            x=["Promoters", "Passives", "Detractors"],
            y=[q['nps_promoters'], q['nps_passives'], q['nps_detractors']],
            name="After", marker_color=["#006341","#e67e22","#c0392b"],
            text=[q['nps_promoters'], q['nps_passives'], q['nps_detractors']],
            textposition='outside'
        ))
        nps_fig.update_layout(barmode='group', height=350, yaxis=dict(range=[0,25]),
            font=dict(family="Epilogue", color="#2c3e50"),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5))
        st.plotly_chart(nps_fig, use_container_width=True)

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### LinkedIn Connections Made")
            li_labels = list(q['linkedin_connections'].keys())
            li_vals   = list(q['linkedin_connections'].values())
            li_fig = go.Figure(data=[go.Bar(
                x=li_labels, y=li_vals, marker_color='#0d3b6e',
                text=li_vals, textposition='outside'
            )])
            li_fig.update_layout(height=300, yaxis=dict(range=[0,12]),
                font=dict(family="Epilogue", color="#2c3e50"),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
            st.plotly_chart(li_fig, use_container_width=True)
        with col2:
            st.markdown("### Meaningful Connections")
            mc_labels = list(q['meaningful_connections'].keys())
            mc_vals   = list(q['meaningful_connections'].values())
            mc_fig = go.Figure(data=[go.Bar(
                x=mc_labels, y=mc_vals, marker_color='#006341',
                text=mc_vals, textposition='outside'
            )])
            mc_fig.update_layout(height=300, yaxis=dict(range=[0,12]),
                font=dict(family="Epilogue", color="#2c3e50"),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
            st.plotly_chart(mc_fig, use_container_width=True)

        st.markdown("### Goals: Intended vs Achieved")
        goals_labels = list(p['goals'].keys())
        goals_pre  = list(p['goals'].values())
        goals_post = list(q['goals_achieved'].values())
        gf = go.Figure()
        gf.add_trace(go.Bar(name='Intended (pre)', x=goals_labels, y=goals_pre,
            marker_color='#e9ecef', text=goals_pre, textposition='outside'))
        gf.add_trace(go.Bar(name='Achieved (post)', x=goals_labels, y=goals_post,
            marker_color='#0d3b6e', text=goals_post, textposition='outside'))
        gf.update_layout(barmode='group', height=380, yaxis=dict(range=[0,30]),
            font=dict(family="Epilogue", color="#2c3e50"),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5))
        st.plotly_chart(gf, use_container_width=True)

        st.markdown("### Confidence Impact")
        conf_labels = ["Significantly improved", "Slightly improved", "No change"]
        conf_vals   = [q['confidence_improved_significantly'], q['confidence_improved_slightly'], q['confidence_no_change']]
        cf = go.Figure(data=[go.Pie(
            labels=conf_labels, values=conf_vals, hole=0.5,
            marker_colors=['#0d3b6e','#378add','#e9ecef'],
            textfont=dict(size=13)
        )])
        cf.update_layout(height=380, paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5))
        st.plotly_chart(cf, use_container_width=True)

    with tab3:
        st.markdown("### Career & Professional Outcomes")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Career Opportunities Identified")
            career_fig = go.Figure(data=[go.Pie(
                labels=["Yes, definitely","Possibly","Not at this stage"],
                values=[14, 6, 7], hole=0.5,
                marker_colors=['#006341','#93c13f','#e9ecef'],
                textfont=dict(size=13)
            )])
            career_fig.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5))
            st.plotly_chart(career_fig, use_container_width=True)
        with col2:
            st.markdown("#### Research/Project Opportunities")
            res_fig = go.Figure(data=[go.Pie(
                labels=["Yes","Maybe","No"],
                values=[8, 11, 8], hole=0.5,
                marker_colors=['#0d3b6e','#85B7EB','#e9ecef'],
                textfont=dict(size=13)
            )])
            res_fig.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5))
            st.plotly_chart(res_fig, use_container_width=True)

        st.markdown("### How Circles Format Helped")
        circles_labels = list(q['circles_helped'].keys())
        circles_vals   = list(q['circles_helped'].values())
        cf2 = go.Figure(data=[go.Bar(
            y=circles_labels, x=circles_vals, orientation='h',
            marker_color=['#006341','#0d3b6e','#378add','#85B7EB','#e9ecef'],
            text=circles_vals, textposition='outside'
        )])
        cf2.update_layout(height=300, xaxis=dict(range=[0,25]),
            font=dict(family="Epilogue", color="#2c3e50"),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False,
            margin=dict(l=10, r=40, t=10, b=20))
        st.plotly_chart(cf2, use_container_width=True)

        st.markdown("### How This Compared to Other Events")
        comp_labels = list(q['compared_to_other_events'].keys())
        comp_vals   = list(q['compared_to_other_events'].values())
        comp_colors = ['#e9ecef','#006341','#00843d','#93c13f','#e74c3c']
        comp_fig = go.Figure(data=[go.Bar(
            x=comp_labels, y=comp_vals,
            marker_color=comp_colors, text=comp_vals, textposition='outside'
        )])
        comp_fig.update_layout(height=320, yaxis=dict(range=[0,12]),
            font=dict(family="Epilogue", color="#2c3e50"),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
        st.plotly_chart(comp_fig, use_container_width=True)

    with tab4:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### How Did They Hear About Us?")
            heard_fig = go.Figure(data=[go.Bar(
                x=list(p['heard_about'].keys()),
                y=list(p['heard_about'].values()),
                marker_color=['#0d3b6e','#378add','#85B7EB','#B5D4F4','#e9ecef'],
                text=list(p['heard_about'].values()), textposition='outside'
            )])
            heard_fig.update_layout(height=350, yaxis=dict(range=[0,16]),
                font=dict(family="Epilogue", color="#2c3e50"),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
            st.plotly_chart(heard_fig, use_container_width=True)
        with col2:
            st.markdown("#### Pre-Event Confidence Level")
            conf_pre_fig = go.Figure(data=[go.Bar(
                x=list(p['confidence'].keys()),
                y=list(p['confidence'].values()),
                marker_color=['#006341','#00843d','#93c13f','#f39c12','#e9ecef'],
                text=list(p['confidence'].values()), textposition='outside'
            )])
            conf_pre_fig.update_layout(height=350, yaxis=dict(range=[0,15]),
                font=dict(family="Epilogue", color="#2c3e50"),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
            st.plotly_chart(conf_pre_fig, use_container_width=True)

    st.markdown(f"""
    <div class="info-box">
        <h3>📋 About Leaders Network Circles</h3>
        <p>
            Leaders Network Circles is the <strong>third initiative</strong> of the Saudi Leadership Society Australia Chapter.
            It brings together Saudi health students and professionals through a structured circle-rotation format — 
            six short rounds of small-group conversations across three circles: <strong>Growth, Connection, and Impact</strong>.
            Participants build genuine relationships, explore career pathways, and strengthen the Saudi health 
            community abroad — all aligned with <strong>Vision 2030</strong>'s health sector goals.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='sls-footer'>
        <h2>🔗 Leaders Network Circles</h2>
        <p class="tagline">Health Sector Session 1 • Australia Chapter</p>
        <div style='display: flex; justify-content: center; gap: 3rem; margin: 2rem 0; flex-wrap: wrap; position: relative; z-index: 1;'>
            <div><div style='font-size: 2.5rem; font-weight: 700;'>{N}</div><div style='opacity: 0.8;'>Participants</div></div>
            <div><div style='font-size: 2.5rem; font-weight: 700;'>85%</div><div style='opacity: 0.8;'>Excellent rating</div></div>
            <div><div style='font-size: 2.5rem; font-weight: 700;'>+{nps_post-nps_pre}</div><div style='opacity: 0.8;'>NPS increase</div></div>
            <div><div style='font-size: 2.5rem; font-weight: 700;'>74%</div><div style='opacity: 0.8;'>Career opps found</div></div>
        </div>
        <p style='font-size: 1.1rem; margin-top: 2rem; opacity: 0.9; position: relative; z-index: 1;'><strong>Grow • Connect • Impact</strong></p>
        <p style='font-size: 0.9rem; opacity: 0.7; margin-top: 1rem; position: relative; z-index: 1;'>{datetime.now().strftime('%B %d, %Y')} | Vision 2030</p>
    </div>
    """, unsafe_allow_html=True)

    st.stop()
# ============================================================================
# HEALTH SESSION DASHBOARD
# ============================================================================

if session_info.get('type') == 'health':
    metrics = data['metrics']
    topics = session_info['topic_labels']

    # Map the four topic keys in order to their nested metric dicts
    # Auto-detect first topic key — 'grow_sector' for Health, 'grow_nursing_knowledge' for Nursing
    topic_keys = session_info.get('topic_keys', ['grow_sector', 'grow_vision2030', 'grow_job_market', 'grow_skills'])
    #topic_keys = ['grow_sector', 'grow_vision2030', 'grow_job_market', 'grow_skills']
    topic_data = [metrics.get(k, {}) for k in topic_keys]

    pre_scores   = [t.get('pre', 0)         for t in topic_data]
    post_scores  = [t.get('post', 0)        for t in topic_data]
    improvements = [t.get('improvement', 0) for t in topic_data]

    # ── KPI ROW 1 : REACH & ENGAGEMENT ──────────────────────────────────────
    st.markdown('<p class="section-title">📊 Key Performance Indicators</p>', unsafe_allow_html=True)
    st.markdown('<p class="subsection-title">Reach & Participation</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            create_kpi_card(
                "REACH",
                "Total Participants",
                str(metrics['total_participants_pre']),
                "Attended the Health session",
                f"✓ {metrics['total_participants_post']} completed post-survey"
            ),
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            create_kpi_card(
                "ENGAGEMENT",
                "Completed Both Surveys",
                str(metrics['total_responses']),
                "Matched pre & post responses",
                f"✓ {metrics['match_rate_pct']:.1f}% match rate"
            ),
            unsafe_allow_html=True
        )

    with col3:
        improved_pct = metrics.get('grow_members_reporting_growth_pct', 0)
        st.markdown(
            create_kpi_card(
                "LEARNING",
                "Participants Improved",
                f"{improved_pct:.1f}%",
                "Showed knowledge gain across topics",
                "✓ Strong majority" if improved_pct >= 60 else "→ Solid progress"
            ),
            unsafe_allow_html=True
        )

    # ── KPI ROW 2 : LEARNING EFFECTIVENESS ───────────────────────────────────
    st.markdown('<p class="subsection-title">Learning Effectiveness by Topic</p>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    card_configs = [
        ("SECTOR",     topics[0], 0),
        ("VISION",     topics[1], 1),
        ("JOB MARKET", topics[2], 2),
        ("SKILLS",     topics[3], 3),
    ]

    cols_row = [col1, col2, col3, col4]
    for col, (cat, label, i) in zip(cols_row, card_configs):
        imp = improvements[i]
        is_positive = imp >= 0
        trend_text = f"{'✓' if is_positive else '▼'} {imp:+.2f} pts ({pre_scores[i]:.2f} → {post_scores[i]:.2f})"
        with col:
            st.markdown(
                create_kpi_card(
                    cat,
                    label,
                    f"{post_scores[i]:.2f}",
                    "Post-session score (out of 5)",
                    trend_text,
                    warn=(not is_positive)
                ),
                unsafe_allow_html=True
            )

    # ── KPI ROW 3 : OVERALL GROWTH ────────────────────────────────────────────
    st.markdown('<p class="subsection-title">Overall Knowledge Growth</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    avg_growth = metrics.get('grow_avg_knowledge_increase', 0)
    avg_pre  = sum(pre_scores)  / len(pre_scores)
    avg_post = sum(post_scores) / len(post_scores)

    with col1:
        st.markdown(
            create_kpi_card(
                "BASELINE",
                "Average Pre-Score",
                f"{avg_pre:.2f}/5",
                "Across all four knowledge topics",
                ""
            ),
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            create_kpi_card(
                "OUTCOME",
                "Average Post-Score",
                f"{avg_post:.2f}/5",
                "Across all four knowledge topics",
                f"✓ +{avg_growth:.2f} pts average increase" if avg_growth >= 0 else f"▼ {avg_growth:.2f} pts average change",
                warn=(avg_growth < 0)
            ),
            unsafe_allow_html=True
        )

    with col3:
        positive_topics = sum(1 for imp in improvements if imp > 0)
        st.markdown(
            create_kpi_card(
                "BREADTH",
                "Topics with Positive Growth",
                f"{positive_topics} / {len(topics)}",
                "Number of areas that improved",
                "✓ Broad impact" if positive_topics >= 3 else "→ Targeted gains"
            ),
            unsafe_allow_html=True
        )

    # ── SESSION HIGHLIGHTS ─────────────────────────────────────────────────────
    achievements = []
    if improved_pct >= 60:
        achievements.append(f"{improved_pct:.1f}% of paired participants showed knowledge growth")
    best_idx = improvements.index(max(improvements))
    if improvements[best_idx] > 0:
        achievements.append(f"Strongest gain in '{topics[best_idx]}': +{improvements[best_idx]:.2f} pts")
    if positive_topics >= 3:
        achievements.append(f"Positive growth recorded in {positive_topics} out of {len(topics)} topic areas")
    if avg_post >= 3.5:
        achievements.append(f"Post-session average of {avg_post:.2f}/5 across all health topics")

    if achievements:
        st.markdown(f"""
        <div class="highlight-box">
            <h3>✨ Session Highlights</h3>
            <ul>
                {''.join([f'<li>{a}</li>' for a in achievements])}
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # ── DETAILED ANALYSIS TABS ────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<p class="section-title">📚 Detailed Analysis</p>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🌱 Knowledge Development", "🕸️ Knowledge Profile", "👥 Participant Demographics"])

    with tab1:
        st.markdown("### Learning Progress — Before vs After")

        col1, col2 = st.columns([3, 2])

        with col1:
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
                yaxis_title='Knowledge Score (1–5 scale)',
                yaxis=dict(range=[0, 5.8]),
                height=420,
                font=dict(family="Epilogue", color="#2c3e50"),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
            )

            st.plotly_chart(knowledge_fig, use_container_width=True)

        with col2:
            st.markdown("### Growth by Topic")

            bar_colors = ['#006341' if v >= 0 else '#e74c3c' for v in improvements]

            improvement_fig = go.Figure()
            improvement_fig.add_trace(go.Bar(
                x=improvements,
                y=topics,
                orientation='h',
                marker_color=bar_colors,
                text=[f"{v:+.2f}" for v in improvements],
                textposition='outside',
                textfont=dict(size=13)
            ))

            improvement_fig.add_vline(x=0, line_dash="dash", line_color="#adb5bd", line_width=1.5)

            improvement_fig.update_layout(
                xaxis_title='Score Change',
                xaxis=dict(range=[-0.5, 0.8]),
                height=420,
                font=dict(family="Epilogue", color="#2c3e50"),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                margin=dict(l=10, r=40, t=20, b=20)
            )

            st.plotly_chart(improvement_fig, use_container_width=True)

            st.markdown("### Key Metrics")
            st.metric("Average Growth", f"+{avg_growth:.2f} pts")
            st.metric("Participants Improved", f"{improved_pct:.1f}%")
            st.metric("Topics Improved", f"{positive_topics} / {len(topics)}")

    with tab2:
        st.markdown("### Knowledge Profile — Before vs After")

        radar_fig = go.Figure()

        radar_fig.add_trace(go.Scatterpolar(
            r=pre_scores + [pre_scores[0]],
            theta=topics + [topics[0]],
            fill='toself',
            name='Before Session',
            line_color='#adb5bd',
            fillcolor='rgba(173,181,189,0.2)',
            line_width=2
        ))

        radar_fig.add_trace(go.Scatterpolar(
            r=post_scores + [post_scores[0]],
            theta=topics + [topics[0]],
            fill='toself',
            name='After Session',
            line_color='#006341',
            fillcolor='rgba(0,132,61,0.15)',
            line_width=2.5
        ))

        radar_fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 5], tickfont=dict(size=11)),
                angularaxis=dict(tickfont=dict(size=13, family='Epilogue'))
            ),
            showlegend=True,
            height=500,
            font=dict(family="Epilogue", color="#2c3e50"),
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
        )

        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.plotly_chart(radar_fig, use_container_width=True)

        st.markdown("### Score Summary")
        summary_cols = st.columns(len(topics))
        for i, (col, topic) in enumerate(zip(summary_cols, topics)):
            with col:
                delta_val = improvements[i]
                st.metric(
                    label=topic,
                    value=f"{post_scores[i]:.2f}",
                    delta=f"{delta_val:+.2f}",
                    delta_color="normal" if delta_val >= 0 else "inverse"
                )

    with tab3:
        st.markdown("### Who Attended?")

        # Support both nested demographics dict (Health) and flat keys (Nursing)
        demographics = metrics.get('demographics', {})
        location_data  = demographics.get('location', {}) or metrics.get('demographics_location', {})
        heard_data     = demographics.get('heard_about', {}) or metrics.get('demographics_heard_about', {})
        academic_data  = demographics.get('academic_level', {})

        if not location_data and not heard_data and not academic_data:
            st.info("No demographics data available in the JSON yet.")
        else:
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 📍 Location")
                if location_data:
                    fig_loc = go.Figure(data=[go.Pie(
                        labels=list(location_data.keys()),
                        values=list(location_data.values()),
                        hole=0.45,
                        marker_colors=[
                            '#006341', '#00843d', '#93c13f',
                            '#b8d96d', '#d4e89e', '#e9f5c9', '#f4fbe8'
                        ],
                        textfont=dict(size=13, family='Epilogue'),
                        textinfo='label+percent'
                    )])
                    fig_loc.update_layout(
                        height=400,
                        showlegend=True,
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(family="Epilogue", color="#2c3e50"),
                        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02),
                        margin=dict(l=20, r=120, t=20, b=20)
                    )
                    st.plotly_chart(fig_loc, use_container_width=True)

                    top_city = max(location_data, key=location_data.get)
                    top_pct  = round(location_data[top_city] / sum(location_data.values()) * 100)
                    st.markdown(
                        create_kpi_card(
                            "TOP LOCATION", "Most Participants From", top_city,
                            f"{location_data[top_city]} of {sum(location_data.values())} participants ({top_pct}%)",
                            "✓ Strong city representation"
                        ),
                        unsafe_allow_html=True
                    )

            with col2:
                st.markdown("#### 📣 How Did They Hear About Us?")
                if heard_data:
                    heard_labels = list(heard_data.keys())
                    heard_values = list(heard_data.values())
                    heard_colors = ['#006341', '#00843d', '#93c13f', '#b8d96d', '#d4e89e'][:len(heard_labels)]

                    fig_heard = go.Figure(data=[go.Bar(
                        x=heard_labels,
                        y=heard_values,
                        marker_color=heard_colors,
                        text=heard_values,
                        textposition='outside',
                        textfont=dict(size=15, family='Epilogue')
                    )])
                    fig_heard.update_layout(
                        height=380,
                        yaxis_title='Number of Participants',
                        yaxis=dict(range=[0, max(heard_values) * 1.35]),
                        font=dict(family="Epilogue", color="#2c3e50"),
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        showlegend=False,
                        margin=dict(l=20, r=20, t=20, b=60)
                    )
                    st.plotly_chart(fig_heard, use_container_width=True)

                    top_channel = max(heard_data, key=heard_data.get)
                    top_ch_pct  = round(heard_data[top_channel] / sum(heard_data.values()) * 100)
                    st.markdown(
                        create_kpi_card(
                            "TOP CHANNEL", "Primary Outreach Channel", top_channel,
                            f"{heard_data[top_channel]} of {sum(heard_data.values())} participants ({top_ch_pct}%)",
                            "✓ Effective outreach"
                        ),
                        unsafe_allow_html=True
                    )

            # Academic level — only shown if data exists (Health has it, Nursing doesn't)
            if academic_data:
                st.markdown("---")
                st.markdown("#### 🎓 Academic Level")
                col1, col2 = st.columns([3, 2])
                with col1:
                    acad_labels = list(academic_data.keys())
                    acad_values = list(academic_data.values())
                    acad_colors = ['#006341', '#00843d', '#93c13f', '#b8d96d'][:len(acad_labels)]
                    fig_acad = go.Figure(data=[go.Bar(
                        y=acad_labels, x=acad_values, orientation='h',
                        marker_color=acad_colors, text=acad_values,
                        textposition='outside', textfont=dict(size=15, family='Epilogue')
                    )])
                    fig_acad.update_layout(
                        height=320, xaxis_title='Number of Participants',
                        xaxis=dict(range=[0, max(acad_values) * 1.3]),
                        font=dict(family="Epilogue", color="#2c3e50"),
                        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                        showlegend=False, margin=dict(l=20, r=60, t=20, b=20)
                    )
                    st.plotly_chart(fig_acad, use_container_width=True)
                with col2:
                    st.markdown("### Summary")
                    total_acad = sum(acad_values)
                    for label, val in academic_data.items():
                        pct = round(val / total_acad * 100)
                        st.metric(label=label, value=f"{val}", delta=f"{pct}% of cohort")
                        
    
    st.markdown(f"""
    <div class="info-box">
        <h3>📋 About This Session</h3>
        <p>
            This <strong>{selected_session}</strong> session is part of the 
            <strong>{initiative_info['name']}</strong> initiative, 
            designed to deepen participants' understanding of the {selected_session} sector landscape, 
            its role in <strong>Vision 2030</strong>, and the skills and job market opportunities 
            it presents. Survey data was collected before and after the session to measure 
            knowledge growth across four core topic areas: {', '.join(topics)}.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    #st.markdown("""
    #<div class="info-box">
       # <h3>📋 About This Session</h3>
       # <p>
        #    This Health Sector session is part of the <strong>Towards the Vision</strong> initiative, 
         #   designed to deepen participants' understanding of Saudi Arabia's health sector landscape, 
         #   its role in <strong>Vision 2030</strong>, and the skills and job market opportunities 
         #   it presents. Survey data was collected before and after the session to measure 
         #   knowledge growth across four core topic areas: Health Sector Knowledge, Vision 2030 
         #   Contribution, Job Market Awareness, and In-Demand Skills.
       # </p>
    #</div>
   # """, unsafe_allow_html=True)
    st.markdown(f"""
    <div class='sls-footer'>
        <h2>{session_info['icon']} {selected_session}</h2>
        <p class="tagline">{initiative_info['name']} • Australia Chapter</p>
        <div style='display: flex; justify-content: center; gap: 3rem; margin: 2rem 0; flex-wrap: wrap; position: relative; z-index: 1;'>
            <div>
                <div style='font-size: 2.5rem; font-weight: 700;'>{metrics['total_participants_pre']}</div>
                <div style='opacity: 0.8;'>Participants</div>
            </div>
            <div>
                <div style='font-size: 2.5rem; font-weight: 700;'>{metrics['total_responses']}</div>
                <div style='opacity: 0.8;'>Matched Surveys</div>
            </div>
            <div>
                <div style='font-size: 2.5rem; font-weight: 700;'>{improved_pct:.0f}%</div>
                <div style='opacity: 0.8;'>Showed Growth</div>
            </div>
            <div>
                <div style='font-size: 2.5rem; font-weight: 700;'>{avg_post:.2f}/5</div>
                <div style='opacity: 0.8;'>Avg Post-Score</div>
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

    st.stop()

# ============================================================================
# AWARENESS DASHBOARD
# ============================================================================

if session_info.get('type') == 'awareness':
    
    metrics = data['metrics']
    viz_data = data['visualization_data']
    
    st.markdown('<p class="section-title">📊 Awareness Impact</p>', unsafe_allow_html=True)
    
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
    
    st.markdown('<p class="section-title">🔄 Before vs After Comparison</p>', unsafe_allow_html=True)
    
    levels = viz_data['awareness_comparison']['levels']
    pre_scores_aw = viz_data['awareness_comparison']['pre']
    post_scores_aw = viz_data['awareness_comparison']['post']
    
    fig_compare = go.Figure()
    
    fig_compare.add_trace(go.Bar(
        name='Before Session',
        x=levels,
        y=pre_scores_aw,
        marker_color='#e9ecef',
        text=[f"{s:.1f}%" for s in pre_scores_aw],
        textposition='outside'
    ))
    
    fig_compare.add_trace(go.Bar(
        name='After Session',
        x=levels,
        y=post_scores_aw,
        marker_color='#006341',
        text=[f"{s:.1f}%" for s in post_scores_aw],
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
            <strong>Grow • Connect • Impact</strong>
        </p>
        <p style='font-size: 0.9rem; opacity: 0.7; margin-top: 1rem; position: relative; z-index: 1;'>
            {datetime.now().strftime('%B %d, %Y')} | Misk Tracks
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.stop()

# ============================================================================
# COMPREHENSIVE DASHBOARD (10x Leaders with Overall/Paired Analysis)
# ============================================================================

if session_info.get('type') == 'comprehensive':
    metrics = data['metrics']
    
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
    
    st.markdown('<p class="section-title">📊 Analysis Methodology</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-box">
            <h3>Overall Analysis</h3>
            <p style="font-size: 1.05rem; line-height: 1.8;">
            Compares <strong>all pre-survey respondents</strong> ({pre}) with 
            <strong>all post-survey respondents</strong> ({post}). 
            Shows the population-level change in awareness.
            </p>
            <p style="font-size: 1.05rem; line-height: 1.8; margin-top: 1rem;">
            <strong>Result:</strong> {before:.1f}% → {after:.1f}% 
            (+{increase:.1f} points)
            </p>
        </div>
        """.format(
            pre=TOTAL_PRE, post=TOTAL_POST,
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
            Shows true within-person change by comparing the same individuals before and after.
            </p>
            <p style="font-size: 1.05rem; line-height: 1.8; margin-top: 1rem;">
            <strong>Result:</strong> {before:.1f}% → {after:.1f}% 
            (+{increase:.1f} points)
            </p>
        </div>
        """.format(
            matched=MATCHED,
            before=awareness_analysis.get('paired_pre_pct', 0),
            after=awareness_analysis.get('paired_post_pct', 0),
            increase=paired_increase
        ), unsafe_allow_html=True)
    
    st.markdown('<p class="section-title">📈 Awareness Growth Comparison</p>', unsafe_allow_html=True)
    
    fig_awareness = go.Figure()
    
    categories = ['Overall (All Respondents)', 'Paired (Matched Participants)']
    pre_values = [awareness_analysis.get('overall_pre_pct', 0), awareness_analysis.get('paired_pre_pct', 0)]
    post_values = [awareness_analysis.get('overall_post_pct', 0), awareness_analysis.get('paired_post_pct', 0)]
    
    fig_awareness.add_trace(go.Bar(
        name='Before Session', x=categories, y=pre_values,
        marker_color='#e9ecef',
        text=[f"{v:.1f}%" for v in pre_values], textposition='outside', textfont=dict(size=14)
    ))
    
    fig_awareness.add_trace(go.Bar(
        name='After Session', x=categories, y=post_values,
        marker_color='#006341',
        text=[f"{v:.1f}%" for v in post_values], textposition='outside', textfont=dict(size=14)
    ))
    
    fig_awareness.update_layout(
        barmode='group', yaxis_title='Awareness Percentage', yaxis=dict(range=[0, 100]),
        height=450, font=dict(family="Epilogue", color="#2c3e50"),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    
    st.plotly_chart(fig_awareness, use_container_width=True)
    
    st.markdown('<p class="section-title">👥 Participant Demographics</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Locations")
        location_data = demographics.get('location', {})
        if location_data:
            fig_loc = go.Figure(data=[go.Pie(
                labels=list(location_data.keys()), values=list(location_data.values()),
                hole=0.4, marker_colors=['#006341', '#00843d', '#93c13f', '#b8d96d', '#d4e89e', '#e9f5c9'],
                textfont=dict(size=14)
            )])
            fig_loc.update_layout(height=400, showlegend=True, paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02))
            st.plotly_chart(fig_loc, use_container_width=True)
    
    with col2:
        st.markdown("### How They Heard About Us")
        heard_data = demographics.get('heard_about', {})
        if heard_data:
            fig_heard = go.Figure(data=[go.Bar(
                x=list(heard_data.keys()), y=list(heard_data.values()),
                marker_color='#006341', text=list(heard_data.values()), textposition='outside',
                textfont=dict(size=14)
            )])
            fig_heard.update_layout(height=400, yaxis_title='Number of Participants',
                font=dict(family="Epilogue", color="#2c3e50"),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
            st.plotly_chart(fig_heard, use_container_width=True)
    
    st.markdown('<p class="section-title">⭐ Satisfaction Distribution</p>', unsafe_allow_html=True)
    
    sat_dist = satisfaction.get('distribution', {})
    if sat_dist:
        col1, col2 = st.columns([2, 1])
        with col1:
            labels = [f"{k} Stars" for k in sorted(sat_dist.keys())]
            values = [sat_dist[k] for k in sorted(sat_dist.keys())]
            colors = ['#93c13f' if int(k) >= 4 else '#f39c12' for k in sorted(sat_dist.keys())]
            fig_sat = go.Figure(data=[go.Bar(
                x=labels, y=values, marker_color=colors,
                text=values, textposition='outside', textfont=dict(size=16)
            )])
            fig_sat.update_layout(height=350, yaxis_title='Number of Participants',
                font=dict(family="Epilogue", color="#2c3e50"),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
            st.plotly_chart(fig_sat, use_container_width=True)
        with col2:
            st.markdown("### Summary")
            st.metric("Average Rating", f"{satisfaction.get('average_score', 0):.2f}/5.0")
            st.metric("Highly Satisfied", f"{satisfaction.get('satisfied_pct', 0):.0f}%")
            st.metric("Total Responses", TOTAL_POST)
    
    st.markdown(f"""
    <div class='sls-footer'>
        <h2>10x Leaders Program</h2>
        <p class="tagline">Misk Tracks • Australia Chapter</p>
        <div style='display: flex; justify-content: center; gap: 3rem; margin: 2rem 0; flex-wrap: wrap; position: relative; z-index: 1;'>
            <div><div style='font-size: 2.5rem; font-weight: 700;'>{ACTUAL_ATTENDEES}</div><div style='opacity: 0.8;'>Participants</div></div>
            <div><div style='font-size: 2.5rem; font-weight: 700;'>+{paired_increase:.1f}%</div><div style='opacity: 0.8;'>Awareness Growth</div></div>
            <div><div style='font-size: 2.5rem; font-weight: 700;'>{satisfaction.get('average_score', 0):.2f}/5</div><div style='opacity: 0.8;'>Satisfaction</div></div>
        </div>
        <p style='font-size: 1.1rem; margin-top: 2rem; opacity: 0.9; position: relative; z-index: 1;'><strong>Grow • Connect • Impact</strong></p>
        <p style='font-size: 0.9rem; opacity: 0.7; margin-top: 1rem; position: relative; z-index: 1;'>{datetime.now().strftime('%B %d, %Y')} | 10x Leaders</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.stop()

# ============================================================================
# STANDARD SESSION DASHBOARD (Cybersecurity, Finance)
# ============================================================================

metrics = data['metrics']
viz_data = data.get('visualization_data', {})
chapter_metrics = metrics.get('chapter_metrics', {})

REGISTERED = chapter_metrics.get('total_registered', 0)
TARGET = chapter_metrics.get('target_attendance', 50)
ACTUAL_ATTENDEES = chapter_metrics.get('actual_attendees', 0)

st.markdown('<p class="section-title">📊 Key Performance Indicators</p>', unsafe_allow_html=True)

st.markdown('<p class="subsection-title">Reach & Participation</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    attendance_rate = (ACTUAL_ATTENDEES / REGISTERED * 100) if REGISTERED > 0 else 0
    st.markdown(
        create_kpi_card("REACH", "Total Participants", f"{ACTUAL_ATTENDEES}",
            f"Out of {REGISTERED} registered", f"✓ {attendance_rate:.0f}% attendance rate"),
        unsafe_allow_html=True)

with col2:
    survey_completion = (metrics['total_responses'] / ACTUAL_ATTENDEES * 100) if ACTUAL_ATTENDEES > 0 else 0
    st.markdown(
        create_kpi_card("ENGAGEMENT", "Completed Both Surveys", f"{metrics['total_responses']}",
            f"Out of {ACTUAL_ATTENDEES} participants",
            "✓ High engagement" if survey_completion >= 50 else "→ Can improve"),
        unsafe_allow_html=True)

with col3:
    target_performance = (ACTUAL_ATTENDEES / TARGET * 100) if TARGET > 0 else 0
    st.markdown(
        create_kpi_card("TARGET", "Goal Achievement", f"{target_performance:.0f}%",
            f"Target was {TARGET} participants",
            f"✓ Exceeded target" if ACTUAL_ATTENDEES > TARGET else "→ Approaching target"),
        unsafe_allow_html=True)

st.markdown('<p class="subsection-title">Learning Effectiveness</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    avg_growth = metrics.get('grow_avg_knowledge_increase', 0)
    st.markdown(
        create_kpi_card("KNOWLEDGE", "Average Growth", f"+{avg_growth:.2f}",
            "Points improvement (1-5 scale)",
            f"✓ Strong growth" if avg_growth >= 1.0 else "→ Moderate growth"),
        unsafe_allow_html=True)

with col2:
    improved_pct = metrics.get('grow_members_reporting_growth_pct', 0)
    st.markdown(
        create_kpi_card("LEARNING", "Participants Improved", f"{improved_pct:.0f}%",
            "Showed knowledge gain",
            f"✓ Excellent reach" if improved_pct >= 70 else "→ Good reach"),
        unsafe_allow_html=True)

with col3:
    significant_pct = metrics.get('grow_significant_growth_pct', 0)
    st.markdown(
        create_kpi_card("IMPACT", "Significant Growth", f"{significant_pct:.0f}%",
            "Gained ≥0.5 points",
            f"✓ Deep learning" if significant_pct >= 50 else "→ Solid progress"),
        unsafe_allow_html=True)

st.markdown('<p class="subsection-title">Action & Satisfaction</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    action_pct = metrics.get('connect_members_planning_action_pct', 0)
    action_count = metrics.get('connect_total_planning_action', 0)
    st.markdown(
        create_kpi_card("COMMITMENT", "Plan to Take Action", f"{action_pct:.0f}%",
            f"{action_count} participants committed",
            f"✓ Outstanding" if action_pct >= 80 else "✓ Strong" if action_pct >= 60 else "→ Growing"),
        unsafe_allow_html=True)

with col2:
    satisfaction = metrics.get('impact_avg_satisfaction', 0)
    st.markdown(
        create_kpi_card("QUALITY", "Satisfaction Score", f"{satisfaction:.2f}/5.0",
            "Average participant rating",
            f"✓ Excellent" if satisfaction >= 4.5 else "✓ Very good" if satisfaction >= 4.0 else "→ Good"),
        unsafe_allow_html=True)

with col3:
    satisfied_pct = metrics.get('impact_satisfaction_pct', 0)
    st.markdown(
        create_kpi_card("SATISFACTION", "Highly Satisfied", f"{satisfied_pct:.0f}%",
            "Rated 4+ stars",
            f"✓ Strong approval" if satisfied_pct >= 70 else "→ Positive reception"),
        unsafe_allow_html=True)

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

st.markdown('<p class="section-title">🎓 Participant Journey</p>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    funnel_fig = go.Figure()
    funnel_fig.add_trace(go.Funnel(
        y=['Registered', 'Attended', 'Completed Both Surveys', 'Plan to Act'],
        x=[REGISTERED, ACTUAL_ATTENDEES, metrics['total_responses'], metrics.get('connect_total_planning_action', 0)],
        textposition="inside", textinfo="value+percent initial",
        marker={"color": ['#006341', '#00843d', '#93c13f', '#b8d96d'], "line": {"width": 2, "color": "white"}}
    ))
    funnel_fig.update_layout(height=400, font=dict(family="Epilogue", size=14, color="#2c3e50"),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(funnel_fig, use_container_width=True)

with col2:
    st.markdown("### Conversion Metrics")
    reg_to_attend   = (ACTUAL_ATTENDEES / REGISTERED * 100) if REGISTERED > 0 else 0
    attend_to_survey = (metrics['total_responses'] / ACTUAL_ATTENDEES * 100) if ACTUAL_ATTENDEES > 0 else 0
    survey_to_action = (metrics.get('connect_total_planning_action', 0) / metrics['total_responses'] * 100) if metrics['total_responses'] > 0 else 0
    st.metric("Registered → Attended", f"{reg_to_attend:.0f}%")
    st.metric("Attended → Surveyed", f"{attend_to_survey:.0f}%")
    st.metric("Surveyed → Committed", f"{survey_to_action:.0f}%")
    st.markdown("---")
    overall = (metrics.get('connect_total_planning_action', 0) / REGISTERED * 100) if REGISTERED > 0 else 0
    st.info(f"**Overall:** {overall:.0f}% of registrants became committed participants")

st.markdown("---")
st.markdown('<p class="section-title">📚 Detailed Analysis</p>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🌱 Knowledge Development", "🤝 Commitment", "💡 Satisfaction"])

with tab1:
    st.markdown("### Learning Progress")
    col1, col2 = st.columns([3, 2])
    with col1:
        topics = session_info['topic_labels']
        pre_scores  = viz_data['knowledge_comparison']['pre_scores']
        post_scores = viz_data['knowledge_comparison']['post_scores']
        improvements = viz_data['knowledge_comparison']['improvements']
        
        knowledge_fig = go.Figure()
        knowledge_fig.add_trace(go.Bar(name='Before Session', x=topics, y=pre_scores,
            marker_color='#e9ecef', text=[f"{s:.2f}" for s in pre_scores], textposition='outside'))
        knowledge_fig.add_trace(go.Bar(name='After Session', x=topics, y=post_scores,
            marker_color='#006341', text=[f"{s:.2f}" for s in post_scores], textposition='outside'))
        knowledge_fig.update_layout(barmode='group', yaxis_title='Knowledge Level (1-5)',
            yaxis=dict(range=[0, 6]), height=400, font=dict(family="Epilogue", color="#2c3e50"),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5))
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
        committed_count = metrics.get('connect_total_planning_action', 0)
        action_fig = go.Figure(data=[go.Pie(
            labels=labels, values=values, hole=0.6,
            marker_colors=['#006341', '#e9ecef'], textfont=dict(size=16, family='Epilogue')
        )])
        action_fig.update_layout(height=350, showlegend=True,
            annotations=[dict(text=f"<b>{committed_count}</b><br>Committed",
                x=0.5, y=0.5, font=dict(size=20, family='Cormorant Garamond'), showarrow=False)],
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5))
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
            sorted_items = sorted(satisfaction_data.items(),
                key=lambda x: satisfaction_order.index(x[0]) if x[0] in satisfaction_order else 2)
            labels = [item[0] for item in sorted_items]
            values = [item[1] for item in sorted_items]
            colors = ['#e74c3c', '#e67e22', '#f39c12', '#93c13f', '#006341'][:len(labels)]
            sat_fig = go.Figure(data=[go.Bar(
                y=labels, x=values, orientation='h', marker_color=colors,
                text=values, textposition='outside', textfont=dict(size=14)
            )])
            sat_fig.update_layout(xaxis_title='Number of Participants', height=350,
                font=dict(family="Epilogue", color="#2c3e50"),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
            st.plotly_chart(sat_fig, use_container_width=True)
    with col2:
        st.markdown("### Metrics")
        st.metric("Average Rating", f"{metrics.get('impact_avg_satisfaction', 0):.2f}/5.0")
        st.metric("Highly Satisfied", f"{metrics.get('impact_satisfaction_pct', 0):.0f}%")
        st.metric("Likely to Recommend", f"{metrics.get('impact_likely_recommend_pct', 0):.1f}%")

st.markdown(f"""
<div class='sls-footer'>
    <h2>Saudi Leadership Society</h2>
    <p class="tagline">Towards the Vision • Australia Chapter</p>
    <div style='display: flex; justify-content: center; gap: 3rem; margin: 2rem 0; flex-wrap: wrap; position: relative; z-index: 1;'>
        <div><div style='font-size: 2.5rem; font-weight: 700;'>{ACTUAL_ATTENDEES}</div><div style='opacity: 0.8;'>Participants</div></div>
        <div><div style='font-size: 2.5rem; font-weight: 700;'>+{metrics.get('grow_avg_knowledge_increase', 0):.2f}</div><div style='opacity: 0.8;'>Avg Growth</div></div>
        <div><div style='font-size: 2.5rem; font-weight: 700;'>{metrics.get('connect_total_planning_action', 0)}</div><div style='opacity: 0.8;'>Taking Action</div></div>
    </div>
    <p style='font-size: 1.1rem; margin-top: 2rem; opacity: 0.9; position: relative; z-index: 1;'><strong>Grow • Connect • Impact</strong></p>
    <p style='font-size: 0.9rem; opacity: 0.7; margin-top: 1rem; position: relative; z-index: 1;'>{datetime.now().strftime('%B %d, %Y')} | Vision 2030</p>
</div>
""", unsafe_allow_html=True)
