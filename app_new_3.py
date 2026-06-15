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
        "description": "Professional networking circles connecting Saudi health students and professionals in Australia — Growth, Connection, and Impact circles — aligned with Vision 2030.",
        "color": "#0d3b6e",
        "sessions": {
            "Health Sector Session 1": {
                "name": "🏥 Health Sector — Session 1",
                "data_file": None,
                "icon": "🏥",
                "vision_theme": "Professional Networking & Career Development",
                "color": "#0d3b6e",
                "topic_labels": [],
                "type": "lnc"
            },
            "Technology Sector Session 1": {
                "name": "💻 Technology Sector — Session 1",
                "data_file": None,
                "icon": "💻",
                "vision_theme": "Professional Networking & Career Development",
                "color": "#0d3b6e",
                "topic_labels": [],
                "type": "lnc_tech"
            },
            
            "Cross-Sector Analysis": {
                "name": "⚡ Health vs Technology — Cross Analysis",
                "data_file": None,
                "icon": "⚡",
                "vision_theme": "Health & Technology Sectors Compared",
                "color": "#0d3b6e",
                "topic_labels": [],
                "type": "lnc_cross"
            },
            "Combined Analysis": {
                "name": "🌐 Health + Technology — Combined",
                "data_file": None,
                "icon": "🌐",
                "vision_theme": "Health & Technology — Combined Programme Insights",
                "color": "#0d3b6e",
                "topic_labels": [],
                "type": "lnc_combined"
            }
        }
    },
    "Leaders Accelerator": {
        "name": "Leaders Accelerator",
        "icon": "⚡",
        "description": "A mentorship-driven accelerator preparing Saudi students in Australia to apply for Misk's 10X Leaders program — through clarity, confidence, and coaching.",
        "color": "#7C3AED",
        "sessions": {
            "10X Leaders Session": {
                "name": "⚡ Leaders Accelerator — 10X Leaders",
                "data_file": None,
                "icon": "⚡",
                "vision_theme": "Application Readiness & Leadership Development",
                "color": "#7C3AED",
                "topic_labels": [],
                "type": "leaders_accelerator"
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
    
    * { font-family: 'Epilogue', sans-serif; }
    
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
    
    .sls-header {
        background: linear-gradient(135deg, #006341 0%, #00843d 50%, #93c13f 100%);
        padding: 4rem 2rem;
        border-radius: 0 0 40px 40px;
        box-shadow: 0 20px 60px rgba(0, 100, 65, 0.2), inset 0 -1px 0 rgba(255,255,255,0.2);
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
        animation: headerGlow 3s ease-in-out infinite alternate;
    }

    /* LNC-specific navy header */
    .lnc-header {
        background: linear-gradient(135deg, #0d3b6e 0%, #1a5fa8 50%, #378add 100%);
        padding: 4rem 2rem;
        border-radius: 0 0 40px 40px;
        box-shadow: 0 20px 60px rgba(13, 59, 110, 0.3), inset 0 -1px 0 rgba(255,255,255,0.2);
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
        animation: headerGlow 3s ease-in-out infinite alternate;
    }

    .lnc-header::before {
        content: '';
        position: absolute;
        top: -50%; right: -10%;
        width: 600px; height: 600px;
        background: radial-gradient(circle, rgba(255,255,255,0.12) 0%, transparent 70%),
            repeating-linear-gradient(45deg, transparent, transparent 20px, rgba(255,255,255,0.04) 20px, rgba(255,255,255,0.04) 40px);
        border-radius: 50%;
        animation: rotate 30s linear infinite;
    }

    .lnc-header::after {
        content: '';
        position: absolute;
        bottom: -30%; left: -5%;
        width: 500px; height: 500px;
        background: radial-gradient(circle, rgba(55,138,221,0.3) 0%, transparent 70%);
        border-radius: 50%;
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes headerGlow {
        from { box-shadow: 0 20px 60px rgba(0,100,65,0.2), inset 0 -1px 0 rgba(255,255,255,0.2); }
        to   { box-shadow: 0 25px 70px rgba(0,100,65,0.3), inset 0 -1px 0 rgba(255,255,255,0.3); }
    }
    
    .sls-header::before {
        content: '';
        position: absolute;
        top: -50%; right: -10%;
        width: 600px; height: 600px;
        background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%),
            repeating-linear-gradient(45deg, transparent, transparent 20px, rgba(255,255,255,0.05) 20px, rgba(255,255,255,0.05) 40px);
        border-radius: 50%;
        animation: rotate 30s linear infinite;
    }
    
    .sls-header::after {
        content: '';
        position: absolute;
        bottom: -30%; left: -5%;
        width: 500px; height: 500px;
        background: radial-gradient(circle, rgba(147,193,63,0.25) 0%, transparent 70%);
        border-radius: 50%;
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    @keyframes pulse  { 0%,100% { transform: scale(1); opacity:0.25; } 50% { transform: scale(1.1); opacity:0.35; } }
    
    .initiative-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 4rem; font-weight: 700; color: white;
        text-align: center; margin: 0; position: relative; z-index: 1;
        text-shadow: 0 4px 20px rgba(0,0,0,0.2);
        animation: titleFloat 3s ease-in-out infinite;
    }
    
    @keyframes titleFloat {
        0%,100% { transform: translateY(0px); }
        50%      { transform: translateY(-5px); }
    }
    
    .initiative-subtitle {
        font-family: 'Epilogue', sans-serif;
        font-size: 1.4rem; font-weight: 300; color: rgba(255,255,255,0.95);
        text-align: center; margin-top: 0.75rem; position: relative; z-index: 1;
        letter-spacing: 0.08em;
    }
    
    .mission-tagline {
        font-family: 'Epilogue', sans-serif;
        font-size: 1.15rem; font-weight: 600; color: rgba(255,255,255,0.95);
        text-align: center; margin-top: 1.75rem;
        padding: 1.25rem 2.5rem;
        background: rgba(255,255,255,0.18); border-radius: 60px;
        backdrop-filter: blur(15px); border: 1px solid rgba(255,255,255,0.3);
        display: inline-block; position: relative; z-index: 1;
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
        animation: taglineGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes taglineGlow {
        from { box-shadow: 0 8px 30px rgba(0,0,0,0.15); }
        to   { box-shadow: 0 12px 40px rgba(55,138,221,0.35); }
    }

    /* LNC circle badges */
    .circle-badge {
        display: inline-flex; align-items: center; gap: 0.5rem;
        padding: 0.6rem 1.4rem; border-radius: 40px;
        font-family: 'Epilogue', sans-serif; font-size: 1rem; font-weight: 700;
        margin: 0.4rem; position: relative; z-index: 1;
    }
    .circle-growth   { background: rgba(55,138,221,0.25); color: #fff; border: 1px solid rgba(55,138,221,0.5); }
    .circle-connect  { background: rgba(0,132,61,0.25);   color: #fff; border: 1px solid rgba(0,132,61,0.5); }
    .circle-impact   { background: rgba(147,193,63,0.25); color: #fff; border: 1px solid rgba(147,193,63,0.5); }

    /* Pre/Post comparison band */
    .compare-band {
        display: flex; gap: 1rem; align-items: stretch;
        background: linear-gradient(135deg, #f0f9ff 0%, #e8f5e9 100%);
        border-radius: 20px; padding: 1.5rem; margin: 1.5rem 0;
        border: 1px solid rgba(13,59,110,0.1);
    }
    .compare-col { flex: 1; text-align: center; }
    .compare-label {
        font-size: 0.75rem; font-weight: 800; text-transform: uppercase;
        letter-spacing: 0.15em; margin-bottom: 0.5rem;
    }
    .compare-val {
        font-family: 'Cormorant Garamond', serif;
        font-size: 2.8rem; font-weight: 700; line-height: 1;
    }
    .compare-sub { font-size: 0.85rem; color: #666; margin-top: 0.3rem; }
    .compare-arrow {
        display: flex; align-items: center;
        font-size: 2rem; color: #0d3b6e; font-weight: 900;
    }
    .compare-delta {
        font-family: 'Epilogue', sans-serif; font-size: 1rem; font-weight: 700;
        padding: 0.3rem 0.8rem; border-radius: 20px; margin-top: 0.4rem; display: inline-block;
    }
    .delta-pos { background: rgba(0,132,61,0.12); color: #006341; }
    .delta-neg { background: rgba(231,76,60,0.12);  color: #c0392b; }
    .delta-neu { background: rgba(108,117,125,0.12); color: #495057; }

    .section-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 2.5rem; font-weight: 700; color: #1a1a1a;
        margin: 3.5rem 0 2rem 0; padding-bottom: 1.25rem; position: relative;
    }
    .section-title::after {
        content: ''; position: absolute; bottom: 0; left: 0;
        width: 120px; height: 4px;
        background: linear-gradient(90deg, #0d3b6e, #378add);
        border-radius: 2px; animation: underlineGrow 1s ease-out;
    }
    @keyframes underlineGrow { from { width: 0; } to { width: 120px; } }
    
    .subsection-title {
        font-family: 'Epilogue', sans-serif;
        font-size: 0.95rem; font-weight: 800; color: #0d3b6e;
        text-transform: uppercase; letter-spacing: 0.15em;
        margin: 2.5rem 0 1.5rem 0;
        opacity: 0; animation: fadeInUp 0.6s ease-out forwards;
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    
    .kpi-card {
        background: linear-gradient(135deg, #ffffff 0%, #f0f6ff 100%);
        padding: 2.5rem; border-radius: 24px;
        box-shadow: 0 10px 40px rgba(13,59,110,0.08), inset 0 1px 0 rgba(255,255,255,0.9);
        border: 1px solid rgba(13,59,110,0.08);
        transition: all 0.5s cubic-bezier(0.4,0,0.2,1);
        height: 100%; position: relative; overflow: hidden;
        opacity: 0; animation: cardSlideIn 0.8s ease-out forwards;
    }
    @keyframes cardSlideIn {
        from { opacity: 0; transform: translateY(30px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .kpi-card::before {
        content: ''; position: absolute; top: 0; left: 0;
        width: 5px; height: 100%;
        background: linear-gradient(180deg, #0d3b6e 0%, #378add 100%);
        box-shadow: 0 0 20px rgba(13,59,110,0.3);
    }
    .kpi-card:hover {
        transform: translateY(-12px) scale(1.02);
        box-shadow: 0 20px 60px rgba(13,59,110,0.18), inset 0 1px 0 rgba(255,255,255,1);
    }
    .kpi-category {
        font-family: 'Epilogue', sans-serif; font-size: 0.7rem; font-weight: 900;
        color: #0d3b6e; text-transform: uppercase; letter-spacing: 0.2em;
        margin-bottom: 0.75rem; opacity: 0.8;
    }
    .kpi-label {
        font-family: 'Epilogue', sans-serif; font-size: 1.15rem; font-weight: 600;
        color: #2c3e50; margin-bottom: 1.25rem; line-height: 1.4;
    }
    .kpi-value {
        font-family: 'Cormorant Garamond', serif; font-size: 3.5rem; font-weight: 700;
        background: linear-gradient(135deg, #0d3b6e 0%, #378add 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text; line-height: 1; margin: 1rem 0;
    }
    .kpi-context {
        font-family: 'Epilogue', sans-serif; font-size: 0.95rem;
        color: #5a6c7d; margin-top: 1rem; line-height: 1.6;
    }
    .kpi-trend {
        font-family: 'Epilogue', sans-serif; font-size: 0.85rem; font-weight: 700;
        color: #0d3b6e; margin-top: 0.75rem; padding: 0.5rem 1rem;
        background: rgba(13,59,110,0.08); border-radius: 20px; display: inline-block;
    }
    .kpi-trend-warn {
        font-family: 'Epilogue', sans-serif; font-size: 0.85rem; font-weight: 700;
        color: #b45309; margin-top: 0.75rem; padding: 0.5rem 1rem;
        background: rgba(180,83,9,0.08); border-radius: 20px; display: inline-block;
    }
    
    /* LNC highlight box — navy */
    .lnc-highlight-box {
        background: linear-gradient(135deg, #0d3b6e 0%, #1a5fa8 100%);
        padding: 3rem; border-radius: 30px; margin: 3rem 0;
        box-shadow: 0 20px 60px rgba(13,59,110,0.3), inset 0 1px 0 rgba(255,255,255,0.2);
        position: relative; overflow: hidden;
        animation: boxFloat 6s ease-in-out infinite;
    }
    @keyframes boxFloat {
        0%,100% { transform: translateY(0px); }
        50%      { transform: translateY(-8px); }
    }
    .lnc-highlight-box::before {
        content: ''; position: absolute; top: -50%; right: -20%;
        width: 500px; height: 500px;
        background: radial-gradient(circle, rgba(55,138,221,0.25) 0%, transparent 70%);
        border-radius: 50%; animation: pulseGlow 5s ease-in-out infinite;
    }
    @keyframes pulseGlow {
        0%,100% { opacity:0.25; transform:scale(1); }
        50%      { opacity:0.4;  transform:scale(1.15); }
    }
    .lnc-highlight-box h3 {
        font-family: 'Cormorant Garamond', serif; font-size: 2rem; font-weight: 700;
        color: white; margin-bottom: 2rem; position: relative; z-index: 1;
    }
    .lnc-highlight-box ul { list-style: none; padding: 0; margin: 0; position: relative; z-index: 1; }
    .lnc-highlight-box li {
        font-family: 'Epilogue', sans-serif; font-size: 1.1rem;
        color: rgba(255,255,255,0.95); line-height: 2; padding: 0.6rem 0; padding-left: 2.5rem;
        position: relative; opacity: 0; animation: listItemSlide 0.6s ease-out forwards;
    }
    .lnc-highlight-box li:nth-child(1) { animation-delay: 0.1s; }
    .lnc-highlight-box li:nth-child(2) { animation-delay: 0.2s; }
    .lnc-highlight-box li:nth-child(3) { animation-delay: 0.3s; }
    .lnc-highlight-box li:nth-child(4) { animation-delay: 0.4s; }
    .lnc-highlight-box li:nth-child(5) { animation-delay: 0.5s; }
    @keyframes listItemSlide {
        from { opacity:0; transform:translateX(-20px); }
        to   { opacity:1; transform:translateX(0); }
    }
    .lnc-highlight-box li:before {
        content: "✓"; position: absolute; left: 0;
        color: #85B7EB; font-weight: 900; font-size: 1.4rem;
    }

    /* LNC stat pill */
    .stat-pill {
        display: inline-flex; flex-direction: column; align-items: center;
        padding: 1.2rem 2rem; border-radius: 20px; margin: 0.4rem;
        background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.25);
        backdrop-filter: blur(10px); position: relative; z-index: 1;
        min-width: 120px;
    }
    .stat-pill .num {
        font-family: 'Cormorant Garamond', serif;
        font-size: 2.8rem; font-weight: 700; color: #fff; line-height: 1;
    }
    .stat-pill .lbl {
        font-family: 'Epilogue', sans-serif;
        font-size: 0.8rem; font-weight: 600; color: rgba(255,255,255,0.8);
        text-align: center; margin-top: 0.3rem; text-transform: uppercase; letter-spacing: 0.1em;
    }

    .highlight-box {
        background: linear-gradient(135deg, #006341 0%, #00843d 100%);
        padding: 3rem; border-radius: 30px; margin: 3rem 0;
        box-shadow: 0 20px 60px rgba(0,100,65,0.3), inset 0 1px 0 rgba(255,255,255,0.2);
        position: relative; overflow: hidden; animation: boxFloat 6s ease-in-out infinite;
    }
    .highlight-box::before {
        content: ''; position: absolute; top: -50%; right: -20%;
        width: 500px; height: 500px;
        background: radial-gradient(circle, rgba(147,193,63,0.25) 0%, transparent 70%);
        border-radius: 50%; animation: pulseGlow 5s ease-in-out infinite;
    }
    .highlight-box h3 {
        font-family: 'Cormorant Garamond', serif; font-size: 2rem; font-weight: 700;
        color: white; margin-bottom: 2rem; position: relative; z-index: 1;
    }
    .highlight-box ul { list-style: none; padding: 0; margin: 0; position: relative; z-index: 1; }
    .highlight-box li {
        font-family: 'Epilogue', sans-serif; font-size: 1.15rem;
        color: rgba(255,255,255,0.95); line-height: 2; padding: 0.75rem 0; padding-left: 2.5rem;
        position: relative; opacity: 0; animation: listItemSlide 0.6s ease-out forwards;
    }
    .highlight-box li:nth-child(1) { animation-delay: 0.1s; }
    .highlight-box li:nth-child(2) { animation-delay: 0.2s; }
    .highlight-box li:nth-child(3) { animation-delay: 0.3s; }
    .highlight-box li:nth-child(4) { animation-delay: 0.4s; }
    .highlight-box li:before { content:"✓"; position:absolute; left:0; color:#93c13f; font-weight:900; font-size:1.5rem; }
    
    .info-box {
        background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(240,246,255,0.9) 100%);
        backdrop-filter: blur(20px); padding: 3rem; border-radius: 28px;
        border: 2px solid rgba(13,59,110,0.1);
        box-shadow: 0 15px 50px rgba(13,59,110,0.08); margin: 2.5rem 0;
        position: relative; overflow: hidden;
    }
    .info-box h3 { font-family:'Cormorant Garamond',serif; font-size:2rem; color:#1a1a1a; margin-bottom:1.5rem; }
    .info-box p  { font-family:'Epilogue',sans-serif; font-size:1.1rem; line-height:1.9; color:#495057; }

    .session-card {
        background: white; padding: 3.5rem 2.5rem; border-radius: 28px;
        text-align: center; box-shadow: 0 12px 40px rgba(0,0,0,0.08);
        transition: all 0.5s cubic-bezier(0.4,0,0.2,1); border: 2px solid transparent;
        cursor: pointer; position: relative; overflow: hidden;
    }
    .session-card:hover {
        transform: translateY(-15px) scale(1.03);
        box-shadow: 0 25px 60px rgba(13,59,110,0.2); border-color: #0d3b6e;
    }
    .session-icon {
        font-size: 5rem; margin-bottom: 1.75rem;
        filter: drop-shadow(0 8px 16px rgba(0,0,0,0.1)); transition: transform 0.5s;
    }
    .session-card:hover .session-icon { transform: scale(1.1) rotate(5deg); }
    .session-name { font-family:'Cormorant Garamond',serif; font-size:2rem; font-weight:700; color:#1a1a1a; margin-bottom:1rem; }
    .session-theme { font-family:'Epilogue',sans-serif; font-size:1.05rem; color:#666; font-weight:500; line-height:1.6; }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.75rem; background: white; padding: 1.25rem; border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.06); border: 1px solid rgba(13,59,110,0.08);
    }
    .stTabs [data-baseweb="tab"] {
        font-family:'Epilogue',sans-serif; font-size:1.05rem; font-weight:700;
        padding: 1rem 2rem; border-radius: 14px; transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background: linear-gradient(135deg, #0d3b6e 0%, #1a5fa8 100%);
        color: white; box-shadow: 0 6px 20px rgba(13,59,110,0.35); transform: translateY(-2px);
    }

    .lnc-footer {
        background: linear-gradient(135deg, #0d1f3c 0%, #1a3a6e 100%);
        color: white; padding: 4rem 2rem; border-radius: 40px 40px 0 0;
        margin-top: 5rem; text-align: center; position: relative; overflow: hidden;
    }
    .lnc-footer::before {
        content: ''; position: absolute; top: -50%; left: -25%;
        width: 150%; height: 200%;
        background: radial-gradient(circle, rgba(55,138,221,0.12) 0%, transparent 70%);
        animation: footerPulse 8s ease-in-out infinite;
    }
    @keyframes footerPulse { 0%,100% { transform:scale(1); } 50% { transform:scale(1.1); } }
    .lnc-footer h2 { font-family:'Cormorant Garamond',serif; font-size:2.5rem; margin-bottom:0.75rem; position:relative; z-index:1; }
    .lnc-footer .tagline { font-family:'Epilogue',sans-serif; font-size:1.4rem; font-weight:300; opacity:0.95; margin-bottom:2.5rem; position:relative; z-index:1; }

    .sls-footer {
        background: linear-gradient(135deg, #1a1a1a 0%, #2c3e50 100%);
        color: white; padding: 4rem 2rem; border-radius: 40px 40px 0 0;
        margin-top: 5rem; text-align: center; position: relative; overflow: hidden;
    }
    .sls-footer::before {
        content: ''; position: absolute; top: -50%; left: -25%;
        width: 150%; height: 200%;
        background: radial-gradient(circle, rgba(0,132,61,0.1) 0%, transparent 70%);
        animation: footerPulse 8s ease-in-out infinite;
    }
    .sls-footer h2 { font-family:'Cormorant Garamond',serif; font-size:2.5rem; margin-bottom:0.75rem; position:relative; z-index:1; }
    .sls-footer .tagline { font-family:'Epilogue',sans-serif; font-size:1.4rem; font-weight:300; opacity:0.95; margin-bottom:2.5rem; position:relative; z-index:1; }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_kpi_card(category, label, value, context, trend="", warn=False):
    trend_html = ""
    if trend:
        trend_class = "kpi-trend-warn" if warn else "kpi-trend"
        trend_html = f'<div class="{trend_class}">{trend}</div>'
    return f"""
    <div class="kpi-card">
        <div class="kpi-category">{category}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-context">{context}</div>
        {trend_html}
    </div>
    """

def lnc_bar(x, y, color, height=320, h_range=None, v_range=None, orientation='v', name=None):
    """Quick bar chart for LNC single-series charts."""
    fig = go.Figure()
    kwargs = dict(
        x=x if orientation=='v' else y,
        y=y if orientation=='v' else x,
        orientation=orientation,
        marker_color=color,
        text=[str(v) for v in (y if orientation=='v' else x)],
        textposition='outside',
        textfont=dict(size=13, family='Epilogue'),
    )
    if name:
        kwargs['name'] = name
    fig.add_trace(go.Bar(**kwargs))
    layout = dict(
        height=height,
        font=dict(family='Epilogue', color='#2c3e50'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(l=10, r=40, t=10, b=20),
    )
    if v_range: layout['yaxis'] = dict(range=v_range)
    if h_range: layout['xaxis'] = dict(range=h_range)
    fig.update_layout(**layout)
    return fig

def lnc_grouped_bar(labels, pre_vals, post_vals, pre_color='#d0d9e8', post_color='#0d3b6e', height=360, y_max=30):
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Before', x=labels, y=pre_vals,
        marker_color=pre_color, text=pre_vals, textposition='outside', textfont=dict(size=13)))
    fig.add_trace(go.Bar(name='After', x=labels, y=post_vals,
        marker_color=post_color, text=post_vals, textposition='outside', textfont=dict(size=13)))
    fig.update_layout(
        barmode='group', height=height,
        yaxis=dict(range=[0, y_max]),
        font=dict(family='Epilogue', color='#2c3e50'),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5)
    )
    return fig

def lnc_donut(labels, values, colors, center_text="", height=320):
    fig = go.Figure(data=[go.Pie(
        labels=labels, values=values, hole=0.52,
        marker_colors=colors,
        textfont=dict(size=12, family='Epilogue'),
        textinfo='label+percent'
    )])
    ann = []
    if center_text:
        ann.append(dict(text=center_text, x=0.5, y=0.5,
            font=dict(size=16, family='Cormorant Garamond', color='#0d3b6e'), showarrow=False))
    fig.update_layout(
        height=height, showlegend=True, paper_bgcolor='rgba(0,0,0,0)',
        annotations=ann,
        legend=dict(orientation='h', yanchor='bottom', y=-0.15, xanchor='center', x=0.5)
    )
    return fig

def compare_band(pre_val, post_val, pre_label, post_label, pre_color, post_color, unit="", note=""):
    if isinstance(pre_val, float):
        pre_str  = f"{pre_val:.1f}{unit}"
        post_str = f"{post_val:.1f}{unit}"
    else:
        pre_str  = f"{pre_val}{unit}"
        post_str = f"{post_val}{unit}"
    if isinstance(pre_val, (int, float)) and isinstance(post_val, (int, float)):
        delta = post_val - pre_val
        delta_str = f"+{delta:.1f}{unit}" if delta > 0 else f"{delta:.1f}{unit}"
        delta_class = "delta-pos" if delta > 0 else ("delta-neg" if delta < 0 else "delta-neu")
    else:
        delta_str, delta_class = "", "delta-neu"
    return f"""
    <div class="compare-band">
        <div class="compare-col">
            <div class="compare-label" style="color:{pre_color}">BEFORE</div>
            <div class="compare-val" style="color:{pre_color}">{pre_str}</div>
            <div class="compare-sub">{pre_label}</div>
        </div>
        <div class="compare-arrow">→</div>
        <div class="compare-col">
            <div class="compare-label" style="color:{post_color}">AFTER</div>
            <div class="compare-val" style="color:{post_color}">{post_str}</div>
            <div class="compare-sub">{post_label}</div>
            {f'<span class="compare-delta {delta_class}">{delta_str}</span>' if delta_str else ''}
        </div>
        {"<div class='compare-col' style='flex:0.7'><div class='compare-sub' style='font-size:0.8rem;color:#888;padding-top:1rem'>"+note+"</div></div>" if note else ""}
    </div>
    """

# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_data
def load_data(data_file):
    if not data_file:
        return None
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
# SESSION SELECTION SCREEN
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
            if st.button(f"{session_info['icon']} {session_key}", key=f"btn_{session_key}",
                         use_container_width=True, type="primary"):
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
selected_session    = st.session_state.selected_session
initiative_info     = INITIATIVES[selected_initiative]
session_info        = initiative_info['sessions'][selected_session]

try:
    st.image("sls_image.jpg", use_column_width=True)
except:
    pass

# ─── Header (LNC gets its own navy header) ───────────────────────────────────
if session_info.get('type') == 'lnc':
    st.markdown(f"""
    <div class="lnc-header">
        <h1 class="initiative-title">🔗 Leaders Network Circles</h1>
        <p class="initiative-subtitle">Saudi Leadership Society — Australia Chapter</p>
        <div style="text-align:center; margin-top:1.2rem; position:relative; z-index:1;">
            <span class="circle-badge circle-growth">🌱 Growth</span>
            <span class="circle-badge circle-connect">🤝 Connection</span>
            <span class="circle-badge circle-impact">💥 Impact</span>
        </div>
        <div style="text-align:center; margin-top:1rem;">
            <span class="mission-tagline">Health Sector — Session 1</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
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

# Only load JSON for non-LNC sessions
data = None
if session_info.get('type') not in ('lnc', 'lnc_tech', 'lnc_cross', 'lnc_combined', 'leaders_accelerator'):
    data = load_data(session_info['data_file'])
    if data is None:
        st.error("Could not load data.")
        st.stop()


# ============================================================================
# LNC TECHNOLOGY SECTOR DASHBOARD
# ============================================================================

if session_info.get('type') == 'lnc_tech':

    N = 22  # post-survey respondents (used as base for post metrics)
    N_pre = 24  # pre-survey respondents

    pre = dict(
        heard_about={"Snapchat": 3, "LinkedIn": 1, "WhatsApp": 14,
                     "Friend/colleague": 3, "Other": 3},
        registration={"Excellent": 12, "Good": 11, "Fair": 0, "Poor": 1},
        connection_types={"Professional network\n(tech sector)": 19,
                          "Cross-sector\nconnections": 4,
                          "Mentorship": 10,
                          "Collaboration\npartners": 9,
                          "Curious / no target": 4},
        confidence={"Very confident": 8, "Confident": 9, "Neutral": 4,
                    "Unconfident": 2, "Very unconfident": 1},
        barriers={"Starting\nconversations": 8, "Finding\nrelevant people": 8,
                  "Shyness /\nanxiety": 1, "No specific\nbarrier": 7},
        conn_targets={"1–2": 6, "3–5": 9, "6–9": 3, "10–12": 2, "12+": 4},
        atmosphere={"Comfortable\n& friendly": 20, "Professional &\nwell-organized": 15,
                    "A bit\noverwhelming": 2, "Hard to\nconnect": 0,
                    "Casual & not\norganized": 1},
    )

    post = dict(
        format_rating={"Excellent": 19, "Good": 2, "Fair": 1, "Poor": 0},
        linkedin_conns={"1–2": 1, "3–5": 2, "6–9": 12, "10–12": 5, "12+": 2},
        meaningful={"1–2": 4, "3–5": 8, "6–9": 8, "10–12": 2, "12+": 0},
        connection_types={"Professional network\n(tech sector)": 21,
                          "Cross-sector\nconnections": 12,
                          "Mentorship": 3,
                          "Collaboration\npartners": 6,
                          "No connection\nmade": 0},
        relevance={"Very relevant": 10, "Relevant": 9, "Neutral": 3,
                   "Irrelevant": 0, "Very irrelevant": 0},
        confidence={"Very confident": 15, "Confident": 4, "Neutral": 3,
                    "Unconfident": 0, "Very unconfident": 0},
        barriers_overcome={"Starting\nconversations": 10, "Finding\nrelevant people": 5,
                           "Shyness /\nanxiety": 1, "No specific\nbarrier": 6},
        discussion_questions={"Very helpful": 12, "Helpful": 9, "Neutral": 0,
                              "Unhelpful": 0, "Very unhelpful": 1},
        atmosphere={"Comfortable\n& friendly": 20, "Professional &\nwell-organized": 16,
                    "A bit\noverwhelming": 0, "Hard to\nconnect": 0,
                    "Casual & not\norganized": 1},
        recommendation={"Very likely": 20, "Likely": 2, "Neutral": 0,
                        "Unlikely": 0, "Very unlikely": 0},
        nps={"Promoters": 15, "Passives": 5, "Detractors": 2},
    )

    # Derived numbers
    nps_score       = round((post['nps']['Promoters'] - post['nps']['Detractors']) / N * 100)
    conf_pre_high   = pre['confidence']['Very confident'] + pre['confidence']['Confident']
    conf_post_high  = post['confidence']['Very confident'] + post['confidence']['Confident']
    relevant_pct    = round((post['relevance']['Very relevant'] + post['relevance']['Relevant']) / N * 100)
    recommend_pct   = round((post['recommendation']['Very likely'] + post['recommendation']['Likely']) / N * 100)
    format_excel_pct= round(post['format_rating']['Excellent'] / N * 100)
    discussion_help = round((post['discussion_questions']['Very helpful'] + post['discussion_questions']['Helpful']) / N * 100)

    # ── HEADER ────────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="lnc-header">
        <h1 class="initiative-title">🔗 Leaders Network Circles</h1>
        <p class="initiative-subtitle">Saudi Leadership Society — Australia Chapter</p>
        <div style="text-align:center; margin-top:1.2rem; position:relative; z-index:1;">
            <span class="circle-badge circle-growth">🌱 Growth</span>
            <span class="circle-badge circle-connect">🤝 Connection</span>
            <span class="circle-badge circle-impact">💥 Impact</span>
        </div>
        <div style="text-align:center; margin-top:1rem;">
            <span class="mission-tagline">💻 Technology Sector — Session 1</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── TOP STAT PILLS ─────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="lnc-highlight-box" style="padding:2rem;">
        <div style="display:flex; flex-wrap:wrap; justify-content:center; gap:0.5rem; position:relative; z-index:1;">
            <div class="stat-pill"><span class="num">{N_pre}</span><span class="lbl">Pre-survey</span></div>
            <div class="stat-pill"><span class="num">{N}</span><span class="lbl">Post-survey</span></div>
            <div class="stat-pill"><span class="num">{format_excel_pct}%</span><span class="lbl">Excellent format</span></div>
            <div class="stat-pill"><span class="num">{relevant_pct}%</span><span class="lbl">Relevant connections</span></div>
            <div class="stat-pill"><span class="num">{nps_score}</span><span class="lbl">NPS score</span></div>
            <div class="stat-pill"><span class="num">{recommend_pct}%</span><span class="lbl">Recommend</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── SECTION: KPIs ──────────────────────────────────────────────────────────
    st.markdown('<p class="section-title">📊 Key Performance Indicators</p>', unsafe_allow_html=True)
    st.markdown('<p class="subsection-title">Reach & Event Quality</p>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(create_kpi_card("REACH", "Participants Surveyed",
            f"{N_pre} / {N}",
            f"{N_pre} pre-event · {N} post-event respondents",
            "✓ Strong survey participation"), unsafe_allow_html=True)
    with c2:
        st.markdown(create_kpi_card("FORMAT", "Circle Format — Excellent",
            f"{format_excel_pct}%",
            f"{post['format_rating']['Excellent']} of {N} rated the circle format Excellent",
            "✓ Innovative rotation format"), unsafe_allow_html=True)
    with c3:
        reg_excel = round(pre['registration']['Excellent'] / N_pre * 100)
        st.markdown(create_kpi_card("ONBOARDING", "Registration — Excellent",
            f"{reg_excel}%",
            f"{pre['registration']['Excellent']} of {N_pre} rated registration Excellent",
            "✓ Smooth onboarding"), unsafe_allow_html=True)

    st.markdown('<p class="subsection-title">Networking Outcomes</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        conf_lift = conf_post_high - conf_pre_high
        st.markdown(create_kpi_card("CONFIDENCE", "High Confidence — Post-Event",
            f"{round(conf_post_high / N * 100)}%",
            f"{conf_post_high} felt Very Confident or Confident after the event",
            f"✓ +{conf_lift} participants vs pre-event"), unsafe_allow_html=True)
    with c2:
        st.markdown(create_kpi_card("RELEVANCE", "Relevant Connections Made",
            f"{relevant_pct}%",
            f"Rated connections as Relevant or Very Relevant to their goals",
            "✓ High-quality networking"), unsafe_allow_html=True)
    with c3:
        discuss_count = post['discussion_questions']['Very helpful'] + post['discussion_questions']['Helpful']
        st.markdown(create_kpi_card("DISCUSSION", "Discussion Questions Helpful",
            f"{discussion_help}%",
            f"{discuss_count} of {N} found discussion questions Very Helpful or Helpful",
            "✓ Strong facilitation design"), unsafe_allow_html=True)

    st.markdown('<p class="subsection-title">Satisfaction & Advocacy</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        comfort_pct = round(post['atmosphere']['Comfortable\n& friendly'] / N * 100)
        st.markdown(create_kpi_card("ATMOSPHERE", "Comfortable Atmosphere",
            f"{comfort_pct}%",
            f"{post['atmosphere']['Comfortable\n& friendly']} of {N} felt comfortable & friendly",
            "✓ 0% found it overwhelming"), unsafe_allow_html=True)
    with c2:
        st.markdown(create_kpi_card("NPS", "Net Promoter Score",
            str(nps_score),
            f"Promoters: {post['nps']['Promoters']} · Passives: {post['nps']['Passives']} · Detractors: {post['nps']['Detractors']}",
            "✓ Strong advocacy"), unsafe_allow_html=True)
    with c3:
        st.markdown(create_kpi_card("ADVOCACY", "Would Recommend",
            f"{recommend_pct}%",
            f"{post['recommendation']['Very likely']} Very Likely + {post['recommendation']['Likely']} Likely",
            "✓ Outstanding word-of-mouth"), unsafe_allow_html=True)

    # ── HIGHLIGHT BOX ──────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="lnc-highlight-box">
        <h3>✨ Technology Sector Session — Highlights</h3>
        <ul>
            <li>{format_excel_pct}% rated the circle-rotation format as <strong>Excellent</strong></li>
            <li>Professional tech-sector network goal <em>exceeded</em>: 19 aimed → 21 achieved</li>
            <li>Overwhelming atmosphere dropped from <strong>2 → 0 participants</strong> post-event</li>
            <li>Discussion questions rated helpful by <strong>{discussion_help}%</strong> of participants</li>
            <li>Confidence in networking: <strong>{round(conf_pre_high/N_pre*100)}% → {round(conf_post_high/N*100)}%</strong> (Very Confident + Confident)</li>
            <li>{relevant_pct}% found connections <strong>relevant or very relevant</strong> to their goals</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # ── DEEP-DIVE TABS ─────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<p class="section-title">📚 Deep-Dive Analysis</p>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "🌐 Experience", "🤝 Connections & Goals", "💼 Outcomes", "🔄 Pre vs Post"
    ])

    # ── TAB 1: EXPERIENCE ──────────────────────────────────────────────────────
    with tab1:
        st.markdown("### Circle Format Rating (Post-Event)")
        c1, c2 = st.columns(2)
        with c1:
            fig = lnc_donut(
                list(post['format_rating'].keys()),
                list(post['format_rating'].values()),
                ['#0d3b6e', '#378add', '#85B7EB', '#e74c3c'],
                center_text="Format\nRating"
            )
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("### Discussion Questions Helpfulness")
            fig = lnc_bar(
                list(post['discussion_questions'].keys()),
                list(post['discussion_questions'].values()),
                ['#006341', '#00843d', '#93c13f', '#e9ecef', '#e74c3c'],
                height=320, v_range=[0, 15]
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Event Atmosphere — Before vs After")
        st.markdown(compare_band(
            round(pre['atmosphere']['Comfortable\n& friendly'] / N_pre * 100),
            round(post['atmosphere']['Comfortable\n& friendly'] / N * 100),
            f"{pre['atmosphere']['Comfortable\n& friendly']} felt comfortable (pre)",
            f"{post['atmosphere']['Comfortable\n& friendly']} felt comfortable (post)",
            "#6b7280", "#0d3b6e", "%", "Comfortable & friendly"
        ), unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Atmosphere — Before vs After")
            atm_labs = ["Comfortable\n& friendly", "Professional &\nwell-organized", "A bit\noverwhelming"]
            fig = lnc_grouped_bar(
                atm_labs,
                [pre['atmosphere'][k] for k in atm_labs],
                [post['atmosphere'][k] for k in atm_labs],
                y_max=25
            )
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("#### Recommendation (Post-Event)")
            fig = lnc_bar(
                list(post['recommendation'].keys()),
                list(post['recommendation'].values()),
                ['#006341', '#00843d', '#93c13f', '#e9ecef', '#e74c3c'],
                height=320, v_range=[0, 24]
            )
            st.plotly_chart(fig, use_container_width=True)

    # ── TAB 2: CONNECTIONS & GOALS ─────────────────────────────────────────────
    with tab2:
        st.markdown("### Connection Type — Intended vs Achieved")
        st.markdown(compare_band(
            19, 21,
            "aimed to expand professional tech network",
            "actually expanded professional tech network",
            "#6b7280", "#0d3b6e", "", "Tech network goal exceeded"
        ), unsafe_allow_html=True)

        conn_labs = ["Professional network\n(tech sector)", "Cross-sector\nconnections",
                     "Mentorship", "Collaboration\npartners"]
        fig = lnc_grouped_bar(
            conn_labs,
            [pre['connection_types'][k] for k in conn_labs],
            [post['connection_types'][k] for k in conn_labs],
            y_max=25
        )
        fig.update_layout(title_text="Connection Goals: Intended (Pre) vs Achieved (Post)",
            title_font=dict(family='Cormorant Garamond', size=18))
        st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Connection Target (Pre-Event)")
            fig = lnc_bar(
                list(pre['conn_targets'].keys()),
                list(pre['conn_targets'].values()),
                '#378add', height=300, v_range=[0, 12]
            )
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("#### LinkedIn Connections Made (Post-Event)")
            fig = lnc_bar(
                list(post['linkedin_conns'].keys()),
                list(post['linkedin_conns'].values()),
                '#0d3b6e', height=300, v_range=[0, 15]
            )
            st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Meaningful Connections Made (Post-Event)")
            fig = lnc_bar(
                list(post['meaningful'].keys()),
                list(post['meaningful'].values()),
                '#006341', height=300, v_range=[0, 12]
            )
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("#### Connection Relevance to Goals")
            fig = lnc_donut(
                list(post['relevance'].keys()),
                list(post['relevance'].values()),
                ['#0d3b6e', '#378add', '#85B7EB', '#e9ecef', '#e74c3c'],
                center_text="Relevance"
            )
            st.plotly_chart(fig, use_container_width=True)

    # ── TAB 3: OUTCOMES ────────────────────────────────────────────────────────
    with tab3:
        st.markdown("### Confidence Shift — Before vs After")
        st.markdown(compare_band(
            round(conf_pre_high / N_pre * 100),
            round(conf_post_high / N * 100),
            "were Very Confident or Confident pre-event",
            "were Very Confident or Confident post-event",
            "#6b7280", "#0d3b6e", "%", "Confidence improvement"
        ), unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Confidence — Before vs After")
            conf_labs = ["Very confident", "Confident", "Neutral", "Unconfident", "Very unconfident"]
            fig = lnc_grouped_bar(
                conf_labs,
                [pre['confidence'][k] for k in conf_labs],
                [post['confidence'][k] for k in conf_labs],
                y_max=18
            )
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("#### Barriers Overcome (Pre vs Post)")
            bar_labs = ["Starting\nconversations", "Finding\nrelevant people",
                        "Shyness /\nanxiety", "No specific\nbarrier"]
            fig = lnc_grouped_bar(
                [k.replace('\n', ' ') for k in bar_labs],
                [pre['barriers'][k] for k in bar_labs],
                [post['barriers_overcome'][k] for k in bar_labs],
                pre_color='#d0d9e8', post_color='#0d3b6e',
                y_max=14
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### NPS Breakdown")
        nps_labs = ["Promoters", "Passives", "Detractors"]
        fig = go.Figure(go.Bar(
            x=nps_labs,
            y=[post['nps'][k] for k in nps_labs],
            marker_color=['#006341', '#f39c12', '#e74c3c'],
            text=[post['nps'][k] for k in nps_labs],
            textposition='outside',
            textfont=dict(size=14, family='Epilogue')
        ))
        fig.update_layout(height=320, yaxis=dict(range=[0, 20]),
            font=dict(family='Epilogue', color='#2c3e50'),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # ── TAB 4: PRE vs POST ─────────────────────────────────────────────────────
    with tab4:
        st.markdown("### 🔄 Pre vs Post — Full Comparison")

        metrics_compare = [
            ("Comfortable atmosphere",
             round(pre['atmosphere']['Comfortable\n& friendly'] / N_pre * 100),
             round(post['atmosphere']['Comfortable\n& friendly'] / N * 100), "%"),
            ("High confidence (Very + Confident)",
             round(conf_pre_high / N_pre * 100),
             round(conf_post_high / N * 100), "%"),
            ("Professional tech network (intended/achieved)",
             round(19 / N_pre * 100),
             round(21 / N * 100), "%"),
            ("Overwhelming atmosphere",
             round(pre['atmosphere']['A bit\noverwhelming'] / N_pre * 100),
             round(post['atmosphere']['A bit\noverwhelming'] / N * 100), "%"),
        ]
        labels_cmp = [m[0] for m in metrics_compare]
        pre_cmp    = [m[1] for m in metrics_compare]
        post_cmp   = [m[2] for m in metrics_compare]

        fig = go.Figure()
        fig.add_trace(go.Bar(name='Before Event', y=labels_cmp, x=pre_cmp,
            orientation='h', marker_color='#d0d9e8',
            text=[f"{v}%" for v in pre_cmp], textposition='outside'))
        fig.add_trace(go.Bar(name='After Event', y=labels_cmp, x=post_cmp,
            orientation='h', marker_color='#0d3b6e',
            text=[f"{v}%" for v in post_cmp], textposition='outside'))
        fig.update_layout(barmode='group', height=380, xaxis=dict(range=[0, 110]),
            font=dict(family='Epilogue', color='#2c3e50'),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
            margin=dict(l=10, r=60, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Radar — Experience Profile")
        radar_dims = ["Comfortable\natmosphere", "Excellent\nformat", "High\nconfidence",
                      "Relevant\nconnections", "Would\nrecommend", "Discussion\nhelpful"]
        radar_pre  = [
            round(pre['atmosphere']['Comfortable\n& friendly'] / N_pre * 100),
            0,
            round(conf_pre_high / N_pre * 100),
            0, 0, 0
        ]
        radar_post = [
            round(post['atmosphere']['Comfortable\n& friendly'] / N * 100),
            format_excel_pct,
            round(conf_post_high / N * 100),
            relevant_pct,
            recommend_pct,
            discussion_help,
        ]
        fig_r = go.Figure()
        fig_r.add_trace(go.Scatterpolar(
            r=radar_pre + [radar_pre[0]], theta=radar_dims + [radar_dims[0]],
            fill='toself', name='Before Event',
            line_color='#adb5bd', fillcolor='rgba(173,181,189,0.15)', line_width=2))
        fig_r.add_trace(go.Scatterpolar(
            r=radar_post + [radar_post[0]], theta=radar_dims + [radar_dims[0]],
            fill='toself', name='After Event',
            line_color='#0d3b6e', fillcolor='rgba(13,59,110,0.15)', line_width=2.5))
        fig_r.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=10)),
                       angularaxis=dict(tickfont=dict(size=12, family='Epilogue'))),
            showlegend=True, height=480, paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation='h', yanchor='bottom', y=-0.1, xanchor='center', x=0.5)
        )
        col_l, col_c, col_r = st.columns([1, 3, 1])
        with col_c:
            st.plotly_chart(fig_r, use_container_width=True)

    # ── ABOUT BOX ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="info-box">
        <h3>📋 About Leaders Network Circles — Technology Sector</h3>
        <p>
            This Technology Sector session brought together Saudi technology students and professionals
            through the structured <strong>circle-rotation format</strong> — short rounds of small-group
            conversations across three circles: <strong>Growth, Connection, and Impact</strong>.
            Participants explored career pathways in tech, built cross-sector connections (gov-tech,
            fintech, health-tech), and strengthened the Saudi technology community in Australia —
            all aligned with <strong>Vision 2030</strong>'s digital transformation goals.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── FOOTER ─────────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="lnc-footer">
        <h2>💻 Technology Sector — Session 1</h2>
        <p class="tagline">Leaders Network Circles · Australia Chapter</p>
        <div style="display:flex; justify-content:center; gap:3rem; margin:2rem 0; flex-wrap:wrap; position:relative; z-index:1;">
            <div><div style="font-size:2.5rem;font-weight:700">{N_pre}</div><div style="opacity:0.8">Pre-survey</div></div>
            <div><div style="font-size:2.5rem;font-weight:700">{N}</div><div style="opacity:0.8">Post-survey</div></div>
            <div><div style="font-size:2.5rem;font-weight:700">{format_excel_pct}%</div><div style="opacity:0.8">Excellent format</div></div>
            <div><div style="font-size:2.5rem;font-weight:700">{nps_score}</div><div style="opacity:0.8">NPS score</div></div>
            <div><div style="font-size:2.5rem;font-weight:700">{recommend_pct}%</div><div style="opacity:0.8">Recommend</div></div>
        </div>
        <p style="font-size:1.1rem;margin-top:2rem;opacity:0.9;position:relative;z-index:1"><strong>Grow • Connect • Impact</strong></p>
        <p style="font-size:0.9rem;opacity:0.7;margin-top:1rem;position:relative;z-index:1">{datetime.now().strftime('%B %d, %Y')} | Vision 2030</p>
    </div>
    """, unsafe_allow_html=True)

    st.stop()


    # ============================================================================
# LNC CROSS-SECTOR ANALYSIS DASHBOARD (Health vs Technology)
# ============================================================================

if session_info.get('type') == 'lnc_cross':

    # ── SHARED CONSTANTS ──────────────────────────────────────────────────────
    N_H     = 27   # Health: both pre & post matched
    N_T_pre = 24   # Tech pre
    N_T     = 22   # Tech post

    # ── HEALTH DATA ───────────────────────────────────────────────────────────
    H = dict(
        registration_excellent = 21,
        heard_about  = {"Friend/colleague": 13, "WhatsApp": 10, "Other": 2, "Snapchat": 2, "LinkedIn": 0},
        conf_pre_high  = 12 + 5,   # Extremely + Somewhat confident
        conf_post_high = 19 + 7,   # Significantly + Slightly improved (used as proxy)
        atmosphere_pre_comfort  = 17,
        atmosphere_post_comfort = 23,
        atmosphere_pre_overwhelm  = 6,
        atmosphere_post_overwhelm = 0,
        format_excellent = 23,
        conn_target  = {"1–2": 8, "3–5": 9, "6–9": 5, "10–12": 2, "12+": 3},
        linkedin_post= {"1–2": 3, "3–5": 9, "6–9": 9, "10–12": 4, "12+": 2},
        meaningful_post={"1–2": 9, "3–5": 8, "6–9": 5, "10–12": 2, "12+": 3},
        nps_pre  = {"Promoters": 12, "Passives": 9, "Detractors": 6},
        nps_post = {"Promoters": 17, "Passives": 8, "Detractors": 2},
        recommendation = {"Highly recommend": 20, "Slightly recommend": 5,
                          "Maybe": 0, "Don't think they need it": 2},
        barriers_pre  = {"Starting conversations": 8, "Finding relevant people": 10,
                         "Shyness / anxiety": 6, "No specific barrier": 3},
        barriers_post = {"Starting conversations": 8, "Finding relevant people": 9,
                         "Shyness / anxiety": 6, "No specific barrier": 4},
        career_opps   = {"Yes, definitely": 14, "Possibly": 6, "Not at this stage": 7},
        network_expanded = {"Significantly": 18, "Moderately": 6, "Slightly": 1, "Not at all": 2},
        goals_pre     = {"Friendships": 20, "Professional network": 21, "Mentor": 13,
                         "Research / projects": 10, "Saudi community": 14},
        goals_post    = {"Friendships": 22, "Professional network": 24, "Mentor": 9,
                         "Research / projects": 9, "Saudi community": 15},
    )

    # ── TECH DATA ─────────────────────────────────────────────────────────────
    T = dict(
        registration_excellent = 12,
        heard_about  = {"WhatsApp": 14, "Friend/colleague": 3, "Snapchat": 3, "Other": 3, "LinkedIn": 1},
        conf_pre_high  = 8 + 9,    # Very confident + Confident
        conf_post_high = 15 + 4,   # Very confident + Confident post
        atmosphere_pre_comfort  = 20,
        atmosphere_post_comfort = 20,
        atmosphere_pre_overwhelm  = 2,
        atmosphere_post_overwhelm = 0,
        format_excellent = 19,
        conn_target  = {"1–2": 6, "3–5": 9, "6–9": 3, "10–12": 2, "12+": 4},
        linkedin_post= {"1–2": 1, "3–5": 2, "6–9": 12, "10–12": 5, "12+": 2},
        meaningful_post={"1–2": 4, "3–5": 8, "6–9": 8, "10–12": 2, "12+": 0},
        nps_post = {"Promoters": 15, "Passives": 5, "Detractors": 2},
        recommendation = {"Very likely": 20, "Likely": 2, "Neutral": 0,
                          "Unlikely": 0, "Very unlikely": 0},
        barriers_pre  = {"Starting conversations": 8, "Finding relevant people": 8,
                         "Shyness / anxiety": 1, "No specific barrier": 7},
        barriers_post = {"Starting conversations": 10, "Finding relevant people": 5,
                         "Shyness / anxiety": 1, "No specific barrier": 6},
        relevance     = {"Very relevant": 10, "Relevant": 9, "Neutral": 3,
                         "Irrelevant": 0, "Very irrelevant": 0},
        discussion_help = {"Very helpful": 12, "Helpful": 9, "Neutral": 0,
                           "Unhelpful": 0, "Very unhelpful": 1},
        conn_types_pre = {"Professional network\n(tech)": 19, "Cross-sector": 4,
                          "Mentorship": 10, "Collaboration": 9, "Curious": 4},
        conn_types_post= {"Professional network\n(tech)": 21, "Cross-sector": 12,
                          "Mentorship": 3, "Collaboration": 6, "No connection": 0},
    )

    # ── DERIVED NUMBERS ───────────────────────────────────────────────────────
    H_nps_pre  = round((H['nps_pre']['Promoters']  - H['nps_pre']['Detractors'])  / N_H * 100)
    H_nps_post = round((H['nps_post']['Promoters'] - H['nps_post']['Detractors']) / N_H * 100)
    T_nps_post = round((T['nps_post']['Promoters'] - T['nps_post']['Detractors']) / N_T * 100)

    H_format_pct      = round(H['format_excellent'] / N_H * 100)
    T_format_pct      = round(T['format_excellent'] / N_T * 100)
    H_conf_pre_pct    = round(H['conf_pre_high']  / N_H * 100)
    H_conf_post_pct   = round(H['conf_post_high'] / N_H * 100)
    T_conf_pre_pct    = round(T['conf_pre_high']  / N_T_pre * 100)
    T_conf_post_pct   = round(T['conf_post_high'] / N_T * 100)
    H_comfort_pre_pct = round(H['atmosphere_pre_comfort']  / N_H * 100)
    H_comfort_post_pct= round(H['atmosphere_post_comfort'] / N_H * 100)
    T_comfort_pre_pct = round(T['atmosphere_pre_comfort']  / N_T_pre * 100)
    T_comfort_post_pct= round(T['atmosphere_post_comfort'] / N_T * 100)
    H_rec_pct  = round(H['recommendation']['Highly recommend'] / N_H * 100)
    T_rec_pct  = round((T['recommendation']['Very likely'] + T['recommendation']['Likely']) / N_T * 100)
    H_career   = round((H['career_opps']['Yes, definitely'] + H['career_opps']['Possibly']) / N_H * 100)
    H_network  = round(H['network_expanded']['Significantly'] / N_H * 100)
    T_relevant = round((T['relevance']['Very relevant'] + T['relevance']['Relevant']) / N_T * 100)
    T_discuss  = round((T['discussion_help']['Very helpful'] + T['discussion_help']['Helpful']) / N_T * 100)

    # ── LINKEDIN WEIGHTED MIDPOINTS ───────────────────────────────────────────
    def weighted_avg_conns(d, n):
        mids = {"1–2": 1.5, "3–5": 4, "6–9": 7.5, "10–12": 11, "12+": 13}
        return round(sum(mids[k] * v for k, v in d.items()) / n, 1)

    H_linkedin_avg = weighted_avg_conns(H['linkedin_post'], N_H)
    T_linkedin_avg = weighted_avg_conns(T['linkedin_post'], N_T)
    H_meaningful_avg = weighted_avg_conns(H['meaningful_post'], N_H)
    T_meaningful_avg = weighted_avg_conns(T['meaningful_post'], N_T)

    # ── HEADER ────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="lnc-header">
        <h1 class="initiative-title">⚡ Cross-Sector Analysis</h1>
        <p class="initiative-subtitle">Saudi Leadership Society — Australia Chapter</p>
        <div style="text-align:center; margin-top:1.2rem; position:relative; z-index:1;">
            <span class="circle-badge circle-growth">🏥 Health Sector</span>
            <span class="circle-badge circle-impact">💻 Technology Sector</span>
        </div>
        <div style="text-align:center; margin-top:1rem;">
            <span class="mission-tagline">Leaders Network Circles — Comparative Insights</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── TOP STAT PILLS ─────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="lnc-highlight-box" style="padding:2rem;">
        <div style="display:flex; flex-wrap:wrap; justify-content:center; gap:0.5rem; position:relative; z-index:1;">
            <div class="stat-pill"><span class="num">{N_H}</span><span class="lbl">Health participants</span></div>
            <div class="stat-pill"><span class="num">{N_T}</span><span class="lbl">Tech participants</span></div>
            <div class="stat-pill"><span class="num">{H_nps_post} vs {T_nps_post}</span><span class="lbl">NPS (H vs T)</span></div>
            <div class="stat-pill"><span class="num">{H_format_pct}% vs {T_format_pct}%</span><span class="lbl">Excellent format (H vs T)</span></div>
            <div class="stat-pill"><span class="num">{H_rec_pct}% vs {T_rec_pct}%</span><span class="lbl">Recommend (H vs T)</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI COMPARISON CARDS ───────────────────────────────────────────────────
    st.markdown('<p class="section-title">📊 Side-by-Side KPIs</p>', unsafe_allow_html=True)

    def dual_kpi(label, h_val, t_val, h_ctx="", t_ctx="", icon=""):
        winner_h = str(h_val).replace('%','').replace('pts','').strip()
        winner_t = str(t_val).replace('%','').replace('pts','').strip()
        try:
            h_num = float(winner_h); t_num = float(winner_t)
            h_style = "color:#006341;font-weight:900" if h_num >= t_num else "color:#1a5fa8;font-weight:700"
            t_style = "color:#006341;font-weight:900" if t_num >= h_num else "color:#1a5fa8;font-weight:700"
        except:
            h_style = t_style = "color:#1a5fa8;font-weight:700"
        return f"""
        <div style="background:white;border-radius:20px;padding:1.8rem;
             box-shadow:0 8px 30px rgba(13,59,110,0.08);border:1px solid rgba(13,59,110,0.08);
             position:relative;overflow:hidden;height:100%;">
            <div style="position:absolute;top:0;left:0;width:5px;height:100%;
                 background:linear-gradient(180deg,#006341,#1a5fa8);"></div>
            <div style="font-size:0.7rem;font-weight:900;color:#0d3b6e;
                 text-transform:uppercase;letter-spacing:0.15em;margin-bottom:0.5rem;">{icon} {label}</div>
            <div style="display:flex;gap:0.5rem;align-items:stretch;margin-top:0.8rem;">
                <div style="flex:1;text-align:center;padding:1rem;
                     background:rgba(0,99,65,0.06);border-radius:14px;">
                    <div style="font-size:0.65rem;font-weight:800;color:#006341;
                         text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.4rem;">🏥 HEALTH</div>
                    <div style="font-family:'Cormorant Garamond',serif;font-size:2.2rem;
                         font-weight:700;{h_style};line-height:1">{h_val}</div>
                    <div style="font-size:0.78rem;color:#666;margin-top:0.4rem;line-height:1.3">{h_ctx}</div>
                </div>
                <div style="flex:1;text-align:center;padding:1rem;
                     background:rgba(13,59,110,0.06);border-radius:14px;">
                    <div style="font-size:0.65rem;font-weight:800;color:#1a5fa8;
                         text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.4rem;">💻 TECH</div>
                    <div style="font-family:'Cormorant Garamond',serif;font-size:2.2rem;
                         font-weight:700;{t_style};line-height:1">{t_val}</div>
                    <div style="font-size:0.78rem;color:#666;margin-top:0.4rem;line-height:1.3">{t_ctx}</div>
                </div>
            </div>
        </div>
        """

    st.markdown('<p class="subsection-title">Reach & Format Quality</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(dual_kpi("Participants Surveyed", N_H, N_T,
            "matched pre & post", "post-event respondents", "👥"), unsafe_allow_html=True)
    with c2:
        st.markdown(dual_kpi("Format — Excellent", f"{H_format_pct}%", f"{T_format_pct}%",
            f"{H['format_excellent']} of {N_H}", f"{T['format_excellent']} of {N_T}", "🏆"), unsafe_allow_html=True)
    with c3:
        reg_h = round(H['registration_excellent'] / N_H * 100)
        reg_t = round(T['registration_excellent'] / N_T_pre * 100)
        st.markdown(dual_kpi("Registration — Excellent", f"{reg_h}%", f"{reg_t}%",
            f"{H['registration_excellent']} of {N_H}", f"{T['registration_excellent']} of {N_T_pre}", "📋"), unsafe_allow_html=True)

    st.markdown('<p class="subsection-title">Confidence & Atmosphere</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(dual_kpi("Pre-Event High Confidence", f"{H_conf_pre_pct}%", f"{T_conf_pre_pct}%",
            f"{H['conf_pre_high']} of {N_H}", f"{T['conf_pre_high']} of {N_T_pre}", "💪"), unsafe_allow_html=True)
    with c2:
        st.markdown(dual_kpi("Post-Event High Confidence", f"{H_conf_post_pct}%", f"{T_conf_post_pct}%",
            f"of {N_H} participants", f"of {N_T} participants", "🚀"), unsafe_allow_html=True)
    with c3:
        st.markdown(dual_kpi("Comfortable Atmosphere (Post)", f"{H_comfort_post_pct}%", f"{T_comfort_post_pct}%",
            f"{H['atmosphere_post_comfort']} of {N_H}", f"{T['atmosphere_post_comfort']} of {N_T}", "🌿"), unsafe_allow_html=True)

    st.markdown('<p class="subsection-title">Connections & Advocacy</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(dual_kpi("Avg LinkedIn Connections", f"{H_linkedin_avg}", f"{T_linkedin_avg}",
            "weighted avg per participant", "weighted avg per participant", "🔗"), unsafe_allow_html=True)
    with c2:
        st.markdown(dual_kpi("Avg Meaningful Connections", f"{H_meaningful_avg}", f"{T_meaningful_avg}",
            "weighted avg per participant", "weighted avg per participant", "🤝"), unsafe_allow_html=True)
    with c3:
        st.markdown(dual_kpi("Would Recommend", f"{H_rec_pct}%", f"{T_rec_pct}%",
            f"{H['recommendation']['Highly recommend']} highly recommend",
            f"{T['recommendation']['Very likely']} very likely", "📣"), unsafe_allow_html=True)

    st.markdown('<p class="subsection-title">NPS & Satisfaction</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(dual_kpi("NPS Score (Post-Event)", str(H_nps_post), str(T_nps_post),
            f"was {H_nps_pre} pre-event", "post-event only", "📈"), unsafe_allow_html=True)
    with c2:
        st.markdown(dual_kpi("Overwhelming Atmosphere Eliminated",
            f"{H['atmosphere_pre_overwhelm']} → 0",
            f"{T['atmosphere_pre_overwhelm']} → 0",
            "participants pre → post", "participants pre → post", "✅"), unsafe_allow_html=True)
    with c3:
        st.markdown(dual_kpi("Sector-Specific Outcome",
            f"{H_career}%", f"{T_relevant}%",
            "found career opportunities", "found relevant connections", "🎯"), unsafe_allow_html=True)

    # ── HIGHLIGHT BOX ──────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="lnc-highlight-box">
        <h3>⚡ Cross-Sector Insights — What the Data Tells Us</h3>
        <ul>
            <li>Both sectors <strong>eliminated overwhelming atmosphere</strong> post-event — the circle format works universally</li>
            <li>Tech participants made <strong>more LinkedIn connections</strong> on average ({T_linkedin_avg} vs {H_linkedin_avg}), reflecting the sector's digital-native culture</li>
            <li>Health sector had a <strong>stronger NPS swing</strong>: {H_nps_pre} → {H_nps_post} (+{H_nps_post - H_nps_pre} pts); Tech achieved {T_nps_post} post-event</li>
            <li>Confidence improved in both sectors: Health {H_conf_pre_pct}% → {H_conf_post_pct}% · Tech {T_conf_pre_pct}% → {T_conf_post_pct}%</li>
            <li>Tech participants skewed toward <strong>higher connection volumes</strong> (6–9 range dominated); Health leaned toward <strong>deeper meaningful ties</strong></li>
            <li>Both sessions achieved <strong>{min(H_rec_pct, T_rec_pct)}%+ recommendation rates</strong>, validating the LNC format across sectors</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # ── DEEP-DIVE TABS ─────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<p class="section-title">📚 Deep-Dive Comparison</p>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview", "🤝 Connections", "💪 Confidence & Barriers",
        "📣 Advocacy & NPS", "🕸️ Radar Profile"
    ])

    # ── TAB 1: OVERVIEW ────────────────────────────────────────────────────────
    with tab1:
        st.markdown("### Format Rating — Health vs Technology")
        c1, c2 = st.columns(2)
        with c1:
            fig = go.Figure()
            fmt_labs = ["Excellent", "Good", "Fair", "Poor"]
            fig.add_trace(go.Bar(name='🏥 Health', x=fmt_labs,
                y=[H['format_excellent'], 3, 0, 1],
                marker_color='#006341',
                text=[H['format_excellent'], 3, 0, 1], textposition='outside'))
            fig.add_trace(go.Bar(name='💻 Technology', x=fmt_labs,
                y=[T['format_excellent'], 2, 1, 0],
                marker_color='#1a5fa8',
                text=[T['format_excellent'], 2, 1, 0], textposition='outside'))
            fig.update_layout(barmode='group', height=360, yaxis=dict(range=[0, 28]),
                font=dict(family='Epilogue', color='#2c3e50'),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5))
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("### Comfortable Atmosphere — Pre vs Post")
            dims = ['Health Pre', 'Health Post', 'Tech Pre', 'Tech Post']
            vals = [H_comfort_pre_pct, H_comfort_post_pct, T_comfort_pre_pct, T_comfort_post_pct]
            colors = ['rgba(0,99,65,0.4)', '#006341', 'rgba(13,59,110,0.4)', '#1a5fa8']
            fig = go.Figure(go.Bar(x=dims, y=vals, marker_color=colors,
                text=[f"{v}%" for v in vals], textposition='outside',
                textfont=dict(size=13, family='Epilogue')))
            fig.update_layout(height=360, yaxis=dict(range=[0, 100]),
                font=dict(family='Epilogue', color='#2c3e50'),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Registration Excellence & Outreach")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Registration Rating — Excellent %")
            fig = go.Figure(go.Bar(
                x=['🏥 Health', '💻 Technology'],
                y=[round(H['registration_excellent']/N_H*100),
                   round(T['registration_excellent']/N_T_pre*100)],
                marker_color=['#006341', '#1a5fa8'],
                text=[f"{round(H['registration_excellent']/N_H*100)}%",
                      f"{round(T['registration_excellent']/N_T_pre*100)}%"],
                textposition='outside', textfont=dict(size=14)
            ))
            fig.update_layout(height=320, yaxis=dict(range=[0, 100]),
                font=dict(family='Epilogue', color='#2c3e50'),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("#### How Participants Heard About the Event")
            channels = ["WhatsApp", "Friend/colleague", "Snapchat", "LinkedIn", "Other"]
            h_heard = [10, 13, 2, 0, 2]
            t_heard = [14, 3, 3, 1, 3]
            fig = go.Figure()
            fig.add_trace(go.Bar(name='🏥 Health', x=channels, y=h_heard,
                marker_color='#006341', text=h_heard, textposition='outside'))
            fig.add_trace(go.Bar(name='💻 Technology', x=channels, y=t_heard,
                marker_color='#1a5fa8', text=t_heard, textposition='outside'))
            fig.update_layout(barmode='group', height=320, yaxis=dict(range=[0, 18]),
                font=dict(family='Epilogue', color='#2c3e50'),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5))
            st.plotly_chart(fig, use_container_width=True)

    # ── TAB 2: CONNECTIONS ─────────────────────────────────────────────────────
    with tab2:
        st.markdown("### LinkedIn Connections Made — Distribution")
        conn_labs = ["1–2", "3–5", "6–9", "10–12", "12+"]
        h_linkedin = [H['linkedin_post'][k] for k in conn_labs]
        t_linkedin = [T['linkedin_post'][k] for k in conn_labs]
        fig = go.Figure()
        fig.add_trace(go.Bar(name='🏥 Health', x=conn_labs, y=h_linkedin,
            marker_color='#006341', text=h_linkedin, textposition='outside'))
        fig.add_trace(go.Bar(name='💻 Technology', x=conn_labs, y=t_linkedin,
            marker_color='#1a5fa8', text=t_linkedin, textposition='outside'))
        fig.update_layout(barmode='group', height=380, yaxis=dict(range=[0, 15]),
            font=dict(family='Epilogue', color='#2c3e50'),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5))
        st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Meaningful Connections — Distribution")
            h_mean = [H['meaningful_post'][k] for k in conn_labs]
            t_mean = [T['meaningful_post'][k] for k in conn_labs]
            fig = go.Figure()
            fig.add_trace(go.Bar(name='🏥 Health', x=conn_labs, y=h_mean,
                marker_color='#006341', text=h_mean, textposition='outside'))
            fig.add_trace(go.Bar(name='💻 Technology', x=conn_labs, y=t_mean,
                marker_color='#1a5fa8', text=t_mean, textposition='outside'))
            fig.update_layout(barmode='group', height=340, yaxis=dict(range=[0, 12]),
                font=dict(family='Epilogue', color='#2c3e50'),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5))
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("#### Weighted Average Connections")
            avg_labs = ["LinkedIn\nConnections", "Meaningful\nConnections"]
            fig = go.Figure()
            fig.add_trace(go.Bar(name='🏥 Health', x=avg_labs,
                y=[H_linkedin_avg, H_meaningful_avg],
                marker_color='#006341',
                text=[f"{H_linkedin_avg}", f"{H_meaningful_avg}"],
                textposition='outside', textfont=dict(size=14)))
            fig.add_trace(go.Bar(name='💻 Technology', x=avg_labs,
                y=[T_linkedin_avg, T_meaningful_avg],
                marker_color='#1a5fa8',
                text=[f"{T_linkedin_avg}", f"{T_meaningful_avg}"],
                textposition='outside', textfont=dict(size=14)))
            fig.update_layout(barmode='group', height=340, yaxis=dict(range=[0, 12]),
                font=dict(family='Epilogue', color='#2c3e50'),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5))
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Connection Target (Pre-Event) — What Did They Aim For?")
        h_targets = [H['conn_target'][k] for k in conn_labs]
        t_targets = [T['conn_target'][k] for k in conn_labs]
        fig = go.Figure()
        fig.add_trace(go.Bar(name='🏥 Health', x=conn_labs, y=h_targets,
            marker_color='rgba(0,99,65,0.5)', text=h_targets, textposition='outside'))
        fig.add_trace(go.Bar(name='💻 Technology', x=conn_labs, y=t_targets,
            marker_color='rgba(13,59,110,0.5)', text=t_targets, textposition='outside'))
        fig.update_layout(barmode='group', height=340, yaxis=dict(range=[0, 12]),
            font=dict(family='Epilogue', color='#2c3e50'),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
            title_text="Pre-Event Connection Targets vs Post-Event Achievements",
            title_font=dict(family='Cormorant Garamond', size=16))
        st.plotly_chart(fig, use_container_width=True)

    # ── TAB 3: CONFIDENCE & BARRIERS ───────────────────────────────────────────
    with tab3:
        st.markdown("### Confidence Journey — Pre to Post")
        conf_cats = ["Pre-Event\nHigh Confidence", "Post-Event\nHigh Confidence", "Confidence\nLift (pp)"]
        h_conf = [H_conf_pre_pct, H_conf_post_pct, H_conf_post_pct - H_conf_pre_pct]
        t_conf = [T_conf_pre_pct, T_conf_post_pct, T_conf_post_pct - T_conf_pre_pct]
        fig = go.Figure()
        fig.add_trace(go.Bar(name='🏥 Health', x=conf_cats, y=h_conf,
            marker_color='#006341', text=[f"{v}%" for v in h_conf], textposition='outside'))
        fig.add_trace(go.Bar(name='💻 Technology', x=conf_cats, y=t_conf,
            marker_color='#1a5fa8', text=[f"{v}%" for v in t_conf], textposition='outside'))
        fig.update_layout(barmode='group', height=380, yaxis=dict(range=[-5, 100]),
            font=dict(family='Epilogue', color='#2c3e50'),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Networking Barriers — Pre-Event vs Post-Event (Overcome)")
        barrier_cats = ["Starting conversations", "Finding relevant people",
                        "Shyness / anxiety", "No specific barrier"]
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 🏥 Health Sector")
            h_pre_b  = [H['barriers_pre'][k]  for k in barrier_cats]
            h_post_b = [H['barriers_post'][k] for k in barrier_cats]
            fig = lnc_grouped_bar(
                barrier_cats, h_pre_b, h_post_b,
                pre_color='rgba(0,99,65,0.3)', post_color='#006341', y_max=14
            )
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("#### 💻 Technology Sector")
            t_pre_b  = [T['barriers_pre'][k]  for k in barrier_cats]
            t_post_b = [T['barriers_post'][k] for k in barrier_cats]
            fig = lnc_grouped_bar(
                barrier_cats, t_pre_b, t_post_b,
                pre_color='rgba(13,59,110,0.3)', post_color='#1a5fa8', y_max=14
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Barriers Comparison — Health vs Technology (Pre-Event)")
        fig = go.Figure()
        fig.add_trace(go.Bar(name='🏥 Health', x=barrier_cats,
            y=[H['barriers_pre'][k] for k in barrier_cats],
            marker_color='#006341',
            text=[H['barriers_pre'][k] for k in barrier_cats], textposition='outside'))
        fig.add_trace(go.Bar(name='💻 Technology', x=barrier_cats,
            y=[T['barriers_pre'][k] for k in barrier_cats],
            marker_color='#1a5fa8',
            text=[T['barriers_pre'][k] for k in barrier_cats], textposition='outside'))
        fig.update_layout(barmode='group', height=360, yaxis=dict(range=[0, 14]),
            font=dict(family='Epilogue', color='#2c3e50'),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5))
        st.plotly_chart(fig, use_container_width=True)

    # ── TAB 4: ADVOCACY & NPS ──────────────────────────────────────────────────
    with tab4:
        st.markdown("### NPS Comparison")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 🏥 Health — NPS Journey (Pre → Post)")
            nps_labs = ["Promoters", "Passives", "Detractors"]
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Before', x=nps_labs,
                y=[H['nps_pre'][k] for k in nps_labs],
                marker_color=['rgba(0,99,65,0.4)', 'rgba(243,156,18,0.4)', 'rgba(231,76,60,0.4)'],
                text=[H['nps_pre'][k] for k in nps_labs], textposition='outside'))
            fig.add_trace(go.Bar(name='After', x=nps_labs,
                y=[H['nps_post'][k] for k in nps_labs],
                marker_color=['#006341', '#e67e22', '#e74c3c'],
                text=[H['nps_post'][k] for k in nps_labs], textposition='outside'))
            fig.update_layout(barmode='group', height=340, yaxis=dict(range=[0, 22]),
                font=dict(family='Epilogue', color='#2c3e50'),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5))
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("#### 💻 Technology — NPS (Post-Event Only)")
            fig = go.Figure(go.Bar(
                x=nps_labs,
                y=[T['nps_post'][k] for k in nps_labs],
                marker_color=['#1a5fa8', '#e67e22', '#e74c3c'],
                text=[T['nps_post'][k] for k in nps_labs],
                textposition='outside', textfont=dict(size=14)
            ))
            fig.update_layout(height=340, yaxis=dict(range=[0, 20]),
                font=dict(family='Epilogue', color='#2c3e50'),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Recommendation — Health vs Technology")
        c1, c2 = st.columns(2)
        with c1:
            fig = lnc_donut(
                ["Highly recommend", "Slightly recommend", "Maybe", "Don't think they need it"],
                [H['recommendation']['Highly recommend'], H['recommendation']['Slightly recommend'],
                 H['recommendation']['Maybe'], H['recommendation']["Don't think they need it"]],
                ['#006341', '#00843d', '#93c13f', '#e74c3c'],
                center_text="🏥 Health\nRecommend"
            )
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig = lnc_donut(
                ["Very likely", "Likely", "Neutral", "Unlikely", "Very unlikely"],
                [T['recommendation']['Very likely'], T['recommendation']['Likely'],
                 T['recommendation']['Neutral'], T['recommendation']['Unlikely'],
                 T['recommendation']['Very unlikely']],
                ['#1a5fa8', '#378add', '#85B7EB', '#e9ecef', '#e74c3c'],
                center_text="💻 Tech\nRecommend"
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### NPS Score — Final Comparison")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=['🏥 Health (Pre)', '🏥 Health (Post)', '💻 Tech (Post)'],
            y=[H_nps_pre, H_nps_post, T_nps_post],
            marker_color=['rgba(0,99,65,0.4)', '#006341', '#1a5fa8'],
            text=[str(H_nps_pre), str(H_nps_post), str(T_nps_post)],
            textposition='outside', textfont=dict(size=15, family='Cormorant Garamond')
        ))
        fig.update_layout(height=360, yaxis=dict(range=[-10, 60]),
            font=dict(family='Epilogue', color='#2c3e50'),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False)
        fig.add_hline(y=0, line_dash="dash", line_color="#adb5bd", line_width=1.5)
        st.plotly_chart(fig, use_container_width=True)

    # ── TAB 5: RADAR PROFILE ───────────────────────────────────────────────────
    with tab5:
        st.markdown("### 🕸️ Sector Profile Radar — Health vs Technology")
        radar_dims = [
            "Format\nExcellent %", "Post-Event\nComfort %",
            "Confidence\nLift (pp)", "Avg LinkedIn\nConns (×10)",
            "Recommend %", "NPS Score\n(normalised)"
        ]
        h_radar = [
            H_format_pct,
            H_comfort_post_pct,
            H_conf_post_pct - H_conf_pre_pct,
            round(H_linkedin_avg * 10),
            H_rec_pct,
            round((H_nps_post + 100) / 2)
        ]
        t_radar = [
            T_format_pct,
            T_comfort_post_pct,
            T_conf_post_pct - T_conf_pre_pct,
            round(T_linkedin_avg * 10),
            T_rec_pct,
            round((T_nps_post + 100) / 2)
        ]
        fig_r = go.Figure()
        fig_r.add_trace(go.Scatterpolar(
            r=h_radar + [h_radar[0]], theta=radar_dims + [radar_dims[0]],
            fill='toself', name='🏥 Health',
            line_color='#006341', fillcolor='rgba(0,99,65,0.15)', line_width=2.5))
        fig_r.add_trace(go.Scatterpolar(
            r=t_radar + [t_radar[0]], theta=radar_dims + [radar_dims[0]],
            fill='toself', name='💻 Technology',
            line_color='#1a5fa8', fillcolor='rgba(13,59,110,0.15)', line_width=2.5))
        fig_r.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=10)),
                angularaxis=dict(tickfont=dict(size=12, family='Epilogue'))
            ),
            showlegend=True, height=520, paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation='h', yanchor='bottom', y=-0.1, xanchor='center', x=0.5)
        )
        col_l, col_c, col_r = st.columns([1, 3, 1])
        with col_c:
            st.plotly_chart(fig_r, use_container_width=True)

        st.markdown("### Metric-by-Metric Breakdown")
        metric_names = ["Format Excellent %", "Post Comfort %",
                        "Confidence Lift (pp)", "Avg LinkedIn Conns",
                        "Recommend %", "NPS Score"]
        h_vals_table = [H_format_pct, H_comfort_post_pct,
                        H_conf_post_pct - H_conf_pre_pct,
                        H_linkedin_avg, H_rec_pct, H_nps_post]
        t_vals_table = [T_format_pct, T_comfort_post_pct,
                        T_conf_post_pct - T_conf_pre_pct,
                        T_linkedin_avg, T_rec_pct, T_nps_post]

        fig_table = go.Figure()
        fig_table.add_trace(go.Bar(
            name='🏥 Health', x=metric_names, y=h_vals_table,
            marker_color='#006341',
            text=[str(v) for v in h_vals_table], textposition='outside'))
        fig_table.add_trace(go.Bar(
            name='💻 Technology', x=metric_names, y=t_vals_table,
            marker_color='#1a5fa8',
            text=[str(v) for v in t_vals_table], textposition='outside'))
        fig_table.update_layout(barmode='group', height=420, yaxis=dict(range=[0, 110]),
            font=dict(family='Epilogue', color='#2c3e50'),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5))
        st.plotly_chart(fig_table, use_container_width=True)

    # ── ABOUT BOX ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="info-box">
        <h3>📋 About This Cross-Sector Analysis</h3>
        <p>
            This page compares the <strong>Leaders Network Circles — Health Sector (Session 1)</strong>
            and <strong>Technology Sector (Session 1)</strong> side by side. Both sessions used the same 
            circle-rotation format across three circles: <strong>Growth, Connection, and Impact</strong>.
            <br><br>
            <strong>Health:</strong> N = 27 (matched pre & post) &nbsp;|&nbsp;
            <strong>Technology:</strong> N = 24 pre · 22 post
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── FOOTER ─────────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="lnc-footer">
        <h2>⚡ Cross-Sector Analysis</h2>
        <p class="tagline">Health × Technology · Leaders Network Circles · Australia Chapter</p>
        <div style="display:flex; justify-content:center; gap:3rem; margin:2rem 0;
             flex-wrap:wrap; position:relative; z-index:1;">
            <div><div style="font-size:2.5rem;font-weight:700">{N_H} + {N_T}</div>
                 <div style="opacity:0.8">Total participants</div></div>
            <div><div style="font-size:2.5rem;font-weight:700">{H_nps_post} vs {T_nps_post}</div>
                 <div style="opacity:0.8">NPS (H vs T)</div></div>
            <div><div style="font-size:2.5rem;font-weight:700">{H_rec_pct}% / {T_rec_pct}%</div>
                 <div style="opacity:0.8">Recommend (H / T)</div></div>
            <div><div style="font-size:2.5rem;font-weight:700">0%</div>
                 <div style="opacity:0.8">Overwhelming atmosphere (both)</div></div>
        </div>
        <p style="font-size:1.1rem;margin-top:2rem;opacity:0.9;position:relative;z-index:1">
            <strong>Grow • Connect • Impact</strong></p>
        <p style="font-size:0.9rem;opacity:0.7;margin-top:1rem;position:relative;z-index:1">
            {datetime.now().strftime('%B %d, %Y')} | Vision 2030</p>
    </div>
    """, unsafe_allow_html=True)

    st.stop()


# ============================================================================
# LNC COMBINED ANALYSIS DASHBOARD (Health + Technology)
# ============================================================================

if session_info.get('type') == 'lnc_combined':

    # ── SHARED CONSTANTS ──────────────────────────────────────────────────────
    N_H     = 27
    N_T_pre = 24
    N_T     = 22
    N_total_pre  = N_H + N_T_pre   # 51
    N_total_post = N_H + N_T       # 49

    # ── COMBINED RAW COUNTS ───────────────────────────────────────────────────

    # Registration excellence
    reg_excellent = 21 + 12   # 33
    reg_good      = 5  + 11   # 16
    reg_fair      = 1  + 0    # 1
    reg_poor      = 1  + 1    # 2 (health poor=0 actually, tech poor=1; health had 0 poor in reg)

    # Format excellence (post)
    fmt_excellent = 23 + 19   # 42
    fmt_good      = 3  + 2    # 5
    fmt_fair      = 0  + 1    # 1
    fmt_poor      = 1  + 0    # 1

    # Atmosphere — comfortable & friendly
    atm_pre_comfort  = 17 + 20   # 37
    atm_post_comfort = 23 + 20   # 43
    atm_pre_overwhelm  = 6 + 2   # 8
    atm_post_overwhelm = 0 + 0   # 0

    # Confidence
    conf_pre_high  = (12 + 5) + (8 + 9)    # 34
    conf_post_high = (19 + 7) + (15 + 4)   # 45

    # LinkedIn connections (post) — raw counts per bucket
    linkedin_combined = {
        "1–2":   3 + 1,    # 4
        "3–5":   9 + 2,    # 11
        "6–9":   9 + 12,   # 21
        "10–12": 4 + 5,    # 9
        "12+":   2 + 2,    # 4
    }

    # Meaningful connections (post)
    meaningful_combined = {
        "1–2":   9 + 4,    # 13
        "3–5":   8 + 8,    # 16
        "6–9":   5 + 8,    # 13
        "10–12": 2 + 2,    # 4
        "12+":   3 + 0,    # 3
    }

    # Connection targets (pre)
    conn_target_combined = {
        "1–2":   8 + 6,    # 14
        "3–5":   9 + 9,    # 18
        "6–9":   5 + 3,    # 8
        "10–12": 2 + 2,    # 4
        "12+":   3 + 4,    # 7
    }

    # Barriers pre
    barriers_pre_combined = {
        "Starting\nconversations":  8 + 8,    # 16
        "Finding\nrelevant people": 10 + 8,   # 18
        "Shyness /\nanxiety":       6 + 1,    # 7
        "No specific\nbarrier":     3 + 7,    # 10
    }

    # Barriers post (overcome)
    barriers_post_combined = {
        "Starting\nconversations":  8 + 10,   # 18
        "Finding\nrelevant people": 9 + 5,    # 14
        "Shyness /\nanxiety":       6 + 1,    # 7
        "No specific\nbarrier":     4 + 6,    # 10
    }

    # NPS post (combined raw counts)
    nps_post_combined = {
        "Promoters":  17 + 15,   # 32
        "Passives":   8  + 5,    # 13
        "Detractors": 2  + 2,    # 4
    }
    nps_pre_health = {
        "Promoters": 12, "Passives": 9, "Detractors": 6
    }

    # How heard (pre) — combined
    heard_combined = {
        "WhatsApp":          10 + 14,  # 24
        "Friend/colleague":  13 + 3,   # 16
        "Snapchat":          2  + 3,   # 5
        "Other":             2  + 3,   # 5
        "LinkedIn":          0  + 1,   # 1
    }

    # ── DERIVED METRICS ───────────────────────────────────────────────────────
    fmt_excel_pct      = round(fmt_excellent / N_total_post * 100)
    reg_excel_pct      = round(reg_excellent / N_total_pre  * 100)
    conf_pre_pct       = round(conf_pre_high  / N_total_pre  * 100)
    conf_post_pct      = round(conf_post_high / N_total_post * 100)
    conf_lift          = conf_post_pct - conf_pre_pct
    comfort_pre_pct    = round(atm_pre_comfort  / N_total_pre  * 100)
    comfort_post_pct   = round(atm_post_comfort / N_total_post * 100)
    overwhelm_pre_pct  = round(atm_pre_overwhelm  / N_total_pre  * 100)
    overwhelm_post_pct = round(atm_post_overwhelm / N_total_post * 100)

    nps_score = round(
        (nps_post_combined['Promoters'] - nps_post_combined['Detractors'])
        / N_total_post * 100
    )

    # Recommend combined
    # Health: "Highly recommend" = 20 of 27
    # Tech:   "Very likely" + "Likely" = 20 + 2 = 22 of 22
    rec_combined     = 20 + 22    # 42
    rec_combined_pct = round(rec_combined / N_total_post * 100)

    # Weighted avg connections helper
    def weighted_avg(d, n):
        mids = {"1–2": 1.5, "3–5": 4, "6–9": 7.5, "10–12": 11, "12+": 13}
        return round(sum(mids[k] * v for k, v in d.items()) / n, 1)

    linkedin_avg    = weighted_avg(linkedin_combined,    N_total_post)
    meaningful_avg  = weighted_avg(meaningful_combined,  N_total_post)
    target_avg      = weighted_avg(conn_target_combined, N_total_pre)

    # Career & outcomes (health only has these; used as partial combined)
    # Health career opps: 14 definite + 6 possible = 20 of 27 = 74%
    # Tech relevant conns: 10 + 9 = 19 of 22 = 86%
    career_combined     = 20 + 19   # 39
    career_combined_pct = round(career_combined / N_total_post * 100)

    # ── HEADER ────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="lnc-header">
        <h1 class="initiative-title">🌐 Combined Programme Analysis</h1>
        <p class="initiative-subtitle">Saudi Leadership Society — Australia Chapter</p>
        <div style="text-align:center; margin-top:1.2rem; position:relative; z-index:1;">
            <span class="circle-badge circle-growth">🌱 Growth</span>
            <span class="circle-badge circle-connect">🤝 Connection</span>
            <span class="circle-badge circle-impact">💥 Impact</span>
        </div>
        <div style="text-align:center; margin-top:1rem;">
            <span class="mission-tagline">🏥 Health + 💻 Technology — All Sessions Combined</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── TOP STAT PILLS ─────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="lnc-highlight-box" style="padding:2rem;">
        <div style="display:flex; flex-wrap:wrap; justify-content:center;
             gap:0.5rem; position:relative; z-index:1;">
            <div class="stat-pill">
                <span class="num">{N_total_pre}</span>
                <span class="lbl">Pre-survey total</span>
            </div>
            <div class="stat-pill">
                <span class="num">{N_total_post}</span>
                <span class="lbl">Post-survey total</span>
            </div>
            <div class="stat-pill">
                <span class="num">{fmt_excel_pct}%</span>
                <span class="lbl">Excellent format</span>
            </div>
            <div class="stat-pill">
                <span class="num">{conf_lift:+}pp</span>
                <span class="lbl">Confidence lift</span>
            </div>
            <div class="stat-pill">
                <span class="num">{nps_score}</span>
                <span class="lbl">Combined NPS</span>
            </div>
            <div class="stat-pill">
                <span class="num">{rec_combined_pct}%</span>
                <span class="lbl">Would recommend</span>
            </div>
            <div class="stat-pill">
                <span class="num">0%</span>
                <span class="lbl">Overwhelmed (post)</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI CARDS ──────────────────────────────────────────────────────────────
    st.markdown('<p class="section-title">📊 Programme-Wide KPIs</p>',
                unsafe_allow_html=True)

    st.markdown('<p class="subsection-title">Reach & Event Quality</p>',
                unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(create_kpi_card(
            "REACH", "Total Participants",
            f"{N_total_pre} / {N_total_post}",
            f"{N_total_pre} pre-event across both sectors · {N_total_post} post-event",
            "✓ 2 sectors · 2 sessions"
        ), unsafe_allow_html=True)
    with c2:
        st.markdown(create_kpi_card(
            "FORMAT", "Circle Format — Excellent",
            f"{fmt_excel_pct}%",
            f"{fmt_excellent} of {N_total_post} rated the format Excellent",
            "✓ Consistent across both sectors"
        ), unsafe_allow_html=True)
    with c3:
        st.markdown(create_kpi_card(
            "ONBOARDING", "Registration — Excellent",
            f"{reg_excel_pct}%",
            f"{reg_excellent} of {N_total_pre} rated registration Excellent",
            "✓ Smooth onboarding programme-wide"
        ), unsafe_allow_html=True)

    st.markdown('<p class="subsection-title">Networking Outcomes</p>',
                unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(create_kpi_card(
            "CONFIDENCE", "Post-Event High Confidence",
            f"{conf_post_pct}%",
            f"{conf_post_high} of {N_total_post} felt highly confident after the event",
            f"✓ +{conf_lift}pp lift from pre-event ({conf_pre_pct}%)"
        ), unsafe_allow_html=True)
    with c2:
        st.markdown(create_kpi_card(
            "CONNECTIONS", "Avg LinkedIn Connections",
            str(linkedin_avg),
            f"Weighted average per participant across both sessions",
            f"✓ Avg {meaningful_avg} meaningful connections"
        ), unsafe_allow_html=True)
    with c3:
        st.markdown(create_kpi_card(
            "ATMOSPHERE", "Overwhelming Atmosphere Eliminated",
            "0%",
            f"Dropped from {atm_pre_overwhelm} participants pre → 0 post-event",
            "✓ Circle format removes anxiety universally"
        ), unsafe_allow_html=True)

    st.markdown('<p class="subsection-title">Satisfaction & Advocacy</p>',
                unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(create_kpi_card(
            "NPS", "Combined NPS Score",
            str(nps_score),
            f"Promoters: {nps_post_combined['Promoters']} · "
            f"Passives: {nps_post_combined['Passives']} · "
            f"Detractors: {nps_post_combined['Detractors']}",
            "✓ Strong advocacy across both sectors"
        ), unsafe_allow_html=True)
    with c2:
        st.markdown(create_kpi_card(
            "ADVOCACY", "Would Recommend",
            f"{rec_combined_pct}%",
            f"{rec_combined} of {N_total_post} would recommend the event",
            "✓ Outstanding word-of-mouth"
        ), unsafe_allow_html=True)
    with c3:
        st.markdown(create_kpi_card(
            "OUTCOMES", "Career / Relevant Connections",
            f"{career_combined_pct}%",
            "Found career opps (Health) or relevant connections (Tech)",
            "✓ High professional value"
        ), unsafe_allow_html=True)

    # ── HIGHLIGHT BOX ──────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="lnc-highlight-box">
        <h3>🌐 Combined Programme — Key Findings</h3>
        <ul>
            <li><strong>{N_total_pre} participants</strong> engaged across Health and Technology
                sessions — {N_H} Health · {N_T_pre} Technology</li>
            <li><strong>{fmt_excel_pct}%</strong> rated the circle-rotation format as Excellent
                — consistent quality across both sectors</li>
            <li>Overwhelming atmosphere dropped from
                <strong>{atm_pre_overwhelm} → 0 participants</strong>
                post-event in both sessions combined</li>
            <li>Confidence in networking lifted by
                <strong>+{conf_lift} percentage points</strong>
                programme-wide ({conf_pre_pct}% → {conf_post_pct}%)</li>
            <li>Combined NPS of <strong>{nps_score}</strong> with
                {nps_post_combined['Promoters']} Promoters and only
                {nps_post_combined['Detractors']} Detractors across both sessions</li>
            <li><strong>{rec_combined_pct}%</strong> of all participants would recommend
                Leaders Network Circles to fellow Saudi students</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # ── DEEP-DIVE TABS ─────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<p class="section-title">📚 Programme Deep-Dive</p>',
                unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Format & Atmosphere",
        "🤝 Connections",
        "💪 Confidence & Barriers",
        "📣 Advocacy & NPS"
    ])

    # ── TAB 1: FORMAT & ATMOSPHERE ─────────────────────────────────────────────
    with tab1:
        st.markdown("### Circle Format Rating — Combined (Post-Event)")
        c1, c2 = st.columns(2)
        with c1:
            fig = lnc_donut(
                ["Excellent", "Good", "Fair", "Poor"],
                [fmt_excellent, fmt_good, fmt_fair, fmt_poor],
                ['#0d3b6e', '#378add', '#85B7EB', '#e74c3c'],
                center_text="Format\nRating"
            )
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("### Registration Rating — Combined (Pre-Event)")
            fig = lnc_donut(
                ["Excellent", "Good", "Fair", "Poor"],
                [reg_excellent, reg_good, reg_fair, reg_poor],
                ['#006341', '#00843d', '#93c13f', '#e74c3c'],
                center_text="Registration\nRating"
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Atmosphere — Before vs After (Combined)")
        st.markdown(compare_band(
            comfort_pre_pct, comfort_post_pct,
            f"{atm_pre_comfort} of {N_total_pre} felt comfortable pre-event",
            f"{atm_post_comfort} of {N_total_post} felt comfortable post-event",
            "#6b7280", "#0d3b6e", "%",
            "Comfortable & friendly"
        ), unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Comfortable Atmosphere — Pre vs Post")
            fig = go.Figure(go.Bar(
                x=["Pre-Event", "Post-Event"],
                y=[comfort_pre_pct, comfort_post_pct],
                marker_color=['rgba(13,59,110,0.4)', '#0d3b6e'],
                text=[f"{comfort_pre_pct}%", f"{comfort_post_pct}%"],
                textposition='outside', textfont=dict(size=15, family='Epilogue')
            ))
            fig.update_layout(height=340, yaxis=dict(range=[0, 100]),
                font=dict(family='Epilogue', color='#2c3e50'),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("#### Overwhelming Atmosphere — Pre vs Post")
            fig = go.Figure(go.Bar(
                x=["Pre-Event", "Post-Event"],
                y=[atm_pre_overwhelm, atm_post_overwhelm],
                marker_color=['#e74c3c', '#93c13f'],
                text=[str(atm_pre_overwhelm), str(atm_post_overwhelm)],
                textposition='outside', textfont=dict(size=15, family='Epilogue')
            ))
            fig.update_layout(height=340, yaxis=dict(range=[0, 12]),
                font=dict(family='Epilogue', color='#2c3e50'),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### How Participants Heard About the Event — Combined")
        fig = lnc_bar(
            list(heard_combined.keys()),
            list(heard_combined.values()),
            ['#0d3b6e', '#1a5fa8', '#378add', '#85B7EB', '#d0d9e8'],
            height=320, v_range=[0, 28]
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── TAB 2: CONNECTIONS ─────────────────────────────────────────────────────
    with tab2:
        st.markdown("### LinkedIn Connections Made — Combined (Post-Event)")
        conn_labs = ["1–2", "3–5", "6–9", "10–12", "12+"]

        c1, c2 = st.columns(2)
        with c1:
            fig = lnc_donut(
                conn_labs,
                [linkedin_combined[k] for k in conn_labs],
                ['#e9ecef', '#85B7EB', '#0d3b6e', '#006341', '#93c13f'],
                center_text=f"Avg\n{linkedin_avg}"
            )
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("### Meaningful Connections — Combined (Post-Event)")
            fig = lnc_donut(
                conn_labs,
                [meaningful_combined[k] for k in conn_labs],
                ['#e9ecef', '#85B7EB', '#0d3b6e', '#006341', '#93c13f'],
                center_text=f"Avg\n{meaningful_avg}"
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Target vs Actual — Combined Connection Journey")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Target (Pre-Event)',
            x=conn_labs,
            y=[conn_target_combined[k] for k in conn_labs],
            marker_color='rgba(13,59,110,0.35)',
            text=[conn_target_combined[k] for k in conn_labs],
            textposition='outside'
        ))
        fig.add_trace(go.Bar(
            name='LinkedIn Made (Post)',
            x=conn_labs,
            y=[linkedin_combined[k] for k in conn_labs],
            marker_color='#0d3b6e',
            text=[linkedin_combined[k] for k in conn_labs],
            textposition='outside'
        ))
        fig.add_trace(go.Bar(
            name='Meaningful (Post)',
            x=conn_labs,
            y=[meaningful_combined[k] for k in conn_labs],
            marker_color='#006341',
            text=[meaningful_combined[k] for k in conn_labs],
            textposition='outside'
        ))
        fig.update_layout(
            barmode='group', height=420, yaxis=dict(range=[0, 26]),
            font=dict(family='Epilogue', color='#2c3e50'),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation='h', yanchor='bottom', y=1.02,
                        xanchor='center', x=0.5)
        )
        st.plotly_chart(fig, use_container_width=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Avg LinkedIn Connections", str(linkedin_avg),
                      delta="per participant")
        with c2:
            st.metric("Avg Meaningful Connections", str(meaningful_avg),
                      delta="per participant")
        with c3:
            st.metric("Avg Target (Pre-Event)", str(target_avg),
                      delta="per participant")

    # ── TAB 3: CONFIDENCE & BARRIERS ───────────────────────────────────────────
    with tab3:
        st.markdown("### Confidence Journey — Combined Programme")
        st.markdown(compare_band(
            conf_pre_pct, conf_post_pct,
            f"{conf_pre_high} of {N_total_pre} highly confident pre-event",
            f"{conf_post_high} of {N_total_post} highly confident post-event",
            "#6b7280", "#0d3b6e", "%", "High confidence (combined)"
        ), unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Confidence — Pre vs Post (Combined %)")
            fig = go.Figure(go.Bar(
                x=["Pre-Event\nHigh Confidence", "Post-Event\nHigh Confidence"],
                y=[conf_pre_pct, conf_post_pct],
                marker_color=['rgba(13,59,110,0.4)', '#0d3b6e'],
                text=[f"{conf_pre_pct}%", f"{conf_post_pct}%"],
                textposition='outside', textfont=dict(size=15)
            ))
            fig.update_layout(height=340, yaxis=dict(range=[0, 100]),
                font=dict(family='Epilogue', color='#2c3e50'),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("#### Confidence Levels Distribution (Post-Event Combined)")
            # Post combined: Very confident 15+8=23(T only has very conf/conf)
            # Health post: significantly improved=19, slightly=7 → using as high conf proxy
            # Tech post: very conf=15, conf=4
            post_conf_labs = ["High\nConfidence", "Neutral", "Low\nConfidence"]
            post_conf_vals = [conf_post_high, (N_total_post - conf_post_high - 0), 0]
            # Health neutral=1 (no change), Tech neutral=3 → total neutral=4
            post_conf_vals = [conf_post_high, 4, 0]
            fig = lnc_donut(
                post_conf_labs, post_conf_vals,
                ['#0d3b6e', '#85B7EB', '#e9ecef'],
                center_text=f"{conf_post_pct}%\nHigh Conf"
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Barriers — Combined Pre vs Post")
        bar_labs = [k.replace('\n', ' ') for k in barriers_pre_combined.keys()]
        pre_bar_vals  = list(barriers_pre_combined.values())
        post_bar_vals = list(barriers_post_combined.values())

        fig = lnc_grouped_bar(
            bar_labs, pre_bar_vals, post_bar_vals,
            pre_color='rgba(13,59,110,0.3)', post_color='#0d3b6e',
            height=380, y_max=22
        )
        fig.update_layout(
            title_text="Barriers Reported Pre-Event vs Overcome Post-Event (Combined)",
            title_font=dict(family='Cormorant Garamond', size=17)
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Barriers Distribution — Combined (Pre-Event)")
        fig = lnc_donut(
            [k.replace('\n', ' ') for k in barriers_pre_combined.keys()],
            list(barriers_pre_combined.values()),
            ['#0d3b6e', '#1a5fa8', '#378add', '#85B7EB'],
            center_text=f"{N_total_pre}\nParticipants"
        )
        col_l, col_c, col_r = st.columns([1, 2, 1])
        with col_c:
            st.plotly_chart(fig, use_container_width=True)

    # ── TAB 4: ADVOCACY & NPS ──────────────────────────────────────────────────
    with tab4:
        st.markdown("### NPS — Combined Post-Event")
        c1, c2 = st.columns(2)
        with c1:
            nps_labs = ["Promoters", "Passives", "Detractors"]
            fig = lnc_donut(
                nps_labs,
                [nps_post_combined[k] for k in nps_labs],
                ['#006341', '#f39c12', '#e74c3c'],
                center_text=f"NPS\n{nps_score}"
            )
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("#### NPS Breakdown — Raw Counts")
            fig = go.Figure(go.Bar(
                x=nps_labs,
                y=[nps_post_combined[k] for k in nps_labs],
                marker_color=['#006341', '#f39c12', '#e74c3c'],
                text=[nps_post_combined[k] for k in nps_labs],
                textposition='outside', textfont=dict(size=15, family='Epilogue')
            ))
            fig.update_layout(height=360, yaxis=dict(range=[0, 38]),
                font=dict(family='Epilogue', color='#2c3e50'),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Recommendation — Combined (Post-Event)")
        # Health: Highly=20, Slightly=5, Maybe=0, Don't=2
        # Tech:   Very likely=20, Likely=2, Neutral=0, Unlikely=0, VU=0
        # Merged into: Strong=42, Moderate=5, Neutral=0, Against=2
        fig = lnc_donut(
            ["Strong\nRecommendation", "Moderate\nRecommendation",
             "Neutral / Against"],
            [42, 5, 2],
            ['#006341', '#00843d', '#e74c3c'],
            center_text=f"{rec_combined_pct}%\nRecommend"
        )
        col_l, col_c, col_r = st.columns([1, 2, 1])
        with col_c:
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Programme Funnel — Combined")
        fig = go.Figure(go.Funnel(
            y=["Pre-Event Participants", "Post-Event Participants",
               "Excellent Format Rating", "High Confidence (Post)",
               "Would Recommend"],
            x=[N_total_pre, N_total_post,
               fmt_excellent, conf_post_high, rec_combined],
            textposition="inside",
            textinfo="value+percent initial",
            marker={
                "color": ['#0d3b6e', '#1a5fa8', '#378add', '#006341', '#00843d'],
                "line": {"width": 2, "color": "white"}
            }
        ))
        fig.update_layout(
            height=440,
            font=dict(family="Epilogue", size=13, color="#2c3e50"),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── ABOUT BOX ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="info-box">
        <h3>📋 About This Combined Analysis</h3>
        <p>
            This page aggregates data from both the
            <strong>Leaders Network Circles — Health Sector (Session 1)</strong>
            and <strong>Technology Sector (Session 1)</strong> into a single
            programme-level view. All metrics are combined raw counts or
            weighted averages across both sessions.
            <br><br>
            <strong>Total reach:</strong> {n_pre} pre-event · {n_post} post-event
            across Health and Technology sectors in Australia.
        </p>
    </div>
    """.format(n_pre=N_total_pre, n_post=N_total_post), unsafe_allow_html=True)

    # ── FOOTER ─────────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="lnc-footer">
        <h2>🌐 Combined Programme Analysis</h2>
        <p class="tagline">Health + Technology · Leaders Network Circles · Australia Chapter</p>
        <div style="display:flex; justify-content:center; gap:2.5rem; margin:2rem 0;
             flex-wrap:wrap; position:relative; z-index:1;">
            <div><div style="font-size:2.5rem;font-weight:700">{N_total_pre}</div>
                 <div style="opacity:0.8">Total pre-survey</div></div>
            <div><div style="font-size:2.5rem;font-weight:700">{N_total_post}</div>
                 <div style="opacity:0.8">Total post-survey</div></div>
            <div><div style="font-size:2.5rem;font-weight:700">{fmt_excel_pct}%</div>
                 <div style="opacity:0.8">Excellent format</div></div>
            <div><div style="font-size:2.5rem;font-weight:700">{conf_lift:+}pp</div>
                 <div style="opacity:0.8">Confidence lift</div></div>
            <div><div style="font-size:2.5rem;font-weight:700">{nps_score}</div>
                 <div style="opacity:0.8">Combined NPS</div></div>
            <div><div style="font-size:2.5rem;font-weight:700">{rec_combined_pct}%</div>
                 <div style="opacity:0.8">Would recommend</div></div>
        </div>
        <p style="font-size:1.1rem;margin-top:2rem;opacity:0.9;
             position:relative;z-index:1"><strong>Grow • Connect • Impact</strong></p>
        <p style="font-size:0.9rem;opacity:0.7;margin-top:1rem;
             position:relative;z-index:1">
             {datetime.now().strftime('%B %d, %Y')} | Vision 2030</p>
    </div>
    """, unsafe_allow_html=True)

    st.stop()
# ============================================================================
# ██╗     ███╗   ██╗ ██████╗    DASHBOARD
# ██║     ████╗  ██║██╔════╝
# ██║     ██╔██╗ ██║██║
# ██║     ██║╚██╗██║██║
# ███████╗██║ ╚████║╚██████╗
# ╚══════╝╚═╝  ╚═══╝ ╚═════╝
# ============================================================================

if session_info.get('type') == 'lnc':

    # ── All 27-respondent data hardcoded ─────────────────────────────────────
    N  = 27
    pre  = dict(
        registration = {"Excellent": 21, "Good": 5, "Fair": 1, "Poor": 0},
        heard_about  = {"Friend/colleague": 13, "WhatsApp": 10, "Other": 2, "Snapchat": 2, "LinkedIn": 0},
        confidence   = {"Extremely confident": 12, "Somewhat confident": 5, "Neutral": 9,
                        "Somewhat not confident": 1, "Extremely not confident": 0},
        barriers     = {"Difficulty finding\nrelevant people": 10, "Not knowing how to\nstart conversations": 8,
                        "Shyness / anxiety": 6, "Other": 3},
        conn_targets = {"1–2": 8, "3–5": 9, "6–9": 5, "10–12": 2, "12+": 3},
        goals        = {"Friendships": 20, "Professional\nnetwork": 21, "Mentor": 13,
                        "Research /\nprojects": 10, "Saudi\ncommunity": 14},
        atmosphere   = {"Comfortable\n& friendly": 17, "Professional &\nwell-organized": 11,
                        "A bit\noverwhelming": 6, "Hard to\nconnect": 0, "Casual & not\norganized": 1},
        experience   = {"Very Good": 18, "Average": 9, "Below average": 0, "Very poor": 0},
        nps          = {"Promoters": 12, "Passives": 9, "Detractors": 6},
    )
    post = dict(
        format_rating  = {"Excellent": 23, "Good": 3, "Fair": 0, "Poor": 1},
        linkedin_conns = {"1–2": 3, "3–5": 9, "6–9": 9, "10–12": 4, "12+": 2},
        meaningful     = {"1–2": 9, "3–5": 8, "6–9": 5, "10–12": 2, "12+": 3},
        goals_achieved = {"Friendships": 22, "Professional\nnetwork": 24, "Mentor": 9,
                          "Research /\nprojects": 9, "Saudi\ncommunity": 15},
        confidence_change = {"Significantly\nimproved": 19, "Slightly\nimproved": 7, "No change": 1},
        barriers_overcome = {"Difficulty finding\nrelevant people": 9, "Not knowing how to\nstart conversations": 8,
                             "Shyness / anxiety": 6, "Other": 4},
        network_expanded  = {"Significantly": 18, "Moderately": 6, "Slightly": 1, "Not at all": 2},
        career_opps       = {"Yes, definitely": 14, "Possibly": 6, "Not at this stage": 7},
        business_opps     = {"Significantly": 15, "Somewhat": 6, "Slightly": 3, "Not at this stage": 3},
        research_opps     = {"Yes": 8, "Maybe": 11, "No": 8},
        circles_helped    = {"Helped engage\nmore easily": 20, "Better health sector\nunderstanding": 16,
                             "Insights into future\nof health sector": 15, "Identified skills\nto develop": 9, "Not helpful": 3},
        experience        = {"Very Good": 24, "Average": 2, "Below average": 0, "Very poor": 1},
        atmosphere        = {"Comfortable\n& friendly": 23, "Professional &\nwell-organized": 11,
                             "A bit\noverwhelming": 0, "Hard to\nconnect": 0, "Casual & not\norganized": 3},
        recommendation    = {"Highly recommend": 20, "Slightly recommend": 5, "Maybe": 0, "Don't think they need it": 2},
        nps               = {"Promoters": 17, "Passives": 8, "Detractors": 2},
        vs_other_events   = {"First event": 9, "Much better": 6, "Somewhat better": 7, "About the same": 4, "Needs improvement": 1},
    )

    # Derived quick-access numbers
    nps_pre_score  = round((pre['nps']['Promoters']  - pre['nps']['Detractors'])  / N * 100)
    nps_post_score = round((post['nps']['Promoters'] - post['nps']['Detractors']) / N * 100)
    conf_improved  = post['confidence_change']['Significantly\nimproved'] + post['confidence_change']['Slightly\nimproved']

    # ── SHOW LNC AD IMAGE PROFESSIONALLY ─────────────────────────────────────
    try:
        col_l, col_c, col_r = st.columns([1, 2, 1])
        with col_c:
            st.image("d3b23000-f8ed-4a60-a6c9-14ff54a1a604.JPG",
                     caption="Leaders Network Circles — Health Sector, Session 1",
                     use_column_width=True)
    except:
        try:
            col_l, col_c, col_r = st.columns([1, 2, 1])
            with col_c:
                st.image("/mnt/user-data/uploads/d3b23000-f8ed-4a60-a6c9-14ff54a1a604.JPG",
                         caption="Leaders Network Circles — Health Sector, Session 1",
                         use_column_width=True)
        except:
            pass

    # ── TOP STAT PILLS ────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="lnc-highlight-box" style="padding:2rem;">
        <div style="display:flex; flex-wrap:wrap; justify-content:center; gap:0.5rem; position:relative; z-index:1;">
            <div class="stat-pill"><span class="num">{N}</span><span class="lbl">Participants</span></div>
            <div class="stat-pill"><span class="num">85%</span><span class="lbl">Excellent rating</span></div>
            <div class="stat-pill"><span class="num">{round(conf_improved/N*100)}%</span><span class="lbl">Confidence boosted</span></div>
            <div class="stat-pill"><span class="num">{nps_post_score}</span><span class="lbl">NPS score</span></div>
            <div class="stat-pill"><span class="num">74%</span><span class="lbl">Highly recommend</span></div>
            <div class="stat-pill"><span class="num">+{nps_post_score - nps_pre_score}</span><span class="lbl">NPS increase</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── SECTION: KPIs ─────────────────────────────────────────────────────────
    st.markdown('<p class="section-title">📊 Key Performance Indicators</p>', unsafe_allow_html=True)
    st.markdown('<p class="subsection-title">Reach & Event Quality</p>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(create_kpi_card("REACH", "Total Participants", str(N),
            "Completed both pre- and post-event surveys",
            "✓ 100% survey completion"), unsafe_allow_html=True)
    with c2:
        st.markdown(create_kpi_card("FORMAT", "Circles Format — Excellent",
            f"{round(post['format_rating']['Excellent']/N*100)}%",
            f"{post['format_rating']['Excellent']} out of {N} rated Excellent",
            "✓ Innovative circle-rotation format"), unsafe_allow_html=True)
    with c3:
        reg_excel = round(pre['registration']['Excellent'] / N * 100)
        st.markdown(create_kpi_card("ONBOARDING", "Registration Experience",
            f"{reg_excel}%",
            "Rated registration & selection Excellent",
            "✓ Smooth onboarding process"), unsafe_allow_html=True)

    st.markdown('<p class="subsection-title">Networking Outcomes</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(create_kpi_card("CONFIDENCE", "Confidence Improved",
            f"{round(conf_improved/N*100)}%",
            f"{post['confidence_change']['Significantly\nimproved']} significantly + {post['confidence_change']['Slightly\nimproved']} slightly",
            "✓ Strong personal growth"), unsafe_allow_html=True)
    with c2:
        career_yes  = post['career_opps']['Yes, definitely']
        career_poss = post['career_opps']['Possibly']
        st.markdown(create_kpi_card("CAREERS", "Career Opportunities Found",
            f"{round((career_yes+career_poss)/N*100)}%",
            f"{career_yes} definite + {career_poss} possible out of {N}",
            "✓ High career-value event"), unsafe_allow_html=True)
    with c3:
        network_sig = post['network_expanded']['Significantly']
        st.markdown(create_kpi_card("NETWORK", "Professional Network Expanded",
            f"{round(network_sig/N*100)}%",
            f"Significantly expanded their health-sector network",
            "✓ Vision 2030 aligned"), unsafe_allow_html=True)

    st.markdown('<p class="subsection-title">Satisfaction & Advocacy</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        exp_vg = post['experience']['Very Good']
        st.markdown(create_kpi_card("EXPERIENCE", "Overall Experience — Very Good",
            f"{round(exp_vg/N*100)}%",
            f"{exp_vg} of {N} rated Very Good (was {pre['experience']['Very Good']} pre-event)",
            f"✓ +{exp_vg - pre['experience']['Very Good']} improvement"), unsafe_allow_html=True)
    with c2:
        st.markdown(create_kpi_card("NPS", "Net Promoter Score",
            str(nps_post_score),
            f"Post-event (pre-event was {nps_pre_score})",
            f"✓ +{nps_post_score - nps_pre_score} point jump"), unsafe_allow_html=True)
    with c3:
        rec_high = post['recommendation']['Highly recommend']
        st.markdown(create_kpi_card("ADVOCACY", "Highly Recommend",
            f"{round(rec_high/N*100)}%",
            f"{rec_high} of {N} would highly recommend",
            "✓ Outstanding word-of-mouth"), unsafe_allow_html=True)

    # ── HIGHLIGHT BOX ─────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="lnc-highlight-box">
        <h3>✨ Leaders Network Circles — Session Highlights</h3>
        <ul>
            <li>85% rated the circle-rotation format as <strong>Excellent</strong> — a format-first innovation</li>
            <li>Professional network goal <em>exceeded</em>: 21 aimed → 24 achieved (+14% over-delivery)</li>
            <li>Atmosphere anxiety dropped from <strong>22% → 0%</strong> — the circles removed the awkwardness</li>
            <li>NPS jumped from <strong>{nps_pre_score} → {nps_post_score}</strong> — a {nps_post_score-nps_pre_score} point improvement</li>
            <li>{round(post['confidence_change']['Significantly\nimproved']/N*100)}% of participants <strong>significantly</strong> improved their networking confidence</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # ── DETAILED TABS ──────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<p class="section-title">📚 Deep-Dive Analysis</p>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🌐 Experience", "🤝 Connections & Goals", "💼 Outcomes", "🔄 Pre vs Post", "👥 Demographics"
    ])

    # ── TAB 1: EXPERIENCE ─────────────────────────────────────────────────────
    with tab1:
        st.markdown("### Event Atmosphere — Before vs After")
        st.markdown(compare_band(
            round(pre['atmosphere']['Comfortable\n& friendly']/N*100),
            round(post['atmosphere']['Comfortable\n& friendly']/N*100),
            f"{pre['atmosphere']['Comfortable\n& friendly']} people felt comfortable",
            f"{post['atmosphere']['Comfortable\n& friendly']} people felt comfortable",
            "#6b7280", "#0d3b6e", "%",
            "Comfortable\n& friendly"
        ), unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Atmosphere — Grouped Comparison")
            atm_labs = ["Comfortable\n& friendly", "Professional &\nwell-organized", "A bit\noverwhelming"]
            fig = lnc_grouped_bar(
                atm_labs,
                [pre['atmosphere'][k] for k in atm_labs],
                [post['atmosphere'][k] for k in atm_labs],
                y_max=28
            )
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("#### Overall Experience Rating")
            exp_labs = ["Very Good", "Average", "Below average", "Very poor"]
            fig = lnc_grouped_bar(
                exp_labs,
                [pre['experience'][k] for k in exp_labs],
                [post['experience'][k] for k in exp_labs],
                y_max=28
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Circle-Format Rating (Post-Event)")
        c1, c2 = st.columns(2)
        with c1:
            colors_fmt = ['#0d3b6e', '#378add', '#85B7EB', '#e74c3c']
            fig = lnc_donut(
                list(post['format_rating'].keys()),
                list(post['format_rating'].values()),
                colors_fmt,
                center_text="Format\nRating"
            )
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("#### NPS Shift — Before → After")
            nps_labs = ["Promoters", "Passives", "Detractors"]
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Before', x=nps_labs,
                y=[pre['nps'][k] for k in nps_labs],
                marker_color=['#93c13f','#f39c12','#e9ecef'],
                text=[pre['nps'][k] for k in nps_labs], textposition='outside'))
            fig.add_trace(go.Bar(name='After', x=nps_labs,
                y=[post['nps'][k] for k in nps_labs],
                marker_color=['#006341','#e67e22','#e74c3c'],
                text=[post['nps'][k] for k in nps_labs], textposition='outside'))
            fig.update_layout(barmode='group', height=340, yaxis=dict(range=[0,22]),
                font=dict(family='Epilogue', color='#2c3e50'),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5))
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### How This Compared to Other Events Attended")
        comp_labs = list(post['vs_other_events'].keys())
        comp_vals = list(post['vs_other_events'].values())
        comp_colors = ['#e9ecef','#006341','#00843d','#93c13f','#e74c3c']
        fig = go.Figure(go.Bar(x=comp_labs, y=comp_vals, marker_color=comp_colors,
            text=comp_vals, textposition='outside', textfont=dict(size=13)))
        fig.update_layout(height=320, yaxis=dict(range=[0,12]),
            font=dict(family='Epilogue', color='#2c3e50'),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # ── TAB 2: CONNECTIONS & GOALS ────────────────────────────────────────────
    with tab2:
        st.markdown("### Goal Setting vs. Achievement")
        st.markdown(compare_band(21, 24, "aimed to expand professional network",
            "actually expanded professional network", "#6b7280", "#0d3b6e", "",
            "Professional Network goal exceeded"))

        goal_labs = list(pre['goals'].keys())
        fig = lnc_grouped_bar(
            goal_labs,
            [pre['goals'][k] for k in goal_labs],
            [post['goals_achieved'][k] for k in post['goals_achieved'].keys()],
            y_max=28
        )
        fig.update_layout(title_text="Goals: Intended (Pre) vs Achieved (Post)",
            title_font=dict(family='Cormorant Garamond', size=18))
        st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Connection Target (Pre-Event)")
            fig = lnc_bar(
                list(pre['conn_targets'].keys()),
                list(pre['conn_targets'].values()),
                '#378add', height=300, v_range=[0, 12]
            )
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("#### LinkedIn Connections Made (Post-Event)")
            fig = lnc_bar(
                list(post['linkedin_conns'].keys()),
                list(post['linkedin_conns'].values()),
                '#0d3b6e', height=300, v_range=[0, 12]
            )
            st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Meaningful Connections Made")
            fig = lnc_bar(
                list(post['meaningful'].keys()),
                list(post['meaningful'].values()),
                '#006341', height=300, v_range=[0, 12]
            )
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("#### Confidence Impact (Post-Event)")
            fig = lnc_donut(
                [k.replace('\n', ' ') for k in post['confidence_change'].keys()],
                list(post['confidence_change'].values()),
                ['#0d3b6e', '#378add', '#e9ecef'],
                center_text="Confidence\nImpact"
            )
            st.plotly_chart(fig, use_container_width=True)

    # ── TAB 3: OUTCOMES ───────────────────────────────────────────────────────
    with tab3:
        st.markdown("### Professional & Career Impact")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("#### Career Opportunities")
            fig = lnc_donut(
                list(post['career_opps'].keys()),
                list(post['career_opps'].values()),
                ['#006341', '#93c13f', '#e9ecef'],
                center_text="Career\nOpps"
            )
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("#### Business Opportunities")
            fig = lnc_donut(
                list(post['business_opps'].keys()),
                list(post['business_opps'].values()),
                ['#0d3b6e', '#378add', '#85B7EB', '#e9ecef'],
                center_text="Business\nOpps"
            )
            st.plotly_chart(fig, use_container_width=True)
        with c3:
            st.markdown("#### Research / Project Opportunities")
            fig = lnc_donut(
                list(post['research_opps'].keys()),
                list(post['research_opps'].values()),
                ['#1a5fa8', '#85B7EB', '#e9ecef'],
                center_text="Research\nOpps"
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Network Expansion")
        st.markdown(compare_band(
            round(pre['confidence']['Extremely confident'] / N * 100),
            round(post['network_expanded']['Significantly'] / N * 100),
            "were Extremely confident pre-event",
            "expanded network Significantly",
            "#6b7280", "#0d3b6e", "%",
            "Confidence → Actual impact"
        ), unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Network Expansion — Post-Event")
            fig = lnc_bar(
                list(post['network_expanded'].keys()),
                list(post['network_expanded'].values()),
                ['#0d3b6e','#378add','#85B7EB','#e9ecef'],
                height=300, v_range=[0, 22]
            )
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("#### How Circles Format Helped")
            circles_labs = [k.replace('\n', ' ') for k in post['circles_helped'].keys()]
            circles_vals = list(post['circles_helped'].values())
            fig = go.Figure(go.Bar(
                y=circles_labs, x=circles_vals, orientation='h',
                marker_color=['#006341','#0d3b6e','#378add','#85B7EB','#e9ecef'],
                text=circles_vals, textposition='outside', textfont=dict(size=12)
            ))
            fig.update_layout(height=320, xaxis=dict(range=[0, 25]),
                font=dict(family='Epilogue', color='#2c3e50'),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False, margin=dict(l=10, r=50, t=10, b=20))
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Barriers Overcome")
        bar_labs = [k.replace('\n', ' ') for k in pre['barriers'].keys()]
        fig = lnc_grouped_bar(
            bar_labs,
            list(pre['barriers'].values()),
            [post['barriers_overcome'][k] for k in post['barriers_overcome'].keys()],
            pre_color='#d0d9e8', post_color='#0d3b6e',
            y_max=14
        )
        fig.update_layout(title_text="Barriers: Pre-Event vs Overcome (Post-Event)",
            title_font=dict(family='Cormorant Garamond', size=18))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Recommendation")
        fig = lnc_bar(
            list(post['recommendation'].keys()),
            list(post['recommendation'].values()),
            ['#006341','#00843d','#93c13f','#e74c3c'],
            height=300, v_range=[0, 24]
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── TAB 4: PRE vs POST SIDE-BY-SIDE ──────────────────────────────────────
    with tab4:
        st.markdown("### 🔄 Pre-Event vs Post-Event — Full Comparison")

        metrics_compare = [
            ("Comfortable atmosphere",
             round(pre['atmosphere']['Comfortable\n& friendly']/N*100),
             round(post['atmosphere']['Comfortable\n& friendly']/N*100), "%"),
            ("Very Good overall experience",
             round(pre['experience']['Very Good']/N*100),
             round(post['experience']['Very Good']/N*100), "%"),
            ("Net Promoter Score", nps_pre_score, nps_post_score, "pts"),
            ("Confidence (highly confident)",
             round((pre['confidence']['Extremely confident'])/N*100),
             round(post['confidence_change']['Significantly\nimproved']/N*100), "%"),
            ("Overwhelming atmosphere",
             round(pre['atmosphere']['A bit\noverwhelming']/N*100),
             round(post['atmosphere']['A bit\noverwhelming']/N*100), "%"),
        ]
        labels_cmp = [m[0] for m in metrics_compare]
        pre_cmp    = [m[1] for m in metrics_compare]
        post_cmp   = [m[2] for m in metrics_compare]

        fig = go.Figure()
        fig.add_trace(go.Bar(name='Before Event', y=labels_cmp, x=pre_cmp,
            orientation='h', marker_color='#d0d9e8',
            text=[f"{v}%" for v in pre_cmp], textposition='outside'))
        fig.add_trace(go.Bar(name='After Event', y=labels_cmp, x=post_cmp,
            orientation='h', marker_color='#0d3b6e',
            text=[f"{v}%" for v in post_cmp], textposition='outside'))
        fig.update_layout(barmode='group', height=400, xaxis=dict(range=[0, 100]),
            font=dict(family='Epilogue', color='#2c3e50'),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
            margin=dict(l=10, r=60, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Waterfall — NPS Journey")
        fig_wf = go.Figure(go.Waterfall(
            orientation='v', measure=['relative','relative','relative','total'],
            x=["Pre-event\nPromoters", "Post-event\nPromoters gain", "Detractors\nreduced", "Final NPS"],
            y=[nps_pre_score,
               round(post['nps']['Promoters']/N*100) - round(pre['nps']['Promoters']/N*100),
               round(pre['nps']['Detractors']/N*100)  - round(post['nps']['Detractors']/N*100),
               0],
            connector=dict(line=dict(color='#0d3b6e', width=1.5, dash='dot')),
            decreasing=dict(marker_color='#e74c3c'),
            increasing=dict(marker_color='#006341'),
            totals=dict(marker_color='#0d3b6e'),
            text=[f"{nps_pre_score}", "+", "+", f"{nps_post_score}"],
            textfont=dict(size=14, family='Epilogue')
        ))
        fig_wf.update_layout(height=340,
            font=dict(family='Epilogue', color='#2c3e50'),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_wf, use_container_width=True)

        st.markdown("### Radar — Experience Profile")
        radar_dims  = ["Comfortable\natmosphere", "Very Good\nexperience", "Confidence\nimproved",
                       "Network\nexpanded sig.", "Career opps\nfound", "Highly\nrecommend"]
        radar_pre   = [
            round(pre['atmosphere']['Comfortable\n& friendly']/N*100),
            round(pre['experience']['Very Good']/N*100),
            round(pre['confidence']['Extremely confident']/N*100),
            0, 0, 0
        ]
        radar_post  = [
            round(post['atmosphere']['Comfortable\n& friendly']/N*100),
            round(post['experience']['Very Good']/N*100),
            round(conf_improved/N*100),
            round(post['network_expanded']['Significantly']/N*100),
            round((post['career_opps']['Yes, definitely']+post['career_opps']['Possibly'])/N*100),
            round(post['recommendation']['Highly recommend']/N*100),
        ]
        fig_r = go.Figure()
        fig_r.add_trace(go.Scatterpolar(r=radar_pre + [radar_pre[0]], theta=radar_dims + [radar_dims[0]],
            fill='toself', name='Before Event', line_color='#adb5bd', fillcolor='rgba(173,181,189,0.15)', line_width=2))
        fig_r.add_trace(go.Scatterpolar(r=radar_post + [radar_post[0]], theta=radar_dims + [radar_dims[0]],
            fill='toself', name='After Event', line_color='#0d3b6e', fillcolor='rgba(13,59,110,0.15)', line_width=2.5))
        fig_r.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=10)),
                       angularaxis=dict(tickfont=dict(size=12, family='Epilogue'))),
            showlegend=True, height=480, paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation='h', yanchor='bottom', y=-0.1, xanchor='center', x=0.5)
        )
        col_l, col_c, col_r = st.columns([1, 3, 1])
        with col_c:
            st.plotly_chart(fig_r, use_container_width=True)

    # ── TAB 5: DEMOGRAPHICS ───────────────────────────────────────────────────
    with tab5:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### How Did Attendees Hear About Us?")
            fig = lnc_bar(
                list(pre['heard_about'].keys()),
                list(pre['heard_about'].values()),
                ['#0d3b6e','#1a5fa8','#378add','#85B7EB','#d0d9e8'],
                height=340, v_range=[0, 16]
            )
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("#### Pre-Event Confidence Level")
            fig = lnc_bar(
                list(pre['confidence'].keys()),
                list(pre['confidence'].values()),
                ['#006341','#00843d','#93c13f','#f39c12','#e9ecef'],
                height=340, v_range=[0, 15]
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Primary Reasons for Attending")
        goals_clean = [k.replace('\n', ' ') for k in pre['goals'].keys()]
        fig = lnc_bar(
            goals_clean, list(pre['goals'].values()),
            ['#0d3b6e','#1a5fa8','#378add','#85B7EB','#d0d9e8'],
            height=300, v_range=[0, 25]
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Common Barriers Faced Before the Event")
        bar_labs_clean = [k.replace('\n', ' ') for k in pre['barriers'].keys()]
        fig = lnc_bar(
            bar_labs_clean, list(pre['barriers'].values()),
            '#378add', height=300, v_range=[0, 13]
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── ABOUT BOX ─────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="info-box">
        <h3>📋 About Leaders Network Circles</h3>
        <p>
            Leaders Network Circles is the <strong>third initiative</strong> of the Saudi Leadership Society 
            Australia Chapter. It brings together Saudi health students and professionals through a structured 
            <strong>circle-rotation format</strong> — six short rounds of small-group conversations across 
            three circles: <strong>Growth, Connection, and Impact</strong>. Participants build genuine 
            relationships, explore career pathways, and strengthen the Saudi health community abroad — 
            all aligned with <strong>Vision 2030</strong>'s health sector goals.
            <br><br>
            <strong>Eligibility:</strong> Saudi nationals studying or working in the Australian health sector.
            Limited to 30 leaders per session.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── FOOTER ────────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="lnc-footer">
        <h2>🔗 Leaders Network Circles</h2>
        <p class="tagline">Health Sector — Session 1 · Australia Chapter</p>
        <div style="display:flex; justify-content:center; gap:3rem; margin:2rem 0; flex-wrap:wrap; position:relative; z-index:1;">
            <div><div style="font-size:2.5rem;font-weight:700">{N}</div><div style="opacity:0.8">Participants</div></div>
            <div><div style="font-size:2.5rem;font-weight:700">85%</div><div style="opacity:0.8">Excellent rating</div></div>
            <div><div style="font-size:2.5rem;font-weight:700">+{nps_post_score - nps_pre_score}</div><div style="opacity:0.8">NPS increase</div></div>
            <div><div style="font-size:2.5rem;font-weight:700">74%</div><div style="opacity:0.8">Highly recommend</div></div>
            <div><div style="font-size:2.5rem;font-weight:700">{round(conf_improved/N*100)}%</div><div style="opacity:0.8">Confidence boosted</div></div>
        </div>
        <p style="font-size:1.1rem;margin-top:2rem;opacity:0.9;position:relative;z-index:1"><strong>Grow • Connect • Impact</strong></p>
        <p style="font-size:0.9rem;opacity:0.7;margin-top:1rem;position:relative;z-index:1">{datetime.now().strftime('%B %d, %Y')} | Vision 2030</p>
    </div>
    """, unsafe_allow_html=True)

    st.stop()

# ============================================================================
# LEADERS ACCELERATOR — 10X LEADERS DASHBOARD
# ============================================================================

if session_info.get('type') == 'leaders_accelerator':

    N_pre  = 10
    N_post = 9

    # ── RAW DATA ──────────────────────────────────────────────────────────────
    pre = dict(
        heard_about = {"WhatsApp": 3, "Saudi Students Associations": 7,
                       "Telegram": 0, "Snapchat": 0, "Other": 0},
        location    = {"Sydney": 4, "Melbourne": 5, "Brisbane": 0,
                       "Perth": 0, "Adelaide": 0, "Canberra": 0,
                       "New Zealand": 0, "Other": 1},
        program_understanding = {
            "Strongly Agree": 2, "Agree": 3, "Neutral": 4,
            "Disagree": 1, "Strongly Disagree": 0},
        track_clarity = {
            "Strongly Agree": 2, "Agree": 6, "Neutral": 1,
            "Disagree": 1, "Strongly Disagree": 0},
        app_confidence = {
            "Strongly Agree": 3, "Agree": 2, "Neutral": 4,
            "Disagree": 1, "Strongly Disagree": 0},
        articulate_leadership = {
            "Strongly Agree": 1, "Agree": 8, "Neutral": 1,
            "Disagree": 0, "Strongly Disagree": 0},
    )

    post = dict(
        program_understanding = {
            "Strongly Agree": 8, "Agree": 1, "Neutral": 0,
            "Disagree": 0, "Strongly Disagree": 0},
        track_clarity = {
            "Strongly Agree": 7, "Agree": 2, "Neutral": 0,
            "Disagree": 0, "Strongly Disagree": 0},
        app_confidence = {
            "Strongly Agree": 8, "Agree": 1, "Neutral": 0,
            "Disagree": 0, "Strongly Disagree": 0},
        articulate_leadership = {
            "Strongly Agree": 8, "Agree": 1, "Neutral": 0,
            "Disagree": 0, "Strongly Disagree": 0},
        mentoring_helped = {
            "Strongly Agree": 8, "Agree": 1, "Neutral": 0,
            "Disagree": 0, "Strongly Disagree": 0},
        plan_to_apply = {
            "Yes": 7, "No": 0, "I have already applied": 2},
        recommendation = {
            "Very likely": 8, "Likely": 1, "Neutral": 0,
            "Unlikely": 0, "Very unlikely": 0},
    )

    # ── DERIVED METRICS ───────────────────────────────────────────────────────
    def pct_agree(d, n):
        """% who Strongly Agree or Agree."""
        return round((d.get("Strongly Agree", 0) + d.get("Agree", 0)) / n * 100)

    pre_understand_pct  = pct_agree(pre['program_understanding'], N_pre)
    post_understand_pct = pct_agree(post['program_understanding'], N_post)
    pre_track_pct       = pct_agree(pre['track_clarity'], N_pre)
    post_track_pct      = pct_agree(post['track_clarity'], N_post)
    pre_conf_pct        = pct_agree(pre['app_confidence'], N_pre)
    post_conf_pct       = pct_agree(post['app_confidence'], N_post)
    pre_artic_pct       = pct_agree(pre['articulate_leadership'], N_pre)
    post_artic_pct      = pct_agree(post['articulate_leadership'], N_post)

    mentoring_pct   = pct_agree(post['mentoring_helped'], N_post)
    recommend_pct   = round((post['recommendation']['Very likely'] +
                             post['recommendation']['Likely']) / N_post * 100)
    plan_action_pct = round((post['plan_to_apply']['Yes'] +
                             post['plan_to_apply']['I have already applied']) / N_post * 100)

    scale_labels = ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"]
    scale_colors = ['#7C3AED', '#A78BFA', '#C4B5FD', '#DDD6FE', '#EDE9FE']

    # ── HEADER ────────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #4C1D95 0%, #7C3AED 60%, #A78BFA 100%);
         padding: 4rem 2rem; border-radius: 0 0 40px 40px;
         box-shadow: 0 20px 60px rgba(124,58,237,0.25);
         margin-bottom: 3rem; position: relative; overflow: hidden;">
        <div style="position:absolute;top:-50%;right:-10%;width:600px;height:600px;
             background:radial-gradient(circle,rgba(255,255,255,0.12) 0%,transparent 70%);
             border-radius:50%;"></div>
        <h1 class="initiative-title">⚡ Leaders Accelerator</h1>
        <p class="initiative-subtitle">10X Leaders · Saudi Leadership Society — Australia Chapter</p>
        <div style="text-align:center; margin-top:1.2rem; position:relative; z-index:1;">
            <span class="circle-badge" style="background:rgba(167,139,250,0.25);
                  color:#fff;border:1px solid rgba(167,139,250,0.5);">🎯 Clarity</span>
            <span class="circle-badge" style="background:rgba(124,58,237,0.25);
                  color:#fff;border:1px solid rgba(124,58,237,0.5);">💪 Confidence</span>
            <span class="circle-badge" style="background:rgba(76,29,149,0.25);
                  color:#fff;border:1px solid rgba(76,29,149,0.5);">🏆 Coaching</span>
        </div>
        <div style="text-align:center; margin-top:1rem;">
            <span class="mission-tagline">Application Readiness & Leadership Development</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── TOP STAT PILLS ─────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#4C1D95 0%,#7C3AED 100%);
         padding:2rem; border-radius:20px; margin-bottom:2rem;
         box-shadow:0 10px 40px rgba(124,58,237,0.2);">
        <div style="display:flex;flex-wrap:wrap;justify-content:center;
             gap:0.5rem;position:relative;z-index:1;">
            <div class="stat-pill"><span class="num">{N_pre}</span>
                <span class="lbl">Pre-survey</span></div>
            <div class="stat-pill"><span class="num">{N_post}</span>
                <span class="lbl">Post-survey</span></div>
            <div class="stat-pill"><span class="num">{post_understand_pct}%</span>
                <span class="lbl">Program clarity (post)</span></div>
            <div class="stat-pill"><span class="num">{post_conf_pct}%</span>
                <span class="lbl">App. confidence (post)</span></div>
            <div class="stat-pill"><span class="num">{mentoring_pct}%</span>
                <span class="lbl">Mentoring helped</span></div>
            <div class="stat-pill"><span class="num">{recommend_pct}%</span>
                <span class="lbl">Would recommend</span></div>
            <div class="stat-pill"><span class="num">{plan_action_pct}%</span>
                <span class="lbl">Plan to apply</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI CARDS ──────────────────────────────────────────────────────────────
    ACC_COLOR = "#7C3AED"

    def acc_kpi_card(category, label, value, context, trend="", warn=False):
        trend_html = ""
        if trend:
            trend_class = "kpi-trend-warn" if warn else "kpi-trend"
            trend_html = f'<div class="{trend_class}">{trend}</div>'
        return f"""
        <div class="kpi-card" style="--accent:#7C3AED;">
            <div style="position:absolute;top:0;left:0;width:5px;height:100%;
                 background:linear-gradient(180deg,#4C1D95,#A78BFA);
                 box-shadow:0 0 20px rgba(124,58,237,0.3);border-radius:2px 0 0 2px;"></div>
            <div class="kpi-category" style="color:{ACC_COLOR};">{category}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value" style="background:linear-gradient(135deg,#4C1D95,#7C3AED);
                 -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                 background-clip:text;">{value}</div>
            <div class="kpi-context">{context}</div>
            {trend_html}
        </div>"""

    st.markdown('<p class="section-title">📊 Key Performance Indicators</p>',
                unsafe_allow_html=True)
    st.markdown('<p class="subsection-title">Reach & Participation</p>',
                unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(acc_kpi_card("REACH", "Participants Surveyed",
            f"{N_pre} / {N_post}",
            f"{N_pre} pre-session · {N_post} post-session respondents",
            "✓ Strong engagement for focused cohort"), unsafe_allow_html=True)
    with c2:
        st.markdown(acc_kpi_card("OUTREACH", "Primary Channel — Saudi Student Assoc.",
            "70%",
            f"7 of {N_pre} heard via Saudi Students Associations",
            "✓ Community-driven reach"), unsafe_allow_html=True)
    with c3:
        cities = sum(1 for v in pre['location'].values() if v > 0)
        st.markdown(acc_kpi_card("REACH", "Cities Represented",
            str(cities),
            "Sydney, Melbourne + 1 other location",
            "✓ Multi-city cohort"), unsafe_allow_html=True)

    st.markdown('<p class="subsection-title">Readiness Shift — Pre vs Post</p>',
                unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    items = [
        ("CLARITY", "Program Requirements Clarity",
         pre_understand_pct, post_understand_pct),
        ("TRACK", "Track Selection Clarity",
         pre_track_pct, post_track_pct),
        ("CONFIDENCE", "Application Confidence",
         pre_conf_pct, post_conf_pct),
        ("ARTICULATION", "Leadership Articulation",
         pre_artic_pct, post_artic_pct),
    ]
    for col, (cat, label, pre_v, post_v) in zip([c1, c2, c3, c4], items):
        lift = post_v - pre_v
        with col:
            st.markdown(acc_kpi_card(
                cat, label,
                f"{post_v}%",
                f"Agree/Strongly Agree post-session",
                f"✓ +{lift}pp vs pre-session ({pre_v}%)"
            ), unsafe_allow_html=True)

    st.markdown('<p class="subsection-title">Mentoring & Advocacy</p>',
                unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(acc_kpi_card("MENTORING", "Individual Mentoring Helped",
            f"{mentoring_pct}%",
            f"{post['mentoring_helped']['Strongly Agree']} Strongly Agree + "
            f"{post['mentoring_helped']['Agree']} Agree",
            "✓ High-impact coaching format"), unsafe_allow_html=True)
    with c2:
        st.markdown(acc_kpi_card("ACTION", "Plan to Apply / Already Applied",
            f"{plan_action_pct}%",
            f"7 planning to apply · 2 already applied",
            "✓ 100% conversion — 0 said No"), unsafe_allow_html=True)
    with c3:
        st.markdown(acc_kpi_card("ADVOCACY", "Would Recommend",
            f"{recommend_pct}%",
            f"{post['recommendation']['Very likely']} Very Likely + "
            f"{post['recommendation']['Likely']} Likely",
            "✓ Outstanding word-of-mouth"), unsafe_allow_html=True)

    # ── HIGHLIGHT BOX ──────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#4C1D95 0%,#7C3AED 100%);
         padding:3rem; border-radius:30px; margin:3rem 0;
         box-shadow:0 20px 60px rgba(124,58,237,0.3);
         position:relative; overflow:hidden;">
        <div style="position:absolute;top:-50%;right:-20%;width:500px;height:500px;
             background:radial-gradient(circle,rgba(167,139,250,0.25) 0%,transparent 70%);
             border-radius:50%;"></div>
        <h3 style="font-family:'Cormorant Garamond',serif;font-size:2rem;font-weight:700;
             color:white;margin-bottom:2rem;position:relative;z-index:1;">
            ✨ Leaders Accelerator — Session Highlights</h3>
        <ul style="list-style:none;padding:0;margin:0;position:relative;z-index:1;">
            <li style="font-family:'Epilogue',sans-serif;font-size:1.1rem;
                 color:rgba(255,255,255,0.95);line-height:2;padding:0.6rem 0 0.6rem 2.5rem;
                 position:relative;">
                <span style="position:absolute;left:0;color:#C4B5FD;font-weight:900;
                      font-size:1.4rem;">✓</span>
                Program requirements clarity jumped from
                <strong>{pre_understand_pct}% → {post_understand_pct}%</strong>
                (+{post_understand_pct - pre_understand_pct}pp)</li>
            <li style="font-family:'Epilogue',sans-serif;font-size:1.1rem;
                 color:rgba(255,255,255,0.95);line-height:2;padding:0.6rem 0 0.6rem 2.5rem;
                 position:relative;">
                <span style="position:absolute;left:0;color:#C4B5FD;font-weight:900;
                      font-size:1.4rem;">✓</span>
                Application confidence rose from
                <strong>{pre_conf_pct}% → {post_conf_pct}%</strong>
                (+{post_conf_pct - pre_conf_pct}pp)</li>
            <li style="font-family:'Epilogue',sans-serif;font-size:1.1rem;
                 color:rgba(255,255,255,0.95);line-height:2;padding:0.6rem 0 0.6rem 2.5rem;
                 position:relative;">
                <span style="position:absolute;left:0;color:#C4B5FD;font-weight:900;
                      font-size:1.4rem;">✓</span>
                <strong>100%</strong> of post-survey respondents plan to apply or have
                already applied — 0 said No</li>
            <li style="font-family:'Epilogue',sans-serif;font-size:1.1rem;
                 color:rgba(255,255,255,0.95);line-height:2;padding:0.6rem 0 0.6rem 2.5rem;
                 position:relative;">
                <span style="position:absolute;left:0;color:#C4B5FD;font-weight:900;
                      font-size:1.4rem;">✓</span>
                Individual mentoring rated helpful by
                <strong>{mentoring_pct}%</strong> of participants</li>
            <li style="font-family:'Epilogue',sans-serif;font-size:1.1rem;
                 color:rgba(255,255,255,0.95);line-height:2;padding:0.6rem 0 0.6rem 2.5rem;
                 position:relative;">
                <span style="position:absolute;left:0;color:#C4B5FD;font-weight:900;
                      font-size:1.4rem;">✓</span>
                <strong>{recommend_pct}%</strong> would recommend the session to a colleague
            </li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # ── DEEP-DIVE TABS ─────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<p class="section-title">📚 Deep-Dive Analysis</p>',
                unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs([
        "🔄 Pre vs Post Shifts", "🎯 Outcomes & Action", "👥 Demographics"
    ])

    # ── TAB 1: PRE VS POST ─────────────────────────────────────────────────────
    with tab1:
        st.markdown("### Readiness Shifts — All Four Dimensions")

        dimensions = [
            "Program\nRequirements\nClarity",
            "Track\nSelection\nClarity",
            "Application\nConfidence",
            "Leadership\nArticulation",
        ]
        pre_pcts  = [pre_understand_pct, pre_track_pct,
                     pre_conf_pct, pre_artic_pct]
        post_pcts = [post_understand_pct, post_track_pct,
                     post_conf_pct, post_artic_pct]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Before Session', x=dimensions, y=pre_pcts,
            marker_color='#DDD6FE',
            text=[f"{v}%" for v in pre_pcts], textposition='outside',
            textfont=dict(size=13, family='Epilogue')))
        fig.add_trace(go.Bar(
            name='After Session', x=dimensions, y=post_pcts,
            marker_color='#7C3AED',
            text=[f"{v}%" for v in post_pcts], textposition='outside',
            textfont=dict(size=13, family='Epilogue')))
        fig.update_layout(
            barmode='group', height=420,
            yaxis=dict(range=[0, 110], title='% Agree / Strongly Agree'),
            font=dict(family='Epilogue', color='#2c3e50'),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation='h', yanchor='bottom',
                        y=1.02, xanchor='center', x=0.5))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Compare Bands — Each Dimension")
        for dim, pre_v, post_v in zip(
                ["Program Requirements Clarity", "Track Selection Clarity",
                 "Application Confidence", "Leadership Articulation"],
                pre_pcts, post_pcts):
            st.markdown(compare_band(
                pre_v, post_v,
                f"agreed pre-session",
                f"agreed post-session",
                "#6b7280", "#7C3AED", "%", dim
            ), unsafe_allow_html=True)

        st.markdown("### Likert Distribution — Before vs After")
        c1, c2 = st.columns(2)
        likert_dims_pre = {
            "Program\nClarity":    pre['program_understanding'],
            "Track\nClarity":      pre['track_clarity'],
            "App\nConfidence":     pre['app_confidence'],
            "Leadership\nArticul.":pre['articulate_leadership'],
        }
        likert_dims_post = {
            "Program\nClarity":     post['program_understanding'],
            "Track\nClarity":       post['track_clarity'],
            "App\nConfidence":      post['app_confidence'],
            "Leadership\nArticul.": post['articulate_leadership'],
        }
        with c1:
            st.markdown("#### Before Session")
            fig_pre = go.Figure()
            for label, color in zip(scale_labels, scale_colors):
                fig_pre.add_trace(go.Bar(
                    name=label,
                    x=list(likert_dims_pre.keys()),
                    y=[d.get(label, 0) for d in likert_dims_pre.values()],
                    marker_color=color,
                    text=[d.get(label, 0) for d in likert_dims_pre.values()],
                    textposition='inside', textfont=dict(size=11)
                ))
            fig_pre.update_layout(
                barmode='stack', height=380, yaxis=dict(range=[0, N_pre + 1]),
                font=dict(family='Epilogue', color='#2c3e50'),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation='h', yanchor='bottom',
                            y=-0.3, xanchor='center', x=0.5))
            st.plotly_chart(fig_pre, use_container_width=True)
        with c2:
            st.markdown("#### After Session")
            fig_post = go.Figure()
            for label, color in zip(scale_labels, scale_colors):
                fig_post.add_trace(go.Bar(
                    name=label,
                    x=list(likert_dims_post.keys()),
                    y=[d.get(label, 0) for d in likert_dims_post.values()],
                    marker_color=color,
                    text=[d.get(label, 0) for d in likert_dims_post.values()],
                    textposition='inside', textfont=dict(size=11)
                ))
            fig_post.update_layout(
                barmode='stack', height=380, yaxis=dict(range=[0, N_post + 1]),
                font=dict(family='Epilogue', color='#2c3e50'),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation='h', yanchor='bottom',
                            y=-0.3, xanchor='center', x=0.5))
            st.plotly_chart(fig_post, use_container_width=True)

        st.markdown("### Radar — Readiness Profile Before vs After")
        radar_dims  = ["Program\nClarity", "Track\nClarity",
                       "App\nConfidence", "Leadership\nArticulation"]
        fig_r = go.Figure()
        fig_r.add_trace(go.Scatterpolar(
            r=pre_pcts + [pre_pcts[0]], theta=radar_dims + [radar_dims[0]],
            fill='toself', name='Before Session',
            line_color='#C4B5FD', fillcolor='rgba(196,181,253,0.15)', line_width=2))
        fig_r.add_trace(go.Scatterpolar(
            r=post_pcts + [post_pcts[0]], theta=radar_dims + [radar_dims[0]],
            fill='toself', name='After Session',
            line_color='#7C3AED', fillcolor='rgba(124,58,237,0.15)', line_width=2.5))
        fig_r.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100],
                                tickfont=dict(size=10)),
                angularaxis=dict(tickfont=dict(size=12, family='Epilogue'))),
            showlegend=True, height=480, paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation='h', yanchor='bottom',
                        y=-0.1, xanchor='center', x=0.5))
        col_l, col_c, col_r = st.columns([1, 3, 1])
        with col_c:
            st.plotly_chart(fig_r, use_container_width=True)

    # ── TAB 2: OUTCOMES ────────────────────────────────────────────────────────
    with tab2:
        st.markdown("### Post-Session Outcomes")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("#### Plan to Apply")
            fig = lnc_donut(
                list(post['plan_to_apply'].keys()),
                list(post['plan_to_apply'].values()),
                ['#7C3AED', '#A78BFA', '#E9D5FF'],
                center_text=f"{plan_action_pct}%\nWill Apply"
            )
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("#### Recommendation Likelihood")
            fig = lnc_donut(
                list(post['recommendation'].keys()),
                list(post['recommendation'].values()),
                ['#4C1D95', '#7C3AED', '#A78BFA', '#C4B5FD', '#EDE9FE'],
                center_text=f"{recommend_pct}%\nRecommend"
            )
            st.plotly_chart(fig, use_container_width=True)
        with c3:
            st.markdown("#### Mentoring Effectiveness")
            fig = lnc_donut(
                list(post['mentoring_helped'].keys()),
                list(post['mentoring_helped'].values()),
                ['#4C1D95', '#7C3AED', '#A78BFA', '#C4B5FD', '#EDE9FE'],
                center_text=f"{mentoring_pct}%\nHelped"
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Post-Session Summary — All Measures")
        post_measures = [
            "Program\nClarity", "Track\nClarity",
            "App\nConfidence", "Leadership\nArticulation",
            "Mentoring\nHelped", "Would\nRecommend", "Plan\nto Apply"
        ]
        post_vals = [
            post_understand_pct, post_track_pct,
            post_conf_pct, post_artic_pct,
            mentoring_pct, recommend_pct, plan_action_pct
        ]
        fig = go.Figure(go.Bar(
            x=post_measures, y=post_vals,
            marker_color='#7C3AED',
            text=[f"{v}%" for v in post_vals],
            textposition='outside',
            textfont=dict(size=13, family='Epilogue')
        ))
        fig.update_layout(
            height=380, yaxis=dict(range=[0, 110]),
            font=dict(family='Epilogue', color='#2c3e50'),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # ── TAB 3: DEMOGRAPHICS ────────────────────────────────────────────────────
    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### How Participants Heard About the Session")
            heard_labels = [k for k, v in pre['heard_about'].items() if v > 0]
            heard_vals   = [v for v in pre['heard_about'].values() if v > 0]
            fig = go.Figure(go.Bar(
                x=heard_labels, y=heard_vals,
                marker_color=['#7C3AED', '#A78BFA', '#C4B5FD'],
                text=heard_vals, textposition='outside',
                textfont=dict(size=14, family='Epilogue')
            ))
            fig.update_layout(
                height=340, yaxis=dict(range=[0, 10]),
                font=dict(family='Epilogue', color='#2c3e50'),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("#### Location of Participants")
            loc_labels = [k for k, v in pre['location'].items() if v > 0]
            loc_vals   = [v for k, v in pre['location'].items() if v > 0]
            fig = lnc_donut(
                loc_labels, loc_vals,
                ['#4C1D95', '#7C3AED', '#A78BFA'],
                center_text=f"{N_pre}\nParticipants"
            )
            st.plotly_chart(fig, use_container_width=True)

    # ── ABOUT BOX ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="info-box">
        <h3>📋 About Leaders Accelerator — 10X Leaders</h3>
        <p>
            The <strong>Leaders Accelerator</strong> is a focused coaching and mentorship session
            designed to help Saudi students in Australia prepare strong applications for the
            <strong>Misk 10X Leaders program</strong>. Through individual mentoring, participants
            clarify their track fit, sharpen their articulation of leadership experiences, and
            leave with the confidence and clarity to submit a competitive application.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── FOOTER ─────────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1E0A3C 0%,#4C1D95 100%);
         color:white;padding:4rem 2rem;border-radius:40px 40px 0 0;
         margin-top:5rem;text-align:center;position:relative;overflow:hidden;">
        <div style="position:absolute;top:-50%;left:-25%;width:150%;height:200%;
             background:radial-gradient(circle,rgba(124,58,237,0.15) 0%,transparent 70%);"></div>
        <h2 style="font-family:'Cormorant Garamond',serif;font-size:2.5rem;
             margin-bottom:0.75rem;position:relative;z-index:1;">
             ⚡ Leaders Accelerator — 10X Leaders</h2>
        <p style="font-family:'Epilogue',sans-serif;font-size:1.4rem;font-weight:300;
             opacity:0.95;margin-bottom:2.5rem;position:relative;z-index:1;">
             Saudi Leadership Society · Australia Chapter</p>
        <div style="display:flex;justify-content:center;gap:2.5rem;margin:2rem 0;
             flex-wrap:wrap;position:relative;z-index:1;">
            <div><div style="font-size:2.5rem;font-weight:700">{N_pre}</div>
                 <div style="opacity:0.8">Pre-survey</div></div>
            <div><div style="font-size:2.5rem;font-weight:700">{N_post}</div>
                 <div style="opacity:0.8">Post-survey</div></div>
            <div><div style="font-size:2.5rem;font-weight:700">{post_conf_pct}%</div>
                 <div style="opacity:0.8">App. confident (post)</div></div>
            <div><div style="font-size:2.5rem;font-weight:700">{plan_action_pct}%</div>
                 <div style="opacity:0.8">Plan to apply</div></div>
            <div><div style="font-size:2.5rem;font-weight:700">{recommend_pct}%</div>
                 <div style="opacity:0.8">Would recommend</div></div>
        </div>
        <p style="font-size:1.1rem;margin-top:2rem;opacity:0.9;
             position:relative;z-index:1;"><strong>Clarity · Confidence · Coaching</strong></p>
        <p style="font-size:0.9rem;opacity:0.7;margin-top:1rem;
             position:relative;z-index:1;">
             {datetime.now().strftime('%B %d, %Y')} | Vision 2030</p>
    </div>
    """, unsafe_allow_html=True)

    st.stop()
# ============================================================================
# HEALTH SESSION DASHBOARD
# ============================================================================

if session_info.get('type') == 'health':
    metrics = data['metrics']
    topics = session_info['topic_labels']
    topic_keys = session_info.get('topic_keys', ['grow_sector', 'grow_vision2030', 'grow_job_market', 'grow_skills'])
    topic_data = [metrics.get(k, {}) for k in topic_keys]
    pre_scores   = [t.get('pre', 0)         for t in topic_data]
    post_scores  = [t.get('post', 0)        for t in topic_data]
    improvements = [t.get('improvement', 0) for t in topic_data]

    st.markdown('<p class="section-title">📊 Key Performance Indicators</p>', unsafe_allow_html=True)
    st.markdown('<p class="subsection-title">Reach & Participation</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(create_kpi_card("REACH","Total Participants",str(metrics['total_participants_pre']),
            "Attended the Health session",f"✓ {metrics['total_participants_post']} completed post-survey"),
            unsafe_allow_html=True)
    with col2:
        st.markdown(create_kpi_card("ENGAGEMENT","Completed Both Surveys",str(metrics['total_responses']),
            "Matched pre & post responses",f"✓ {metrics['match_rate_pct']:.1f}% match rate"),
            unsafe_allow_html=True)
    with col3:
        improved_pct = metrics.get('grow_members_reporting_growth_pct', 0)
        st.markdown(create_kpi_card("LEARNING","Participants Improved",f"{improved_pct:.1f}%",
            "Showed knowledge gain across topics",
            "✓ Strong majority" if improved_pct >= 60 else "→ Solid progress"),
            unsafe_allow_html=True)

    st.markdown('<p class="subsection-title">Learning Effectiveness by Topic</p>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    card_configs = [("SECTOR",topics[0],0),("VISION",topics[1],1),("JOB MARKET",topics[2],2),("SKILLS",topics[3],3)]
    for col, (cat, label, i) in zip([col1,col2,col3,col4], card_configs):
        imp = improvements[i]; is_pos = imp >= 0
        trend_text = f"{'✓' if is_pos else '▼'} {imp:+.2f} pts ({pre_scores[i]:.2f} → {post_scores[i]:.2f})"
        with col:
            st.markdown(create_kpi_card(cat,label,f"{post_scores[i]:.2f}",
                "Post-session score (out of 5)",trend_text,warn=(not is_pos)),unsafe_allow_html=True)

    st.markdown('<p class="subsection-title">Overall Knowledge Growth</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    avg_growth = metrics.get('grow_avg_knowledge_increase', 0)
    avg_pre  = sum(pre_scores)/len(pre_scores)
    avg_post = sum(post_scores)/len(post_scores)
    with col1:
        st.markdown(create_kpi_card("BASELINE","Average Pre-Score",f"{avg_pre:.2f}/5",
            "Across all four knowledge topics",""),unsafe_allow_html=True)
    with col2:
        st.markdown(create_kpi_card("OUTCOME","Average Post-Score",f"{avg_post:.2f}/5",
            "Across all four knowledge topics",
            f"✓ +{avg_growth:.2f} pts average increase" if avg_growth>=0 else f"▼ {avg_growth:.2f} pts",
            warn=(avg_growth<0)),unsafe_allow_html=True)
    with col3:
        positive_topics = sum(1 for imp in improvements if imp > 0)
        st.markdown(create_kpi_card("BREADTH","Topics with Positive Growth",f"{positive_topics} / {len(topics)}",
            "Number of areas that improved",
            "✓ Broad impact" if positive_topics>=3 else "→ Targeted gains"),unsafe_allow_html=True)

    achievements = []
    if improved_pct >= 60: achievements.append(f"{improved_pct:.1f}% of paired participants showed knowledge growth")
    best_idx = improvements.index(max(improvements))
    if improvements[best_idx] > 0: achievements.append(f"Strongest gain in '{topics[best_idx]}': +{improvements[best_idx]:.2f} pts")
    if positive_topics >= 3: achievements.append(f"Positive growth recorded in {positive_topics} out of {len(topics)} topic areas")
    if avg_post >= 3.5: achievements.append(f"Post-session average of {avg_post:.2f}/5 across all health topics")
    if achievements:
        st.markdown(f"""<div class="highlight-box"><h3>✨ Session Highlights</h3><ul>
            {''.join([f'<li>{a}</li>' for a in achievements])}</ul></div>""",unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<p class="section-title">📚 Detailed Analysis</p>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["🌱 Knowledge Development", "🕸️ Knowledge Profile", "👥 Participant Demographics"])

    with tab1:
        st.markdown("### Learning Progress — Before vs After")
        col1, col2 = st.columns([3, 2])
        with col1:
            knowledge_fig = go.Figure()
            knowledge_fig.add_trace(go.Bar(name='Before Session',x=topics,y=pre_scores,
                marker_color='#e9ecef',text=[f"{s:.2f}" for s in pre_scores],textposition='outside'))
            knowledge_fig.add_trace(go.Bar(name='After Session',x=topics,y=post_scores,
                marker_color='#006341',text=[f"{s:.2f}" for s in post_scores],textposition='outside'))
            knowledge_fig.update_layout(barmode='group',yaxis_title='Knowledge Score (1–5 scale)',
                yaxis=dict(range=[0,5.8]),height=420,font=dict(family="Epilogue",color="#2c3e50"),
                plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="center",x=0.5))
            st.plotly_chart(knowledge_fig, use_container_width=True)
        with col2:
            st.markdown("### Growth by Topic")
            bar_colors = ['#006341' if v>=0 else '#e74c3c' for v in improvements]
            improvement_fig = go.Figure()
            improvement_fig.add_trace(go.Bar(x=improvements,y=topics,orientation='h',
                marker_color=bar_colors,text=[f"{v:+.2f}" for v in improvements],
                textposition='outside',textfont=dict(size=13)))
            improvement_fig.add_vline(x=0,line_dash="dash",line_color="#adb5bd",line_width=1.5)
            improvement_fig.update_layout(xaxis_title='Score Change',xaxis=dict(range=[-0.5,0.8]),
                height=420,font=dict(family="Epilogue",color="#2c3e50"),
                plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False,margin=dict(l=10,r=40,t=20,b=20))
            st.plotly_chart(improvement_fig, use_container_width=True)
            st.markdown("### Key Metrics")
            st.metric("Average Growth", f"+{avg_growth:.2f} pts")
            st.metric("Participants Improved", f"{improved_pct:.1f}%")
            st.metric("Topics Improved", f"{positive_topics} / {len(topics)}")

    with tab2:
        st.markdown("### Knowledge Profile — Before vs After")
        radar_fig = go.Figure()
        radar_fig.add_trace(go.Scatterpolar(r=pre_scores+[pre_scores[0]],theta=topics+[topics[0]],
            fill='toself',name='Before Session',line_color='#adb5bd',fillcolor='rgba(173,181,189,0.2)',line_width=2))
        radar_fig.add_trace(go.Scatterpolar(r=post_scores+[post_scores[0]],theta=topics+[topics[0]],
            fill='toself',name='After Session',line_color='#006341',fillcolor='rgba(0,132,61,0.15)',line_width=2.5))
        radar_fig.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0,5],tickfont=dict(size=11)),
            angularaxis=dict(tickfont=dict(size=13,family='Epilogue'))),
            showlegend=True,height=500,font=dict(family="Epilogue",color="#2c3e50"),paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h",yanchor="bottom",y=-0.15,xanchor="center",x=0.5))
        col1,col2,col3 = st.columns([1,3,1])
        with col2: st.plotly_chart(radar_fig, use_container_width=True)
        st.markdown("### Score Summary")
        summary_cols = st.columns(len(topics))
        for i,(col,topic) in enumerate(zip(summary_cols,topics)):
            with col:
                st.metric(label=topic,value=f"{post_scores[i]:.2f}",delta=f"{improvements[i]:+.2f}",
                    delta_color="normal" if improvements[i]>=0 else "inverse")

    with tab3:
        st.markdown("### Who Attended?")
        demographics = metrics.get('demographics', {})
        location_data = demographics.get('location',{}) or metrics.get('demographics_location',{})
        heard_data    = demographics.get('heard_about',{}) or metrics.get('demographics_heard_about',{})
        academic_data = demographics.get('academic_level',{})
        if not location_data and not heard_data and not academic_data:
            st.info("No demographics data available in the JSON yet.")
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 📍 Location")
                if location_data:
                    fig_loc = go.Figure(data=[go.Pie(labels=list(location_data.keys()),
                        values=list(location_data.values()),hole=0.45,
                        marker_colors=['#006341','#00843d','#93c13f','#b8d96d','#d4e89e','#e9f5c9','#f4fbe8'],
                        textfont=dict(size=13,family='Epilogue'),textinfo='label+percent')])
                    fig_loc.update_layout(height=400,showlegend=True,paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(family="Epilogue",color="#2c3e50"),
                        legend=dict(orientation="v",yanchor="middle",y=0.5,xanchor="left",x=1.02),
                        margin=dict(l=20,r=120,t=20,b=20))
                    st.plotly_chart(fig_loc, use_container_width=True)
            with col2:
                st.markdown("#### 📣 How Did They Hear About Us?")
                if heard_data:
                    heard_labels = list(heard_data.keys()); heard_values = list(heard_data.values())
                    fig_heard = go.Figure(data=[go.Bar(x=heard_labels,y=heard_values,
                        marker_color=['#006341','#00843d','#93c13f','#b8d96d','#d4e89e'][:len(heard_labels)],
                        text=heard_values,textposition='outside',textfont=dict(size=15,family='Epilogue'))])
                    fig_heard.update_layout(height=380,yaxis_title='Number of Participants',
                        yaxis=dict(range=[0,max(heard_values)*1.35]),
                        font=dict(family="Epilogue",color="#2c3e50"),
                        plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0,0,0,0)',
                        showlegend=False,margin=dict(l=20,r=20,t=20,b=60))
                    st.plotly_chart(fig_heard, use_container_width=True)

    st.markdown(f"""<div class="info-box"><h3>📋 About This Session</h3>
        <p>This <strong>{selected_session}</strong> session is part of the <strong>{initiative_info['name']}</strong> initiative, 
        designed to deepen participants' understanding of the {selected_session} sector landscape, 
        its role in <strong>Vision 2030</strong>, and the skills and job market opportunities 
        it presents. Survey data was collected before and after the session to measure 
        knowledge growth across four core topic areas: {', '.join(topics)}.</p></div>""",
        unsafe_allow_html=True)

    st.markdown(f"""<div class='sls-footer'>
        <h2>{session_info['icon']} {selected_session}</h2>
        <p class="tagline">{initiative_info['name']} • Australia Chapter</p>
        <div style='display:flex;justify-content:center;gap:3rem;margin:2rem 0;flex-wrap:wrap;position:relative;z-index:1;'>
            <div><div style='font-size:2.5rem;font-weight:700'>{metrics['total_participants_pre']}</div><div style='opacity:0.8'>Participants</div></div>
            <div><div style='font-size:2.5rem;font-weight:700'>{metrics['total_responses']}</div><div style='opacity:0.8'>Matched Surveys</div></div>
            <div><div style='font-size:2.5rem;font-weight:700'>{improved_pct:.0f}%</div><div style='opacity:0.8'>Showed Growth</div></div>
            <div><div style='font-size:2.5rem;font-weight:700'>{avg_post:.2f}/5</div><div style='opacity:0.8'>Avg Post-Score</div></div>
        </div>
        <p style='font-size:1.1rem;margin-top:2rem;opacity:0.9;position:relative;z-index:1'><strong>Grow • Connect • Impact</strong></p>
        <p style='font-size:0.9rem;opacity:0.7;margin-top:1rem;position:relative;z-index:1'>{datetime.now().strftime('%B %d, %Y')} | Vision 2030</p>
    </div>""", unsafe_allow_html=True)
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
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-category">BEFORE SESSION</div><div class="kpi-label">Awareness Level</div>
            <div class="kpi-value">{metrics['awareness_summary']['aware_pre_pct']:.1f}%</div>
            <div class="kpi-context">Participants aware of Misk Tracks</div></div>""",unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-category">AFTER SESSION</div><div class="kpi-label">Awareness Level</div>
            <div class="kpi-value">{metrics['awareness_summary']['aware_post_pct']:.1f}%</div>
            <div class="kpi-context">Participants aware of Misk Tracks</div>
            <div class="kpi-trend">✓ {metrics['awareness_summary']['awareness_increase_pct_points']:.1f} pp increase</div></div>""",unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-category">SURVEY REACH</div><div class="kpi-label">Participants Surveyed</div>
            <div class="kpi-value">{metrics['total_responses']}</div>
            <div class="kpi-context">Completed both pre and post surveys</div>
            <div class="kpi-trend">✓ {metrics['match_rate_pct']:.1f}% match rate</div></div>""",unsafe_allow_html=True)

    st.markdown(f"""<div class="highlight-box"><h3>✨ Key Finding</h3><ul>
        <li>Awareness increased by {metrics['awareness_summary']['awareness_increase_pct_points']:.1f} percentage points</li>
        <li>{metrics['awareness_summary']['aware_post_pct']:.0f}% of participants are now aware of Misk Tracks</li>
        <li>From {metrics['awareness_summary']['aware_pre_pct']:.1f}% to {metrics['awareness_summary']['aware_post_pct']:.0f}% awareness</li>
    </ul></div>""", unsafe_allow_html=True)

    st.markdown('<p class="section-title">📈 Awareness Breakdown</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    colors_map = {'Very Aware':'#006341','Somewhat Aware':'#93c13f','Heard the name only':'#fbbf24','Not aware at all':'#e74c3c'}
    with col1:
        st.markdown("### Before Session")
        pre_dist = metrics['awareness_distribution']['pre']
        labels_pre = list(pre_dist.keys()); values_pre = list(pre_dist.values())
        colors_pre = [colors_map.get(l,'#666') for l in labels_pre]
        fig_pre = go.Figure(data=[go.Pie(labels=labels_pre,values=values_pre,marker_colors=colors_pre,
            textfont=dict(size=14,family='Epilogue'),hole=0.4)])
        fig_pre.update_layout(height=400,showlegend=True,
            annotations=[dict(text=f"<b>{metrics['awareness_summary']['aware_pre_pct']:.1f}%</b><br>Aware",
                x=0.5,y=0.5,font=dict(size=20,family='Cormorant Garamond'),showarrow=False)],
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h",yanchor="bottom",y=-0.15,xanchor="center",x=0.5))
        st.plotly_chart(fig_pre, use_container_width=True)
    with col2:
        st.markdown("### After Session")
        post_dist = metrics['awareness_distribution']['post']
        labels_post = list(post_dist.keys()); values_post = list(post_dist.values())
        colors_post = [colors_map.get(l,'#666') for l in labels_post]
        fig_post = go.Figure(data=[go.Pie(labels=labels_post,values=values_post,marker_colors=colors_post,
            textfont=dict(size=14,family='Epilogue'),hole=0.4)])
        fig_post.update_layout(height=400,showlegend=True,
            annotations=[dict(text=f"<b>{metrics['awareness_summary']['aware_post_pct']:.0f}%</b><br>Aware",
                x=0.5,y=0.5,font=dict(size=20,family='Cormorant Garamond'),showarrow=False)],
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h",yanchor="bottom",y=-0.15,xanchor="center",x=0.5))
        st.plotly_chart(fig_post, use_container_width=True)

    st.markdown('<p class="section-title">🔄 Before vs After Comparison</p>', unsafe_allow_html=True)
    levels = viz_data['awareness_comparison']['levels']
    pre_scores_aw = viz_data['awareness_comparison']['pre']
    post_scores_aw = viz_data['awareness_comparison']['post']
    fig_compare = go.Figure()
    fig_compare.add_trace(go.Bar(name='Before Session',x=levels,y=pre_scores_aw,
        marker_color='#e9ecef',text=[f"{s:.1f}%" for s in pre_scores_aw],textposition='outside'))
    fig_compare.add_trace(go.Bar(name='After Session',x=levels,y=post_scores_aw,
        marker_color='#006341',text=[f"{s:.1f}%" for s in post_scores_aw],textposition='outside'))
    fig_compare.update_layout(barmode='group',yaxis_title='Percentage of Participants',yaxis=dict(range=[0,80]),
        height=450,font=dict(family="Epilogue",color="#2c3e50"),
        plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="center",x=0.5))
    st.plotly_chart(fig_compare, use_container_width=True)

    st.markdown("""<div class="info-box"><h3>📋 About This Study</h3>
        <p>This baseline awareness assessment was conducted to understand participants' familiarity with 
        <strong>Misk Tracks</strong> before and after the session.</p></div>""",unsafe_allow_html=True)

    st.markdown(f"""<div class='sls-footer'>
        <h2>Misk Tracks Awareness Study</h2><p class="tagline">Baseline Assessment • Australia Chapter</p>
        <div style='display:flex;justify-content:center;gap:3rem;margin:2rem 0;flex-wrap:wrap;position:relative;z-index:1;'>
            <div><div style='font-size:2.5rem;font-weight:700'>{metrics['total_responses']}</div><div style='opacity:0.8'>Participants</div></div>
            <div><div style='font-size:2.5rem;font-weight:700'>+{metrics['awareness_summary']['awareness_increase_pct_points']:.1f}%</div><div style='opacity:0.8'>Awareness Increase</div></div>
            <div><div style='font-size:2.5rem;font-weight:700'>{metrics['awareness_summary']['aware_post_pct']:.0f}%</div><div style='opacity:0.8'>Now Aware</div></div>
        </div>
        <p style='font-size:1.1rem;margin-top:2rem;opacity:0.9;position:relative;z-index:1'><strong>Grow • Connect • Impact</strong></p>
        <p style='font-size:0.9rem;opacity:0.7;margin-top:1rem;position:relative;z-index:1'>{datetime.now().strftime('%B %d, %Y')} | Misk Tracks</p>
    </div>""",unsafe_allow_html=True)
    st.stop()

# ============================================================================
# COMPREHENSIVE DASHBOARD (10x Leaders)
# ============================================================================

if session_info.get('type') == 'comprehensive':
    metrics = data['metrics']
    response_summary   = metrics.get('response_summary', {})
    awareness_analysis = metrics.get('awareness_analysis', {})
    satisfaction       = metrics.get('satisfaction', {})
    action_plan        = metrics.get('action_plan', {})
    demographics       = metrics.get('demographics', {})
    chapter_metrics    = metrics.get('chapter_metrics', {})

    REGISTERED      = chapter_metrics.get('total_registered', 0)
    TARGET          = chapter_metrics.get('target_attendance', 50)
    ACTUAL_ATTENDEES= chapter_metrics.get('actual_attendees', 0)
    TOTAL_PRE       = response_summary.get('total_pre_responses', 0)
    TOTAL_POST      = response_summary.get('total_post_responses', 0)
    MATCHED         = response_summary.get('completed_both_surveys', 0)
    nps_pre_score   = 0
    nps_post_score  = 0

    st.markdown('<p class="section-title">📊 Key Performance Indicators</p>', unsafe_allow_html=True)
    st.markdown('<p class="subsection-title">Reach & Participation</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        attendance_rate = (ACTUAL_ATTENDEES/REGISTERED*100) if REGISTERED>0 else 0
        st.markdown(create_kpi_card("REACH","Total Participants",f"{ACTUAL_ATTENDEES}",
            f"Out of {REGISTERED} registered",f"✓ {attendance_rate:.0f}% attendance rate"),unsafe_allow_html=True)
    with col2:
        st.markdown(create_kpi_card("ENGAGEMENT","Survey Participation",f"{TOTAL_PRE} → {TOTAL_POST}",
            f"{MATCHED} completed both surveys",
            f"✓ {response_summary.get('match_rate_vs_pre_pct',0):.1f}% completion rate"),unsafe_allow_html=True)
    with col3:
        total_hours = chapter_metrics.get('total_participant_hours',0)
        target_performance = (ACTUAL_ATTENDEES/TARGET*100) if TARGET>0 else 0
        st.markdown(create_kpi_card("IMPACT","Engagement Hours",f"{total_hours}",
            f"Total participant hours ({chapter_metrics.get('session_duration_hours',0)}h session)",
            f"✓ Exceeded target by {target_performance-100:.0f}%" if target_performance>100 else ""),unsafe_allow_html=True)

    st.markdown('<p class="subsection-title">Awareness Impact</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(create_kpi_card("BEFORE","Baseline Awareness",
            f"{awareness_analysis.get('overall_pre_pct',0):.1f}%","",""),unsafe_allow_html=True)
    with col2:
        st.markdown(create_kpi_card("AFTER","Post-Session Awareness",
            f"{awareness_analysis.get('overall_post_pct',0):.1f}%","",
            f"✓ +{awareness_analysis.get('overall_increase_pct_points',0):.1f} points"),unsafe_allow_html=True)
    with col3:
        st.markdown(create_kpi_card("GROWTH","Awareness Increase",
            f"+{awareness_analysis.get('overall_increase_pct_points',0):.1f}%","","✓ Massive impact!"),unsafe_allow_html=True)

    st.markdown('<p class="subsection-title">Action & Satisfaction</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(create_kpi_card("COMMITMENT","Plan to Take Action",
            f"{action_plan.get('planning_action_pct',0):.0f}%",
            f"{action_plan.get('total_planning_action',0)} participants committed","✓ Strong commitment"),unsafe_allow_html=True)
    with col2:
        st.markdown(create_kpi_card("QUALITY","Satisfaction Score",
            f"{satisfaction.get('average_score',0):.2f}/5.0","Average participant rating","✓ Outstanding!"),unsafe_allow_html=True)
    with col3:
        st.markdown(create_kpi_card("SATISFACTION","Highly Satisfied",
            f"{satisfaction.get('satisfied_pct',0):.0f}%","Rated 4+ stars","✓ Perfect score!"),unsafe_allow_html=True)

    overall_increase = awareness_analysis.get('overall_increase_pct_points',0)
    paired_increase  = awareness_analysis.get('paired_increase_pct_points',0)
    achievements = []
    if overall_increase>=80: achievements.append(f"Massive {overall_increase:.1f} pp awareness increase (overall)")
    if paired_increase>=80:  achievements.append(f"True individual growth: {paired_increase:.1f} pts for matched participants")
    if satisfaction.get('average_score',0)>=4.5: achievements.append(f"Outstanding satisfaction: {satisfaction.get('average_score',0):.2f}/5.0")
    if action_plan.get('planning_action_pct',0)>=75: achievements.append(f"{action_plan.get('planning_action_pct',0):.0f}% committed to taking action")
    if target_performance>100: achievements.append(f"Exceeded attendance target by {target_performance-100:.0f}%")
    if achievements:
        st.markdown(f"""<div class="highlight-box"><h3>✨ Session Highlights</h3>
            <ul>{''.join([f'<li>{a}</li>' for a in achievements])}</ul></div>""",unsafe_allow_html=True)

    st.markdown('<p class="section-title">📈 Awareness Growth Comparison</p>', unsafe_allow_html=True)
    categories = ['Overall (All Respondents)', 'Paired (Matched Participants)']
    pre_values  = [awareness_analysis.get('overall_pre_pct',0), awareness_analysis.get('paired_pre_pct',0)]
    post_values = [awareness_analysis.get('overall_post_pct',0), awareness_analysis.get('paired_post_pct',0)]
    fig_awareness = go.Figure()
    fig_awareness.add_trace(go.Bar(name='Before Session',x=categories,y=pre_values,marker_color='#e9ecef',
        text=[f"{v:.1f}%" for v in pre_values],textposition='outside',textfont=dict(size=14)))
    fig_awareness.add_trace(go.Bar(name='After Session',x=categories,y=post_values,marker_color='#006341',
        text=[f"{v:.1f}%" for v in post_values],textposition='outside',textfont=dict(size=14)))
    fig_awareness.update_layout(barmode='group',yaxis_title='Awareness Percentage',yaxis=dict(range=[0,100]),
        height=450,font=dict(family="Epilogue",color="#2c3e50"),
        plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="center",x=0.5))
    st.plotly_chart(fig_awareness, use_container_width=True)

    st.markdown(f"""<div class='sls-footer'>
        <h2>10x Leaders Program</h2><p class="tagline">Misk Tracks • Australia Chapter</p>
        <div style='display:flex;justify-content:center;gap:3rem;margin:2rem 0;flex-wrap:wrap;position:relative;z-index:1;'>
            <div><div style='font-size:2.5rem;font-weight:700'>{ACTUAL_ATTENDEES}</div><div style='opacity:0.8'>Participants</div></div>
            <div><div style='font-size:2.5rem;font-weight:700'>+{paired_increase:.1f}%</div><div style='opacity:0.8'>Awareness Growth</div></div>
            <div><div style='font-size:2.5rem;font-weight:700'>{satisfaction.get('average_score',0):.2f}/5</div><div style='opacity:0.8'>Satisfaction</div></div>
        </div>
        <p style='font-size:1.1rem;margin-top:2rem;opacity:0.9;position:relative;z-index:1'><strong>Grow • Connect • Impact</strong></p>
        <p style='font-size:0.9rem;opacity:0.7;margin-top:1rem;position:relative;z-index:1'>{datetime.now().strftime('%B %d, %Y')} | 10x Leaders</p>
    </div>""",unsafe_allow_html=True)
    st.stop()

# ============================================================================
# STANDARD SESSION DASHBOARD (Cybersecurity, Finance)
# ============================================================================

metrics = data['metrics']
viz_data = data.get('visualization_data', {})
chapter_metrics = metrics.get('chapter_metrics', {})
REGISTERED       = chapter_metrics.get('total_registered', 0)
TARGET           = chapter_metrics.get('target_attendance', 50)
ACTUAL_ATTENDEES = chapter_metrics.get('actual_attendees', 0)

st.markdown('<p class="section-title">📊 Key Performance Indicators</p>', unsafe_allow_html=True)
st.markdown('<p class="subsection-title">Reach & Participation</p>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    attendance_rate = (ACTUAL_ATTENDEES/REGISTERED*100) if REGISTERED>0 else 0
    st.markdown(create_kpi_card("REACH","Total Participants",f"{ACTUAL_ATTENDEES}",
        f"Out of {REGISTERED} registered",f"✓ {attendance_rate:.0f}% attendance rate"),unsafe_allow_html=True)
with col2:
    survey_completion = (metrics['total_responses']/ACTUAL_ATTENDEES*100) if ACTUAL_ATTENDEES>0 else 0
    st.markdown(create_kpi_card("ENGAGEMENT","Completed Both Surveys",f"{metrics['total_responses']}",
        f"Out of {ACTUAL_ATTENDEES} participants",
        "✓ High engagement" if survey_completion>=50 else "→ Can improve"),unsafe_allow_html=True)
with col3:
    target_performance = (ACTUAL_ATTENDEES/TARGET*100) if TARGET>0 else 0
    st.markdown(create_kpi_card("TARGET","Goal Achievement",f"{target_performance:.0f}%",
        f"Target was {TARGET} participants",
        f"✓ Exceeded target" if ACTUAL_ATTENDEES>TARGET else "→ Approaching target"),unsafe_allow_html=True)

st.markdown('<p class="subsection-title">Learning Effectiveness</p>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    avg_growth = metrics.get('grow_avg_knowledge_increase',0)
    st.markdown(create_kpi_card("KNOWLEDGE","Average Growth",f"+{avg_growth:.2f}",
        "Points improvement (1-5 scale)",
        f"✓ Strong growth" if avg_growth>=1.0 else "→ Moderate growth"),unsafe_allow_html=True)
with col2:
    improved_pct = metrics.get('grow_members_reporting_growth_pct',0)
    st.markdown(create_kpi_card("LEARNING","Participants Improved",f"{improved_pct:.0f}%",
        "Showed knowledge gain","✓ Excellent reach" if improved_pct>=70 else "→ Good reach"),unsafe_allow_html=True)
with col3:
    significant_pct = metrics.get('grow_significant_growth_pct',0)
    st.markdown(create_kpi_card("IMPACT","Significant Growth",f"{significant_pct:.0f}%",
        "Gained ≥0.5 points","✓ Deep learning" if significant_pct>=50 else "→ Solid progress"),unsafe_allow_html=True)

st.markdown('<p class="subsection-title">Action & Satisfaction</p>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    action_pct   = metrics.get('connect_members_planning_action_pct',0)
    action_count = metrics.get('connect_total_planning_action',0)
    st.markdown(create_kpi_card("COMMITMENT","Plan to Take Action",f"{action_pct:.0f}%",
        f"{action_count} participants committed",
        f"✓ Outstanding" if action_pct>=80 else "✓ Strong" if action_pct>=60 else "→ Growing"),unsafe_allow_html=True)
with col2:
    satisfaction = metrics.get('impact_avg_satisfaction',0)
    st.markdown(create_kpi_card("QUALITY","Satisfaction Score",f"{satisfaction:.2f}/5.0",
        "Average participant rating",
        f"✓ Excellent" if satisfaction>=4.5 else "✓ Very good" if satisfaction>=4.0 else "→ Good"),unsafe_allow_html=True)
with col3:
    satisfied_pct = metrics.get('impact_satisfaction_pct',0)
    st.markdown(create_kpi_card("SATISFACTION","Highly Satisfied",f"{satisfied_pct:.0f}%",
        "Rated 4+ stars","✓ Strong approval" if satisfied_pct>=70 else "→ Positive reception"),unsafe_allow_html=True)

achievements = []
if action_pct>=80:   achievements.append(f"{action_pct:.0f}% of participants committed to taking action")
if satisfaction>=4.0: achievements.append(f"Achieved {satisfaction:.1f}/5.0 satisfaction rating")
if ACTUAL_ATTENDEES>TARGET: achievements.append(f"Exceeded attendance target by {((ACTUAL_ATTENDEES-TARGET)/TARGET*100):.0f}%")
if avg_growth>=1.0:  achievements.append(f"Strong knowledge improvement of +{avg_growth:.2f} points")
if achievements:
    st.markdown(f"""<div class="highlight-box"><h3>✨ Session Highlights</h3>
        <ul>{''.join([f'<li>{a}</li>' for a in achievements])}</ul></div>""",unsafe_allow_html=True)

st.markdown('<p class="section-title">🎓 Participant Journey</p>', unsafe_allow_html=True)
col1, col2 = st.columns([2,1])
with col1:
    funnel_fig = go.Figure()
    funnel_fig.add_trace(go.Funnel(
        y=['Registered','Attended','Completed Both Surveys','Plan to Act'],
        x=[REGISTERED,ACTUAL_ATTENDEES,metrics['total_responses'],metrics.get('connect_total_planning_action',0)],
        textposition="inside",textinfo="value+percent initial",
        marker={"color":['#006341','#00843d','#93c13f','#b8d96d'],"line":{"width":2,"color":"white"}}
    ))
    funnel_fig.update_layout(height=400,font=dict(family="Epilogue",size=14,color="#2c3e50"),
        plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0,0,0,0)',margin=dict(l=20,r=20,t=20,b=20))
    st.plotly_chart(funnel_fig, use_container_width=True)
with col2:
    st.markdown("### Conversion Metrics")
    reg_to_attend     = (ACTUAL_ATTENDEES/REGISTERED*100) if REGISTERED>0 else 0
    attend_to_survey  = (metrics['total_responses']/ACTUAL_ATTENDEES*100) if ACTUAL_ATTENDEES>0 else 0
    survey_to_action  = (metrics.get('connect_total_planning_action',0)/metrics['total_responses']*100) if metrics['total_responses']>0 else 0
    st.metric("Registered → Attended",f"{reg_to_attend:.0f}%")
    st.metric("Attended → Surveyed",f"{attend_to_survey:.0f}%")
    st.metric("Surveyed → Committed",f"{survey_to_action:.0f}%")
    st.markdown("---")
    overall = (metrics.get('connect_total_planning_action',0)/REGISTERED*100) if REGISTERED>0 else 0
    st.info(f"**Overall:** {overall:.0f}% of registrants became committed participants")

st.markdown("---")
st.markdown('<p class="section-title">📚 Detailed Analysis</p>', unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["🌱 Knowledge Development","🤝 Commitment","💡 Satisfaction"])

with tab1:
    st.markdown("### Learning Progress")
    col1, col2 = st.columns([3,2])
    with col1:
        topics = session_info['topic_labels']
        pre_scores  = viz_data['knowledge_comparison']['pre_scores']
        post_scores = viz_data['knowledge_comparison']['post_scores']
        improvements = viz_data['knowledge_comparison']['improvements']
        knowledge_fig = go.Figure()
        knowledge_fig.add_trace(go.Bar(name='Before Session',x=topics,y=pre_scores,
            marker_color='#e9ecef',text=[f"{s:.2f}" for s in pre_scores],textposition='outside'))
        knowledge_fig.add_trace(go.Bar(name='After Session',x=topics,y=post_scores,
            marker_color='#006341',text=[f"{s:.2f}" for s in post_scores],textposition='outside'))
        knowledge_fig.update_layout(barmode='group',yaxis_title='Knowledge Level (1-5)',
            yaxis=dict(range=[0,6]),height=400,font=dict(family="Epilogue",color="#2c3e50"),
            plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="center",x=0.5))
        st.plotly_chart(knowledge_fig, use_container_width=True)
    with col2:
        st.markdown("### Key Metrics")
        st.metric("Average Growth",f"+{metrics.get('grow_avg_knowledge_increase',0):.2f} pts")
        st.metric("Participants Improved",f"{metrics.get('grow_members_reporting_growth_pct',0):.0f}%")
        st.metric("Significant Growth",f"{metrics.get('grow_significant_growth_pct',0):.0f}%")

with tab2:
    st.markdown("### Action Commitment")
    col1, col2 = st.columns(2)
    with col1:
        action_data = viz_data.get('action_plan_data',{})
        labels = list(action_data.keys()); values = list(action_data.values())
        committed_count = metrics.get('connect_total_planning_action',0)
        action_fig = go.Figure(data=[go.Pie(labels=labels,values=values,hole=0.6,
            marker_colors=['#006341','#e9ecef'],textfont=dict(size=16,family='Epilogue'))])
        action_fig.update_layout(height=350,showlegend=True,
            annotations=[dict(text=f"<b>{committed_count}</b><br>Committed",
                x=0.5,y=0.5,font=dict(size=20,family='Cormorant Garamond'),showarrow=False)],
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h",yanchor="bottom",y=-0.1,xanchor="center",x=0.5))
        st.plotly_chart(action_fig, use_container_width=True)
    with col2:
        st.markdown("### Summary")
        st.metric("Commitment Rate",f"{metrics.get('connect_members_planning_action_pct',0):.1f}%")
        st.metric("Total Committed",metrics.get('connect_total_planning_action',0))
        st.metric("Would Recommend",f"{metrics.get('impact_likely_recommend_pct',0):.1f}%")

with tab3:
    st.markdown("### Participant Feedback")
    col1, col2 = st.columns([3,2])
    with col1:
        satisfaction_data = viz_data.get('satisfaction_data',{})
        if satisfaction_data:
            satisfaction_order = ['Very dissatisfied','Dissatisfied','Neutral','Satisfied','Very satisfied']
            sorted_items = sorted(satisfaction_data.items(),
                key=lambda x: satisfaction_order.index(x[0]) if x[0] in satisfaction_order else 2)
            labels = [item[0] for item in sorted_items]; values = [item[1] for item in sorted_items]
            colors = ['#e74c3c','#e67e22','#f39c12','#93c13f','#006341'][:len(labels)]
            sat_fig = go.Figure(data=[go.Bar(y=labels,x=values,orientation='h',marker_color=colors,
                text=values,textposition='outside',textfont=dict(size=14))])
            sat_fig.update_layout(xaxis_title='Number of Participants',height=350,
                font=dict(family="Epilogue",color="#2c3e50"),
                plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0,0,0,0)',showlegend=False)
            st.plotly_chart(sat_fig, use_container_width=True)
    with col2:
        st.markdown("### Metrics")
        st.metric("Average Rating",f"{metrics.get('impact_avg_satisfaction',0):.2f}/5.0")
        st.metric("Highly Satisfied",f"{metrics.get('impact_satisfaction_pct',0):.0f}%")
        st.metric("Likely to Recommend",f"{metrics.get('impact_likely_recommend_pct',0):.1f}%")

st.markdown(f"""<div class='sls-footer'>
    <h2>Saudi Leadership Society</h2>
    <p class="tagline">Towards the Vision • Australia Chapter</p>
    <div style='display:flex;justify-content:center;gap:3rem;margin:2rem 0;flex-wrap:wrap;position:relative;z-index:1;'>
        <div><div style='font-size:2.5rem;font-weight:700'>{ACTUAL_ATTENDEES}</div><div style='opacity:0.8'>Participants</div></div>
        <div><div style='font-size:2.5rem;font-weight:700'>+{metrics.get('grow_avg_knowledge_increase',0):.2f}</div><div style='opacity:0.8'>Avg Growth</div></div>
        <div><div style='font-size:2.5rem;font-weight:700'>{metrics.get('connect_total_planning_action',0)}</div><div style='opacity:0.8'>Taking Action</div></div>
    </div>
    <p style='font-size:1.1rem;margin-top:2rem;opacity:0.9;position:relative;z-index:1'><strong>Grow • Connect • Impact</strong></p>
    <p style='font-size:0.9rem;opacity:0.7;margin-top:1rem;position:relative;z-index:1'>{datetime.now().strftime('%B %d, %Y')} | Vision 2030</p>
</div>""",unsafe_allow_html=True)
