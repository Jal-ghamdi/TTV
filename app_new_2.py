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
# SESSION CONFIGURATION
# ============================================================================

SESSIONS = {
    "Cybersecurity": {
        "name": "🔐 Cybersecurity Session",
        "data_file": "sls_kpi_data_cybersecurity_updated1.json",
        "icon": "🔐",
        "vision_theme": "Digital Transformation & Innovation",
        "pillar": "Grow"
    },
    "Finance": {
        "name": "💰 Finance Session",
        "data_file": "sls_kpi_finance_session2_ttv_data_updated1.json",
        "icon": "💰",
        "vision_theme": "The Financial sector and financial institutions",
        "pillar": "Grow"
    }
}

# ============================================================================
# SLS BRAND CSS - INSPIRED BY OFFICIAL MATERIALS
# ============================================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Playfair+Display:wght@400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Saudi-inspired gradient background */
    .main {
        background: linear-gradient(135deg, #fafafa 0%, #ffffff 50%, #f5f8f5 100%);
    }
    
    /* SLS Brand Header */
    .sls-header {
        background: linear-gradient(135deg, #006341 0%, #00843d 50%, #93c13f 100%);
        padding: 3rem 2rem;
        border-radius: 0 0 30px 30px;
        box-shadow: 0 10px 40px rgba(0, 100, 65, 0.15);
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
    }
    
    .sls-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 500px;
        height: 500px;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        border-radius: 50%;
    }
    
    .sls-header::after {
        content: '';
        position: absolute;
        bottom: -30%;
        left: -5%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(147,193,63,0.2) 0%, transparent 70%);
        border-radius: 50%;
    }
    
    .initiative-title {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 900;
        color: white;
        text-align: center;
        margin: 0;
        letter-spacing: -0.03em;
        position: relative;
        z-index: 1;
        text-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .initiative-subtitle {
        font-family: 'Outfit', sans-serif;
        font-size: 1.3rem;
        font-weight: 300;
        color: rgba(255,255,255,0.95);
        text-align: center;
        margin-top: 0.5rem;
        position: relative;
        z-index: 1;
        letter-spacing: 0.05em;
    }
    
    .mission-tagline {
        font-family: 'Outfit', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: rgba(255,255,255,0.9);
        text-align: center;
        margin-top: 1.5rem;
        padding: 1rem 2rem;
        background: rgba(255,255,255,0.15);
        border-radius: 50px;
        backdrop-filter: blur(10px);
        display: inline-block;
        position: relative;
        z-index: 1;
    }
    
    /* Pillar Badges */
    .pillar-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.6rem 1.5rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.95rem;
        margin: 0.3rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .pillar-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    .pillar-grow {
        background: linear-gradient(135deg, #006341 0%, #00843d 100%);
        color: white;
    }
    
    .pillar-connect {
        background: linear-gradient(135deg, #1a5490 0%, #2d7ab5 100%);
        color: white;
    }
    
    .pillar-impact {
        background: linear-gradient(135deg, #93c13f 0%, #b8d96d 100%);
        color: #1a1a1a;
    }
    
    /* Section Headers */
    .section-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a1a1a;
        margin: 3rem 0 1.5rem 0;
        padding-bottom: 1rem;
        border-bottom: 3px solid;
        border-image: linear-gradient(90deg, #006341, #93c13f) 1;
    }
    
    /* KPI Cards - SLS Style */
    .metric-card {
        background: white;
        padding: 2.5rem 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0, 100, 65, 0.08);
        border: 1px solid rgba(0, 132, 61, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #006341 0%, #93c13f 100%);
    }
    
    .metric-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 40px rgba(0, 132, 61, 0.15);
    }
    
    .metric-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .metric-label {
        font-family: 'Outfit', sans-serif;
        font-size: 0.85rem;
        font-weight: 700;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin-bottom: 0.75rem;
    }
    
    .metric-value {
        font-family: 'Playfair Display', serif;
        font-size: 3.2rem;
        font-weight: 900;
        color: #006341;
        line-height: 1;
        margin: 1rem 0;
    }
    
    .metric-context {
        font-family: 'Outfit', sans-serif;
        font-size: 1rem;
        color: #00843d;
        font-weight: 500;
        margin-top: 1rem;
    }
    
    /* Impact Highlight Box */
    .impact-box {
        background: linear-gradient(135deg, #006341 0%, #00843d 100%);
        padding: 2.5rem;
        border-radius: 24px;
        margin: 2rem 0;
        box-shadow: 0 12px 40px rgba(0, 100, 65, 0.25);
        position: relative;
        overflow: hidden;
    }
    
    .impact-box::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(147,193,63,0.2) 0%, transparent 70%);
        border-radius: 50%;
    }
    
    .impact-box h3 {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: white;
        margin-bottom: 1.5rem;
        position: relative;
        z-index: 1;
    }
    
    .impact-box ul {
        list-style: none;
        padding: 0;
        margin: 0;
        position: relative;
        z-index: 1;
    }
    
    .impact-box li {
        font-family: 'Outfit', sans-serif;
        font-size: 1.1rem;
        color: rgba(255,255,255,0.95);
        line-height: 1.8;
        padding: 0.75rem 0;
        padding-left: 2rem;
        position: relative;
        font-weight: 400;
    }
    
    .impact-box li:before {
        content: "✓";
        position: absolute;
        left: 0;
        color: #93c13f;
        font-weight: 900;
        font-size: 1.4rem;
    }
    
    /* Pillar Breakdown Cards */
    .pillar-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin: 1rem 0;
        border-top: 5px solid;
        transition: all 0.3s ease;
    }
    
    .pillar-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    .pillar-card.grow { border-top-color: #006341; }
    .pillar-card.connect { border-top-color: #1a5490; }
    .pillar-card.impact { border-top-color: #93c13f; }
    
    .pillar-name {
        font-family: 'Outfit', sans-serif;
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin-bottom: 0.75rem;
    }
    
    .pillar-card.grow .pillar-name { color: #006341; }
    .pillar-card.connect .pillar-name { color: #1a5490; }
    .pillar-card.impact .pillar-name { color: #93c13f; }
    
    .pillar-score {
        font-family: 'Playfair Display', serif;
        font-size: 2.5rem;
        font-weight: 900;
        color: #1a1a1a;
    }
    
    .pillar-detail {
        font-family: 'Outfit', sans-serif;
        font-size: 0.95rem;
        color: #666;
        margin-top: 0.5rem;
    }
    
    .pillar-contribution {
        font-family: 'Outfit', sans-serif;
        font-size: 0.9rem;
        font-weight: 600;
        margin-top: 0.75rem;
    }
    
    .pillar-card.grow .pillar-contribution { color: #00843d; }
    .pillar-card.connect .pillar-contribution { color: #2d7ab5; }
    .pillar-card.impact .pillar-contribution { color: #93c13f; }
    
    /* Info Box */
    .info-box {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        padding: 2.5rem;
        border-radius: 20px;
        border: 2px solid rgba(0, 100, 65, 0.1);
        margin: 2rem 0;
    }
    
    .info-box h3 {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        color: #1a1a1a;
        margin-bottom: 1rem;
    }
    
    .info-box p {
        font-family: 'Outfit', sans-serif;
        font-size: 1.05rem;
        line-height: 1.8;
        color: #495057;
        font-weight: 400;
    }
    
    /* Session Cards */
    .session-card {
        background: white;
        padding: 3rem 2rem;
        border-radius: 24px;
        text-align: center;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border: 2px solid transparent;
        cursor: pointer;
    }
    
    .session-card:hover {
        transform: translateY(-12px);
        box-shadow: 0 16px 50px rgba(0, 100, 65, 0.2);
        border-color: #00843d;
    }
    
    .session-icon {
        font-size: 4.5rem;
        margin-bottom: 1.5rem;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
    }
    
    .session-name {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 0.75rem;
    }
    
    .session-theme {
        font-family: 'Outfit', sans-serif;
        font-size: 1rem;
        color: #666;
        font-weight: 500;
    }
    
    /* Tabs - SLS Style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: white;
        padding: 1rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(0, 100, 65, 0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Outfit', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background: linear-gradient(135deg, #006341 0%, #00843d 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(0, 100, 65, 0.3);
    }
    
    /* Footer - SLS Brand */
    .sls-footer {
        background: linear-gradient(135deg, #1a1a1a 0%, #2c3e50 100%);
        color: white;
        padding: 3.5rem 2rem;
        border-radius: 30px 30px 0 0;
        margin-top: 4rem;
        text-align: center;
    }
    
    .sls-footer h2 {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        margin-bottom: 0.5rem;
    }
    
    .sls-footer .tagline {
        font-family: 'Outfit', sans-serif;
        font-size: 1.3rem;
        font-weight: 300;
        opacity: 0.9;
        margin-bottom: 2rem;
        letter-spacing: 0.05em;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_engagement_score(metrics):
    """Calculate engagement score: Knowledge (35%) + Action (30%) + Satisfaction (25%) + Attendance (10%)"""
    try:
        attendance_rate = (metrics.get('chapter_metrics', {}).get('actual_attendees', 0) / 
                          metrics.get('chapter_metrics', {}).get('total_registered', 1)) * 100
        knowledge_score = max(0, metrics.get('grow_avg_knowledge_increase', 0) * 20)
        action_rate = metrics.get('connect_members_planning_action_pct', 0)
        satisfaction_score = (metrics.get('impact_avg_satisfaction', 0) / 5) * 100
        
        engagement = (
            knowledge_score * 0.35 +
            action_rate * 0.30 +
            satisfaction_score * 0.25 +
            attendance_rate * 0.10
        )
        
        return round(max(0, min(100, engagement)), 1)
    except:
        return 0

def generate_insights(metrics, chapter_metrics):
    """Generate key insights"""
    insights = []
    
    if metrics.get('connect_members_planning_action_pct', 0) >= 80:
        insights.append(f"{metrics.get('connect_members_planning_action_pct', 0):.0f}% of participants committed to taking action")
    
    if metrics.get('impact_avg_satisfaction', 0) >= 4.0:
        insights.append(f"Exceptional satisfaction with {metrics.get('impact_avg_satisfaction', 0):.1f}/5.0 rating")
    
    if chapter_metrics.get('actual_attendees', 0) > chapter_metrics.get('target_attendance', 0):
        insights.append(f"Exceeded target with {chapter_metrics.get('actual_attendees', 0)} participants")
    
    return insights

def create_metric_card(icon, label, value, context):
    """Create SLS-styled metric card"""
    return f"""
    <div class="metric-card">
        <span class="metric-icon">{icon}</span>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-context">{context}</div>
    </div>
    """

# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_data
def load_data(data_file):
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
        return data
    except:
        st.error(f"⚠️ Data file '{data_file}' not found!")
        return None

# ============================================================================
# SESSION MANAGEMENT
# ============================================================================

if 'selected_session' not in st.session_state:
    st.session_state.selected_session = None

# ============================================================================
# SESSION SELECTION SCREEN
# ============================================================================

if st.session_state.selected_session is None:
    try:
        st.image("sls_image.jpg", use_column_width=True)
    except:
        pass
    
    # SLS Header
    st.markdown("""
    <div class="sls-header">
        <h1 class="initiative-title">Towards the Vision</h1>
        <p class="initiative-subtitle">Saudi Leadership Society • Australia Chapter</p>
        <div style="text-align: center; margin-top: 1.5rem;">
            <span class="mission-tagline">Grow • Connect • Impact</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h3>About Towards the Vision</h3>
        <p>
            An initiative by the <strong>Saudi Leadership Society Australia Chapter</strong>, designed to advance Vision 2030 
            through educational programs that empower participants with knowledge, skills, and connections. 
            This dashboard measures program impact across our three core pillars: <strong>Grow, Connect, and Impact</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="section-title">📚 Select a Session</p>', unsafe_allow_html=True)
    
    cols = st.columns(len(SESSIONS))
    
    for idx, (session_key, session_info) in enumerate(SESSIONS.items()):
        with cols[idx]:
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
                <div style="margin-top: 1rem;">
                    <span class="pillar-badge pillar-{session_info['pillar'].lower()}">{session_info['pillar']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.stop()

# ============================================================================
# LOAD SELECTED SESSION
# ============================================================================

selected_session = st.session_state.selected_session
session_info = SESSIONS[selected_session]

try:
    st.image("sls_image.jpg", use_column_width=True)
except:
    pass

# Header
st.markdown(f"""
<div class="sls-header">
    <h1 class="initiative-title">{session_info["icon"]} {selected_session} Session</h1>
    <p class="initiative-subtitle">Towards the Vision • {session_info['vision_theme']}</p>
    <div style="text-align: center; margin-top: 1.5rem;">
        <span class="pillar-badge pillar-grow">🌱 Grow</span>
        <span class="pillar-badge pillar-connect">🤝 Connect</span>
        <span class="pillar-badge pillar-impact">💡 Impact</span>
    </div>
</div>
""", unsafe_allow_html=True)

if st.button("← Back to Sessions", type="secondary"):
    st.session_state.selected_session = None
    st.rerun()

data = load_data(session_info['data_file'])

if data is None:
    st.error(f"Could not load data for {selected_session} session.")
    st.stop()

metrics = data['metrics']
viz_data = data['visualization_data']
chapter_metrics = metrics.get('chapter_metrics', {})

REGISTERED = chapter_metrics.get('total_registered', 119)
TARGET = chapter_metrics.get('target_attendance', 50)
ACTUAL_ATTENDEES = chapter_metrics.get('actual_attendees', 54)

engagement_score = calculate_engagement_score(metrics)
insights = generate_insights(metrics, chapter_metrics)

# ============================================================================
# KEY METRICS
# ============================================================================

st.markdown('<p class="section-title">📊 Program Performance</p>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        create_metric_card(
            "🎯",
            "Engagement Score",
            f"{engagement_score}/100",
            "Overall quality"
        ),
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        create_metric_card(
            "👥",
            "Participants",
            f"{ACTUAL_ATTENDEES}",
            f"{(ACTUAL_ATTENDEES/TARGET*100):.0f}% of target"
        ),
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        create_metric_card(
            "⚡",
            "Taking Action",
            f"{metrics.get('connect_total_planning_action', 0)}",
            f"{metrics.get('connect_members_planning_action_pct', 0):.0f}% committed"
        ),
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        create_metric_card(
            "⭐",
            "Satisfaction",
            f"{metrics.get('impact_avg_satisfaction', 0):.1f}/5.0",
            f"{metrics.get('impact_satisfaction_pct', 0):.0f}% satisfied"
        ),
        unsafe_allow_html=True
    )

if insights:
    st.markdown(f"""
    <div class="impact-box">
        <h3>✨ Key Achievements</h3>
        <ul>
            {''.join([f'<li>{insight}</li>' for insight in insights])}
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# PILLAR BREAKDOWN
# ============================================================================

st.markdown('<p class="section-title">🎯 Grow • Connect • Impact Breakdown</p>', unsafe_allow_html=True)

attendance_rate = (ACTUAL_ATTENDEES / REGISTERED) * 100 if REGISTERED > 0 else 0
knowledge_score = metrics.get('grow_avg_knowledge_increase', 0) * 20
action_rate = metrics.get('connect_members_planning_action_pct', 0)
satisfaction_score = (metrics.get('impact_avg_satisfaction', 0) / 5) * 100

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="pillar-card grow">
        <div class="pillar-name">🌱 GROW (35%)</div>
        <div class="pillar-score">{knowledge_score:.1f}</div>
        <div class="pillar-detail">Knowledge development</div>
        <div class="pillar-contribution">Contributes +{knowledge_score * 0.35:.1f} points</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="pillar-card connect">
        <div class="pillar-name">🤝 CONNECT (30%)</div>
        <div class="pillar-score">{action_rate:.1f}</div>
        <div class="pillar-detail">Action commitment</div>
        <div class="pillar-contribution">Contributes +{action_rate * 0.30:.1f} points</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="pillar-card impact">
        <div class="pillar-name">💡 IMPACT (25%)</div>
        <div class="pillar-score">{satisfaction_score:.1f}</div>
        <div class="pillar-detail">Member satisfaction</div>
        <div class="pillar-contribution">Contributes +{satisfaction_score * 0.25:.1f} points</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="pillar-card grow">
        <div class="pillar-name">👥 ATTENDANCE (10%)</div>
        <div class="pillar-score">{attendance_rate:.1f}</div>
        <div class="pillar-detail">Show-up rate</div>
        <div class="pillar-contribution">Contributes +{attendance_rate * 0.10:.1f} points</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# PARTICIPANT JOURNEY
# ============================================================================

st.markdown('<p class="section-title">🎓 Participant Journey</p>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    funnel_data = {
        'stages': ['Registered', 'Attended', 'Completed Survey', 'Taking Action'],
        'values': [REGISTERED, ACTUAL_ATTENDEES, metrics['total_responses'], metrics.get('connect_total_planning_action', 0)]
    }
    
    fig = go.Figure()
    
    fig.add_trace(go.Funnel(
        y=funnel_data['stages'],
        x=funnel_data['values'],
        textposition="inside",
        textinfo="value+percent initial",
        marker={
            "color": ['#006341', '#00843d', '#93c13f', '#b8d96d'],
            "line": {"width": 2, "color": "white"}
        }
    ))
    
    fig.update_layout(
        height=450,
        font=dict(family="Outfit", size=14),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 📊 Conversion")
    
    conv1 = (ACTUAL_ATTENDEES / REGISTERED * 100) if REGISTERED > 0 else 0
    conv2 = (metrics['total_responses'] / ACTUAL_ATTENDEES * 100) if ACTUAL_ATTENDEES > 0 else 0
    conv3 = (metrics.get('connect_total_planning_action', 0) / metrics['total_responses'] * 100) if metrics['total_responses'] > 0 else 0
    
    st.metric("Registration → Attendance", f"{conv1:.1f}%")
    st.metric("Attendance → Survey", f"{conv2:.1f}%")
    st.metric("Survey → Action", f"{conv3:.1f}%")

# ============================================================================
# DETAILED TABS
# ============================================================================

st.markdown("---")
st.markdown('<p class="section-title">📚 Detailed Analysis</p>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🌱 Grow", "🤝 Connect", "💡 Impact"])

with tab1:
    st.markdown("### Learning Outcomes")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        topics = viz_data['knowledge_comparison']['topics']
        pre_scores = viz_data['knowledge_comparison']['pre_scores']
        post_scores = viz_data['knowledge_comparison']['post_scores']
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Before',
            x=topics,
            y=pre_scores,
            marker_color='#e9ecef',
            text=[f"{s:.2f}" for s in pre_scores],
            textposition='outside'
        ))
        
        fig.add_trace(go.Bar(
            name='After',
            x=topics,
            y=post_scores,
            marker_color='#006341',
            text=[f"{s:.2f}" for s in post_scores],
            textposition='outside'
        ))
        
        fig.update_layout(
            barmode='group',
            yaxis=dict(range=[0, 6]),
            height=400,
            font=dict(family="Outfit"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.metric("Avg Growth", f"+{metrics.get('grow_avg_knowledge_increase', 0):.2f}")
        st.metric("Improved", f"{metrics.get('grow_members_reporting_growth_pct', 0):.0f}%")

with tab2:
    st.markdown("### Engagement")
    
    col1, col2 = st.columns(2)
    
    with col1:
        action_data = viz_data.get('action_plan_data', {})
        labels = list(action_data.keys())
        values = list(action_data.values())
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.6,
            marker_colors=['#006341', '#e9ecef']
        )])
        
        fig.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.metric("Commitment", f"{metrics.get('connect_members_planning_action_pct', 0):.1f}%")
        st.metric("Committed", metrics.get('connect_total_planning_action', 0))

with tab3:
    st.markdown("### Satisfaction")
    
    satisfaction_data = viz_data.get('satisfaction_data', {})
    
    if satisfaction_data:
        st.metric("Average", f"{metrics.get('impact_avg_satisfaction', 0):.2f}/5.0")
        st.metric("Satisfied", f"{metrics.get('impact_satisfaction_pct', 0):.0f}%")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown(f"""
<div class='sls-footer'>
    <h2>Saudi Leadership Society</h2>
    <p class="tagline">Towards the Vision • Australia Chapter</p>
    <div style='display: flex; justify-content: center; gap: 3rem; margin: 2rem 0; flex-wrap: wrap;'>
        <div>
            <div style='font-size: 2.5rem; font-weight: 700;'>{ACTUAL_ATTENDEES}</div>
            <div style='opacity: 0.8;'>Participants</div>
        </div>
        <div>
            <div style='font-size: 2.5rem; font-weight: 700;'>{engagement_score}/100</div>
            <div style='opacity: 0.8;'>Quality</div>
        </div>
        <div>
            <div style='font-size: 2.5rem; font-weight: 700;'>{metrics.get('connect_total_planning_action', 0)}</div>
            <div style='opacity: 0.8;'>Taking Action</div>
        </div>
    </div>
    <p style='font-size: 1.1rem; margin-top: 2rem; opacity: 0.9;'>
        <strong>Grow • Connect • Impact</strong>
    </p>
    <p style='font-size: 0.9rem; opacity: 0.7; margin-top: 1rem;'>
        {datetime.now().strftime('%B %d, %Y')} | Vision 2030
    </p>
</div>
""", unsafe_allow_html=True)
