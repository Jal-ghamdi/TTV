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
if session_info.get('type') != 'lnc':
    data = load_data(session_info['data_file'])
    if data is None:
        st.error("Could not load data.")
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
            f"{pre['atmosphere']['Comfortable & friendly'.replace(chr(10),' ')]} people felt comfortable",
            f"{post['atmosphere']['Comfortable\n& friendly']} people felt comfortable",
            "#6b7280", "#0d3b6e", "%",
            "Comfortable\n& friendl"
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
