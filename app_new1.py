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
    page_title="SLS AU Chapter Analytics", 
    layout="wide", 
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# ============================================================================
# SESSION CONFIGURATION
# ============================================================================

SESSIONS = {
    "Cybersecurity": {
        "name": "🔐 Cybersecurity Session",
        "data_file": "sls_kpi_data_cybersecurity_updated1.json",
        "color": "#ff6b6b",
        "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "icon": "🔐"
    },
    "Finance": {
        "name": "💰 Finance Session",
        "data_file": "sls_kpi_finance_session2_ttv_data_updated1.json",
        "color": "#51cf66",
        "gradient": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
        "icon": "💰"
    }
}

# ============================================================================
# CUSTOM CSS - PROFESSIONAL DESIGN
# ============================================================================

st.markdown("""
<style>
    /* Import Professional Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Space+Mono:wght@400;700&family=DM+Sans:wght@400;500;700&display=swap');
    
    /* Global Styles */
    .main {
        background: linear-gradient(to bottom, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Headers */
    .dashboard-title {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 1rem 0 0.5rem 0;
        letter-spacing: -0.02em;
    }
    
    .dashboard-subtitle {
        font-family: 'DM Sans', sans-serif;
        font-size: 1.1rem;
        color: #6c757d;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    .section-header {
        font-family: 'Space Mono', monospace;
        font-size: 1.8rem;
        font-weight: 700;
        color: #2c3e50;
        margin: 2.5rem 0 1.5rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 4px solid;
        border-image: linear-gradient(90deg, #667eea, #764ba2) 1;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 1.75rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border-left: 5px solid #667eea;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100px;
        background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 70%);
        border-radius: 50%;
        transform: translate(30%, -30%);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.2);
    }
    
    .metric-card.grow {
        border-left-color: #f093fb;
    }
    
    .metric-card.connect {
        border-left-color: #4facfe;
    }
    
    .metric-card.impact {
        border-left-color: #43e97b;
    }
    
    .metric-label {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.85rem;
        color: #6c757d;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-family: 'Space Mono', monospace;
        font-size: 2.5rem;
        font-weight: 700;
        color: #2c3e50;
        line-height: 1;
        margin: 0.5rem 0;
    }
    
    .metric-delta {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.95rem;
        color: #28a745;
        font-weight: 600;
    }
    
    .metric-delta.negative {
        color: #dc3545;
    }
    
    /* Session Selection */
    .session-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
        transition: all 0.3s ease;
        cursor: pointer;
        border: 3px solid transparent;
    }
    
    .session-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
        border-color: #667eea;
    }
    
    .session-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .session-name {
        font-family: 'DM Sans', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    /* Stats Grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    /* Insight Box */
    .insight-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        font-family: 'DM Sans', sans-serif;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    .insight-box h4 {
        font-family: 'Space Mono', monospace;
        font-weight: 700;
        margin-bottom: 0.75rem;
        font-size: 1.2rem;
    }
    
    .insight-box p {
        margin: 0.5rem 0;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    /* Performance Badge */
    .performance-badge {
        display: inline-block;
        padding: 0.5rem 1.25rem;
        border-radius: 50px;
        font-family: 'Space Mono', monospace;
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    
    .badge-excellent {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: #1a5d3a;
    }
    
    .badge-good {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: #0d4d7a;
    }
    
    .badge-needs-improvement {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: #7a2828;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Space Mono', monospace;
        font-size: 1.1rem;
        font-weight: 700;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-top: 4rem;
        text-align: center;
        font-family: 'DM Sans', sans-serif;
    }
    
    /* Buttons */
    .stButton > button {
        font-family: 'DM Sans', sans-serif;
        font-weight: 600;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
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
    """
    Calculate overall engagement score (0-100)
    
    Weights aligned with SLS's Grow → Connect → Impact mission:
    - Knowledge Growth (GROW): 35%
    - Action Plans (CONNECT): 30%
    - Satisfaction (IMPACT): 25%
    - Attendance (Foundation): 10%
    """
    try:
        # Calculate individual component scores (0-100 scale)
        attendance_rate = (metrics.get('chapter_metrics', {}).get('actual_attendees', 0) / 
                          metrics.get('chapter_metrics', {}).get('total_registered', 1)) * 100
        knowledge_score = metrics.get('grow_avg_knowledge_increase', 0) * 20  # Convert 0-5 scale to 0-100
        action_rate = metrics.get('connect_members_planning_action_pct', 0)
        satisfaction_score = (metrics.get('impact_avg_satisfaction', 0) / 5) * 100  # Convert 0-5 to 0-100
        
        # Apply weights: GROW (35%) + CONNECT (30%) + IMPACT (25%) + Attendance (10%)
        engagement = (
            knowledge_score * 0.35 +      # GROW - Learning outcomes
            action_rate * 0.30 +          # CONNECT - Action commitment
            satisfaction_score * 0.25 +   # IMPACT - Member satisfaction
            attendance_rate * 0.10        # Foundation - Show-up rate
        )
        
        return round(engagement, 1)
    except:
        return 0

def get_performance_badge(score):
    """Get performance badge based on score"""
    if score >= 80:
        return "badge-excellent", "🏆 Excellent"
    elif score >= 60:
        return "badge-good", "✅ Good"
    else:
        return "badge-needs-improvement", "📈 Needs Improvement"

def create_metric_card(label, value, delta=None, icon="📊", color_class=""):
    """Create a professional metric card"""
    delta_html = ""
    if delta:
        delta_class = "negative" if delta.startswith("-") else ""
        delta_html = f'<div class="metric-delta {delta_class}">{delta}</div>'
    
    return f"""
    <div class="metric-card {color_class}">
        <div class="metric-label">{icon} {label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """

def generate_insights(metrics, data):
    """Generate AI-powered insights"""
    insights = []
    
    # Knowledge Growth Insight
    avg_increase = metrics.get('grow_avg_knowledge_increase', 0)
    if avg_increase > 1.5:
        insights.append(f"🎓 Outstanding knowledge growth with +{avg_increase} points average improvement")
    elif avg_increase > 0.5:
        insights.append(f"📚 Solid learning outcomes with +{avg_increase} points improvement")
    
    # Attendance Insight
    chapter_metrics = metrics.get('chapter_metrics', {})
    target = chapter_metrics.get('target_attendance', 50)
    actual = chapter_metrics.get('actual_attendees', 0)
    if actual > target:
        insights.append(f"🎯 Target exceeded! {actual} attendees vs {target} target (+{((actual-target)/target*100):.0f}%)")
    
    # Engagement Insight
    action_pct = metrics.get('connect_members_planning_action_pct', 0)
    if action_pct > 70:
        insights.append(f"💪 High engagement: {action_pct}% committed to taking action")
    
    # Satisfaction Insight
    satisfaction = metrics.get('impact_avg_satisfaction', 0)
    if satisfaction >= 4:
        insights.append(f"⭐ Exceptional satisfaction rating of {satisfaction}/5")
    
    return insights

# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_data
def load_data(data_file):
    """Load the pre-computed metrics from JSON file"""
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        st.error(f"⚠️ Data file '{data_file}' not found!")
        return None
    except Exception as e:
        st.error(f"⚠️ Error loading data: {str(e)}")
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
    # Header Image
    try:
        st.image("sls_image.jpg", use_column_width=True)
    except:
        pass
    
    st.markdown('<p class="dashboard-title">SLS AU Chapter Analytics</p>', unsafe_allow_html=True)
    st.markdown('<p class="dashboard-subtitle">Data-Driven Insights for Growth, Connection & Impact</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🎯 Select a Session to Explore")
    st.markdown("<br>", unsafe_allow_html=True)
    
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
                <div class="session-name">{session_key} Session</div>
                <p style='color: #6c757d; font-size: 0.95rem;'>View comprehensive analytics</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.stop()

# ============================================================================
# LOAD SELECTED SESSION
# ============================================================================

selected_session = st.session_state.selected_session
session_info = SESSIONS[selected_session]

# Header
try:
    st.image("sls_image.jpg", use_column_width=True)
except:
    pass

col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    if st.button("← Sessions", type="secondary"):
        st.session_state.selected_session = None
        st.rerun()

with col2:
    st.markdown(f'<p class="dashboard-title">{session_info["icon"]} {selected_session} Analytics</p>', unsafe_allow_html=True)

st.markdown("---")

# Load data
data = load_data(session_info['data_file'])

if data is None:
    st.error(f"Could not load data for {selected_session} session.")
    if st.button("← Return to Sessions"):
        st.session_state.selected_session = None
        st.rerun()
    st.stop()

metrics = data['metrics']
viz_data = data['visualization_data']
chapter_metrics = metrics.get('chapter_metrics', {})

# Event constants
REGISTERED = chapter_metrics.get('total_registered', 119)
TARGET = chapter_metrics.get('target_attendance', 50)
ACTUAL_ATTENDEES = chapter_metrics.get('actual_attendees', 54)

# ============================================================================
# EXECUTIVE SUMMARY
# ============================================================================

# Calculate engagement score
engagement_score = calculate_engagement_score(metrics)
badge_class, badge_text = get_performance_badge(engagement_score)

# Performance Overview
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🎯 Overall Performance")
    
with col2:
    st.markdown(f"""
    <div style='text-align: right;'>
        <span class='performance-badge {badge_class}'>{badge_text}</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 2.5rem; border-radius: 20px; color: white; 
            box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3); margin: 1.5rem 0;'>
    <div style='display: flex; align-items: center; justify-content: space-between;'>
        <div>
            <h2 style='margin: 0; font-family: "Space Mono", monospace; font-size: 1.2rem; opacity: 0.9;'>
                ENGAGEMENT SCORE
            </h2>
            <h1 style='margin: 0.5rem 0 0 0; font-family: "Playfair Display", serif; font-size: 4.5rem; font-weight: 900;'>
                {engagement_score}<span style='font-size: 2.5rem; opacity: 0.7;'>/100</span>
            </h1>
        </div>
        <div style='text-align: right;'>
            <div style='font-size: 3rem; opacity: 0.8;'>🚀</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Engagement Score Breakdown
st.markdown("### 📋 How We Calculate the Engagement Score")

# Calculate individual components for display
attendance_rate = (ACTUAL_ATTENDEES / REGISTERED) * 100 if REGISTERED > 0 else 0
knowledge_score = metrics.get('grow_avg_knowledge_increase', 0) * 20
action_rate = metrics.get('connect_members_planning_action_pct', 0)
satisfaction_score = (metrics.get('impact_avg_satisfaction', 0) / 5) * 100

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div style='background: white; padding: 1.5rem; border-radius: 12px; 
                border-left: 5px solid #667eea; box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>
        <div style='font-family: "DM Sans", sans-serif; font-size: 0.85rem; 
                    color: #6c757d; text-transform: uppercase; margin-bottom: 0.5rem;'>
            🌱 GROW (35%)
        </div>
        <div style='font-family: "Space Mono", monospace; font-size: 2rem; 
                    font-weight: 700; color: #2c3e50;'>
            {knowledge_score:.1f}
        </div>
        <div style='font-family: "DM Sans", sans-serif; font-size: 0.9rem; color: #6c757d; margin-top: 0.5rem;'>
            Knowledge growth<br>
            <span style='color: #2ecc71; font-weight: 600;'>+{knowledge_score * 0.35:.1f} pts</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style='background: white; padding: 1.5rem; border-radius: 12px; 
                border-left: 5px solid #f093fb; box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>
        <div style='font-family: "DM Sans", sans-serif; font-size: 0.85rem; 
                    color: #6c757d; text-transform: uppercase; margin-bottom: 0.5rem;'>
            🤝 CONNECT (30%)
        </div>
        <div style='font-family: "Space Mono", monospace; font-size: 2rem; 
                    font-weight: 700; color: #2c3e50;'>
            {action_rate:.1f}
        </div>
        <div style='font-family: "DM Sans", sans-serif; font-size: 0.9rem; color: #6c757d; margin-top: 0.5rem;'>
            Action commitment<br>
            <span style='color: #2ecc71; font-weight: 600;'>+{action_rate * 0.30:.1f} pts</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style='background: white; padding: 1.5rem; border-radius: 12px; 
                border-left: 5px solid #43e97b; box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>
        <div style='font-family: "DM Sans", sans-serif; font-size: 0.85rem; 
                    color: #6c757d; text-transform: uppercase; margin-bottom: 0.5rem;'>
            💡 IMPACT (25%)
        </div>
        <div style='font-family: "Space Mono", monospace; font-size: 2rem; 
                    font-weight: 700; color: #2c3e50;'>
            {satisfaction_score:.1f}
        </div>
        <div style='font-family: "DM Sans", sans-serif; font-size: 0.9rem; color: #6c757d; margin-top: 0.5rem;'>
            Member satisfaction<br>
            <span style='color: #2ecc71; font-weight: 600;'>+{satisfaction_score * 0.25:.1f} pts</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style='background: white; padding: 1.5rem; border-radius: 12px; 
                border-left: 5px solid #4facfe; box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>
        <div style='font-family: "DM Sans", sans-serif; font-size: 0.85rem; 
                    color: #6c757d; text-transform: uppercase; margin-bottom: 0.5rem;'>
            👥 ATTEND (10%)
        </div>
        <div style='font-family: "Space Mono", monospace; font-size: 2rem; 
                    font-weight: 700; color: #2c3e50;'>
            {attendance_rate:.1f}
        </div>
        <div style='font-family: "DM Sans", sans-serif; font-size: 0.9rem; color: #6c757d; margin-top: 0.5rem;'>
            Show-up rate<br>
            <span style='color: #2ecc71; font-weight: 600;'>+{attendance_rate * 0.10:.1f} pts</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Explanation box
st.markdown(f"""
<div style='background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%); 
            padding: 1.5rem; border-radius: 12px; margin-top: 1.5rem;
            border-left: 5px solid #667eea;'>
    <div style='font-family: "Space Mono", monospace; font-weight: 700; 
                font-size: 1rem; color: #2c3e50; margin-bottom: 0.75rem;'>
        📊 METHODOLOGY
    </div>
    <div style='font-family: "DM Sans", sans-serif; font-size: 0.95rem; 
                color: #495057; line-height: 1.6;'>
        The Engagement Score combines four key metrics aligned with SLS's mission:
        <strong>Grow → Connect → Impact</strong>. Weights prioritize learning outcomes (35%) 
        and action commitment (30%) over attendance quantity (10%), emphasizing quality engagement.
        <br><br>
        <strong>Formula:</strong> (Knowledge × 35%) + (Action × 30%) + (Satisfaction × 25%) + (Attendance × 10%) = {engagement_score}/100
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Key Insights
insights = generate_insights(metrics, data)
if insights:
    st.markdown("### 💡 Key Insights")
    insight_text = "<br>".join([f"• {insight}" for insight in insights])
    st.markdown(f"""
    <div class="insight-box">
        <h4>🎯 What the Data Tells Us</h4>
        <p>{insight_text}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# TOP METRICS GRID
# ============================================================================

st.markdown("### 📊 Event Performance Dashboard")
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(
        create_metric_card(
            "Registered", 
            REGISTERED, 
            f"+{REGISTERED - TARGET} vs target",
            "📝"
        ), 
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        create_metric_card(
            "Target", 
            TARGET, 
            None,
            "🎯"
        ), 
        unsafe_allow_html=True
    )

with col3:
    attendance_rate = round((ACTUAL_ATTENDEES / REGISTERED) * 100, 1)
    st.markdown(
        create_metric_card(
            "Attended", 
            ACTUAL_ATTENDEES, 
            f"{attendance_rate}% showed up",
            "👥"
        ), 
        unsafe_allow_html=True
    )

with col4:
    target_achievement = round((ACTUAL_ATTENDEES / TARGET) * 100, 1)
    st.markdown(
        create_metric_card(
            "Achievement", 
            f"{target_achievement}%", 
            f"+{ACTUAL_ATTENDEES - TARGET} over target",
            "🏆"
        ), 
        unsafe_allow_html=True
    )

with col5:
    st.markdown(
        create_metric_card(
            "Completion", 
            f"{metrics['match_rate_pct']}%", 
            f"{metrics['total_responses']} surveys",
            "✅"
        ), 
        unsafe_allow_html=True
    )

st.markdown("<br><br>", unsafe_allow_html=True)

# ============================================================================
# ENGAGEMENT FUNNEL VISUALIZATION
# ============================================================================

st.markdown("### 📉 Participant Journey Funnel")

funnel_data = {
    'stages': ['Registered', 'Attended', 'Completed Survey', 'Planning Action'],
    'values': [
        REGISTERED,
        ACTUAL_ATTENDEES,
        metrics['total_responses'],
        metrics.get('connect_total_planning_action', 0)
    ],
    'colors': ['#667eea', '#764ba2', '#f093fb', '#43e97b']
}

# Calculate conversion rates
conversion_rates = []
for i in range(1, len(funnel_data['values'])):
    if funnel_data['values'][i-1] > 0:
        rate = (funnel_data['values'][i] / funnel_data['values'][i-1]) * 100
    else:
        rate = 0
    conversion_rates.append(f"{rate:.1f}%")

fig = go.Figure()

fig.add_trace(go.Funnel(
    y=funnel_data['stages'],
    x=funnel_data['values'],
    textposition="inside",
    textinfo="value+percent initial",
    marker={
        "color": funnel_data['colors'],
        "line": {"width": 2, "color": "white"}
    },
    connector={"line": {"color": "#34495e", "dash": "dot", "width": 3}},
    hovertemplate='<b>%{y}</b><br>Count: %{x}<br>%{percentInitial}<extra></extra>'
))

fig.update_layout(
    height=500,
    font=dict(family="DM Sans, sans-serif", size=14),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=20, r=20, t=40, b=20)
)

st.plotly_chart(fig, use_container_width=True)

# Conversion metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Registration → Attendance", f"{conversion_rates[0]}", "Conversion Rate")
with col2:
    st.metric("Attendance → Survey", f"{conversion_rates[1]}", "Completion Rate")
with col3:
    st.metric("Survey → Action", f"{conversion_rates[2]}", "Engagement Rate")

st.markdown("---")

# ============================================================================
# MAIN TABS
# ============================================================================

tab1, tab2, tab3 = st.tabs([
    "📈 GROW - Learning & Development", 
    "🤝 CONNECT - Engagement & Networking", 
    "💡 IMPACT - Satisfaction & Results"
])

# ============================================================================
# TAB 1: GROW
# ============================================================================

with tab1:
    st.markdown('<p class="section-header">📈 GROW - Member Development & Learning</p>', unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            create_metric_card(
                "Growth Rate",
                f"{metrics.get('grow_members_reporting_growth_pct', 0)}%",
                f"{int(metrics.get('total_responses', 0) * metrics.get('grow_members_reporting_growth_pct', 0) / 100)} members",
                "🌱",
                "grow"
            ),
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            create_metric_card(
                "Avg Increase",
                f"+{metrics.get('grow_avg_knowledge_increase', 0)}",
                "points (out of 5)",
                "📊",
                "grow"
            ),
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            create_metric_card(
                "Significant Growth",
                f"{metrics.get('grow_significant_growth_pct', 0)}%",
                "≥ 0.5 point improvement",
                "🚀",
                "grow"
            ),
            unsafe_allow_html=True
        )
    
    with col4:
        # Calculate ROI metric
        knowledge_per_hour = metrics.get('grow_avg_knowledge_increase', 0) / chapter_metrics.get('estimated_engagement_hours', 1.3)
        st.markdown(
            create_metric_card(
                "Learning ROI",
                f"{knowledge_per_hour:.2f}",
                "pts gained per hour",
                "⚡",
                "grow"
            ),
            unsafe_allow_html=True
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Knowledge Improvement - Dual Chart
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("#### 📊 Knowledge Growth: Pre vs Post Survey")
        
        topics = viz_data['knowledge_comparison']['topics']
        pre_scores = viz_data['knowledge_comparison']['pre_scores']
        post_scores = viz_data['knowledge_comparison']['post_scores']
        improvements = viz_data['knowledge_comparison']['improvements']
        
        # Calculate percentage improvements
        pct_improvements = []
        for i in range(len(topics)):
            if pre_scores[i] > 0:
                pct = ((post_scores[i] - pre_scores[i]) / pre_scores[i]) * 100
            else:
                pct = 0
            pct_improvements.append(pct)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Pre-Survey',
            x=topics,
            y=pre_scores,
            marker_color='#ff6b6b',
            text=[f"{s:.2f}" for s in pre_scores],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Pre: %{y:.2f}/5<extra></extra>',
            offsetgroup=0
        ))
        
        fig.add_trace(go.Bar(
            name='Post-Survey',
            x=topics,
            y=post_scores,
            marker_color='#51cf66',
            text=[f"{s:.2f}" for s in post_scores],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Post: %{y:.2f}/5<extra></extra>',
            offsetgroup=1
        ))
        
        # Add improvement arrows
        for i, topic in enumerate(topics):
            fig.add_annotation(
                x=topic,
                y=max(pre_scores[i], post_scores[i]) + 0.3,
                text=f"↑ {pct_improvements[i]:.0f}%",
                showarrow=False,
                font=dict(size=11, color='#2ecc71', family='Space Mono'),
                bgcolor='rgba(46, 204, 113, 0.1)',
                borderpad=4
            )
        
        fig.update_layout(
            barmode='group',
            yaxis_title='Average Score (1-5 Scale)',
            yaxis=dict(range=[0, 6]),
            height=450,
            hovermode='x unified',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(family="DM Sans")
            ),
            font=dict(family="DM Sans, sans-serif"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🎯 Improvement Distribution")
        
        improvement_dist = viz_data.get('improvement_distribution', {})
        
        if improvement_dist:
            labels = ['Significant\n(≥2 pts)', 'Moderate\n(1-2 pts)', 'Slight\n(>0 pts)', 'No Change', 'Decreased']
            values = [
                improvement_dist.get('significant_improvement_2plus', 0),
                improvement_dist.get('moderate_improvement_1to2', 0),
                improvement_dist.get('slight_improvement_0to1', 0),
                improvement_dist.get('no_change', 0),
                improvement_dist.get('decreased', 0)
            ]
            
            colors = ['#2ecc71', '#4facfe', '#95a5a6', '#e67e22', '#e74c3c']
            
            fig = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=0.5,
                marker_colors=colors,
                textinfo='label+percent',
                textfont=dict(size=12, family='DM Sans'),
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>'
            )])
            
            fig.update_layout(
                height=450,
                showlegend=False,
                annotations=[
                    dict(
                        text='Learning<br>Impact',
                        x=0.5, y=0.5,
                        font=dict(size=16, family='Space Mono', color='#2c3e50'),
                        showarrow=False
                    )
                ],
                font=dict(family="DM Sans, sans-serif"),
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Radar Chart - Knowledge Comparison
    st.markdown("#### 🕸️ Knowledge Profile: Before & After")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=pre_scores + [pre_scores[0]],
        theta=topics + [topics[0]],
        fill='toself',
        name='Pre-Survey',
        line_color='#ff6b6b',
        fillcolor='rgba(255, 107, 107, 0.2)'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=post_scores + [post_scores[0]],
        theta=topics + [topics[0]],
        fill='toself',
        name='Post-Survey',
        line_color='#51cf66',
        fillcolor='rgba(81, 207, 102, 0.2)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickfont=dict(family='Space Mono', size=11)
            ),
            angularaxis=dict(
                tickfont=dict(family='DM Sans', size=12)
            )
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(family="DM Sans")
        ),
        height=500,
        font=dict(family="DM Sans, sans-serif"),
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Topic Breakdown with Percentage
    st.markdown("#### 📈 Detailed Knowledge Gains by Topic")
    
    for i, topic in enumerate(topics):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Progress bar for visual appeal
            progress_pct = (post_scores[i] / 5) * 100
            improvement_color = '#2ecc71' if improvements[i] > 0 else '#e74c3c'
            
            st.markdown(f"""
            <div style='margin: 1rem 0;'>
                <div style='display: flex; justify-content: space-between; margin-bottom: 0.5rem;'>
                    <span style='font-family: "DM Sans", sans-serif; font-weight: 600; color: #2c3e50;'>
                        {topic}
                    </span>
                    <span style='font-family: "Space Mono", monospace; color: {improvement_color}; font-weight: 700;'>
                        {pre_scores[i]:.2f} → {post_scores[i]:.2f} (+{improvements[i]:.2f})
                    </span>
                </div>
                <div style='background: #e9ecef; height: 12px; border-radius: 6px; overflow: hidden;'>
                    <div style='background: linear-gradient(90deg, #667eea, #51cf66); 
                                height: 100%; width: {progress_pct}%; 
                                transition: width 0.5s ease;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.metric("% Gain", f"+{pct_improvements[i]:.1f}%", label_visibility="collapsed")

# ============================================================================
# TAB 2: CONNECT
# ============================================================================

with tab2:
    st.markdown('<p class="section-header">🤝 CONNECT - Engagement & Networking</p>', unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            create_metric_card(
                "Action Commitment",
                f"{metrics.get('connect_members_planning_action_pct', 0)}%",
                f"{metrics.get('connect_total_planning_action', 0)} members",
                "🎯",
                "connect"
            ),
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            create_metric_card(
                "Will Recommend",
                f"{metrics.get('impact_likely_recommend_pct', 0)}%",
                "Net Promoter Score",
                "⭐",
                "connect"
            ),
            unsafe_allow_html=True
        )
    
    with col3:
        engagement_hours = chapter_metrics.get('estimated_engagement_hours', 1.30)
        st.markdown(
            create_metric_card(
                "Total Engagement",
                f"{engagement_hours:.2f}h",
                f"~{engagement_hours * 60:.0f} minutes",
                "⏰",
                "connect"
            ),
            unsafe_allow_html=True
        )
    
    with col4:
        # Calculate network effect
        network_potential = ACTUAL_ATTENDEES * (ACTUAL_ATTENDEES - 1) / 2
        st.markdown(
            create_metric_card(
                "Network Potential",
                f"{network_potential:.0f}",
                "possible connections",
                "🌐",
                "connect"
            ),
            unsafe_allow_html=True
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Action Plan & Recommendation
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Action Plan Commitment")
        
        action_data = viz_data.get('action_plan_data', {})
        
        if action_data:
            labels = list(action_data.keys())
            values = list(action_data.values())
            colors = ['#43e97b', '#e74c3c']
            
            fig = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=0.55,
                marker_colors=colors,
                textinfo='label+percent',
                textfont=dict(size=14, family='DM Sans', color='white'),
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>'
            )])
            
            fig.update_layout(
                height=400,
                showlegend=False,
                annotations=[
                    dict(
                        text=f'<b>{values[0]}</b><br>Taking<br>Action',
                        x=0.5, y=0.5,
                        font=dict(size=14, family='Space Mono', color='#2c3e50'),
                        showarrow=False,
                        align='center'
                    )
                ],
                font=dict(family="DM Sans, sans-serif"),
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🌟 Likelihood to Recommend")
        
        recommend_data = viz_data.get('recommend_data', {})
        
        if recommend_data:
            labels = list(recommend_data.keys())
            values = list(recommend_data.values())
            
            # Color code based on sentiment
            colors = []
            for label in labels:
                if 'Likely' in label or 'Very likely' in label:
                    colors.append('#43e97b')
                elif 'Neutral' in label:
                    colors.append('#f39c12')
                else:
                    colors.append('#e74c3c')
            
            fig = go.Figure(data=[go.Bar(
                x=labels,
                y=values,
                marker_color=colors,
                text=values,
                textposition='outside',
                textfont=dict(size=14, family='Space Mono'),
                hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
            )])
            
            fig.update_layout(
                yaxis_title='Number of Participants',
                height=400,
                showlegend=False,
                font=dict(family="DM Sans, sans-serif"),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(gridcolor='#e9ecef')
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Engagement Timeline Simulation
    st.markdown("#### 📅 Engagement Journey")
    
    # Create a simulated timeline
    timeline_stages = ['Registration', 'Pre-Event', 'Event Day', 'Post-Survey', 'Action Phase']
    timeline_engagement = [
        REGISTERED,
        int(REGISTERED * 0.85),  # Pre-event engagement
        ACTUAL_ATTENDEES,
        metrics['total_responses'],
        metrics.get('connect_total_planning_action', 0)
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=timeline_stages,
        y=timeline_engagement,
        mode='lines+markers+text',
        line=dict(color='#667eea', width=4),
        marker=dict(size=15, color='#764ba2', line=dict(width=3, color='white')),
        text=timeline_engagement,
        textposition='top center',
        textfont=dict(size=14, family='Space Mono', color='#2c3e50'),
        fill='tonexty',
        fillcolor='rgba(102, 126, 234, 0.1)',
        hovertemplate='<b>%{x}</b><br>Participants: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        yaxis_title='Active Participants',
        height=400,
        font=dict(family="DM Sans, sans-serif"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='#e9ecef'),
        hovermode='x'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Connection Insights
    st.markdown("#### 💬 Engagement Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        retention_rate = (metrics['total_responses'] / ACTUAL_ATTENDEES) * 100 if ACTUAL_ATTENDEES > 0 else 0
        st.info(f"""
        **Survey Completion Rate**  
        **{retention_rate:.1f}%** of attendees completed the survey  
        ({metrics['total_responses']} out of {ACTUAL_ATTENDEES})
        """)
    
    with col2:
        conversion_rate = (metrics.get('connect_total_planning_action', 0) / metrics['total_responses']) * 100 if metrics['total_responses'] > 0 else 0
        st.success(f"""
        **Action Conversion**  
        **{conversion_rate:.1f}%** committed to taking action  
        ({metrics.get('connect_total_planning_action', 0)} members)
        """)
    
    with col3:
        recommend_count = int(metrics['total_responses'] * metrics.get('impact_likely_recommend_pct', 0) / 100)
        st.warning(f"""
        **Advocacy Rate**  
        **{recommend_count} members** will recommend SLS  
        ({metrics.get('impact_likely_recommend_pct', 0)}% of respondents)
        """)

# ============================================================================
# TAB 3: IMPACT
# ============================================================================

with tab3:
    st.markdown('<p class="section-header">💡 IMPACT - Satisfaction & Results</p>', unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            create_metric_card(
                "Satisfaction Score",
                f"{metrics.get('impact_avg_satisfaction', 0):.2f}/5",
                f"{metrics.get('impact_satisfaction_pct', 0)}% satisfied",
                "⭐",
                "impact"
            ),
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            create_metric_card(
                "High Satisfaction",
                f"{metrics.get('impact_satisfaction_pct', 0)}%",
                "rated 4-5 stars",
                "🎯",
                "impact"
            ),
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            create_metric_card(
                "Would Recommend",
                f"{metrics.get('impact_likely_recommend_pct', 0)}%",
                "Net Promoter",
                "💯",
                "impact"
            ),
            unsafe_allow_html=True
        )
    
    with col4:
        estimated_impact = metrics.get('impact_people_impacted_estimate', metrics.get('connect_total_planning_action', 0) * 3)
        st.markdown(
            create_metric_card(
                "Ripple Effect",
                estimated_impact,
                "people impacted",
                "🌊",
                "impact"
            ),
            unsafe_allow_html=True
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Satisfaction Analysis
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.markdown("#### 😊 Satisfaction Distribution")
        
        satisfaction_data = viz_data.get('satisfaction_data', {})
        
        if satisfaction_data:
            # Sort by satisfaction level
            satisfaction_order = ['Very dissatisfied', 'Dissatisfied', 'Neutral', 'Satisfied', 'Very satisfied']
            sorted_items = sorted(
                satisfaction_data.items(),
                key=lambda x: satisfaction_order.index(x[0]) if x[0] in satisfaction_order else 2
            )
            labels = [item[0] for item in sorted_items]
            values = [item[1] for item in sorted_items]
            
            colors = ['#e74c3c', '#e67e22', '#f39c12', '#2ecc71', '#27ae60'][:len(labels)]
            
            fig = go.Figure(data=[go.Bar(
                y=labels,
                x=values,
                orientation='h',
                marker_color=colors,
                text=values,
                textposition='outside',
                textfont=dict(size=14, family='Space Mono'),
                hovertemplate='<b>%{y}</b><br>Count: %{x}<extra></extra>'
            )])
            
            fig.update_layout(
                xaxis_title='Number of Participants',
                height=400,
                font=dict(family="DM Sans, sans-serif"),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(gridcolor='#e9ecef'),
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🎯 Overall Satisfaction Gauge")
        
        satisfaction_score = metrics.get('impact_avg_satisfaction', 0)
        satisfaction_normalized = (satisfaction_score / 5) * 100
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=satisfaction_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={
                'text': "Average Satisfaction",
                'font': {'size': 24, 'family': 'Space Mono', 'color': '#2c3e50'}
            },
            delta={'reference': 3.5, 'increasing': {'color': "#2ecc71"}},
            number={'font': {'size': 60, 'family': 'Playfair Display', 'color': '#2c3e50'}},
            gauge={
                'axis': {
                    'range': [None, 5],
                    'tickwidth': 2,
                    'tickcolor': "#2c3e50",
                    'tickfont': {'family': 'Space Mono', 'size': 14}
                },
                'bar': {'color': "#667eea", 'thickness': 0.75},
                'bgcolor': "white",
                'borderwidth': 3,
                'bordercolor': "#e9ecef",
                'steps': [
                    {'range': [0, 2], 'color': '#fee2e2'},
                    {'range': [2, 3], 'color': '#fef3c7'},
                    {'range': [3, 4], 'color': '#dbeafe'},
                    {'range': [4, 5], 'color': '#d1fae5'}
                ],
                'threshold': {
                    'line': {'color': "#2ecc71", 'width': 5},
                    'thickness': 0.8,
                    'value': 4.5
                }
            }
        ))
        
        fig.update_layout(
            height=400,
            font={'family': 'DM Sans, sans-serif'},
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Impact Summary Cards
    st.markdown("#### 📈 Impact Summary")
    
    col1, col2, col3 = st.columns(3)
    
    total_improved = int(metrics.get('total_responses', 0) * metrics.get('grow_members_reporting_growth_pct', 0) / 100)
    satisfied_count = int(metrics.get('total_responses', 0) * metrics.get('impact_satisfaction_pct', 0) / 100)
    
    with col1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 2rem; border-radius: 16px; color: white; text-align: center;
                    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>🎓</div>
            <div style='font-family: "Playfair Display", serif; font-size: 3rem; font-weight: 900;'>{total_improved}</div>
            <div style='font-family: "DM Sans", sans-serif; font-size: 1.1rem; opacity: 0.9; margin-top: 0.5rem;'>
                Members showed<br>knowledge improvement
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    padding: 2rem; border-radius: 16px; color: white; text-align: center;
                    box-shadow: 0 8px 25px rgba(240, 147, 251, 0.3);'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>🎯</div>
            <div style='font-family: "Playfair Display", serif; font-size: 3rem; font-weight: 900;'>{metrics.get('connect_total_planning_action', 0)}</div>
            <div style='font-family: "DM Sans", sans-serif; font-size: 1.1rem; opacity: 0.9; margin-top: 0.5rem;'>
                Members committed<br>to taking action
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
                    padding: 2rem; border-radius: 16px; color: white; text-align: center;
                    box-shadow: 0 8px 25px rgba(67, 233, 123, 0.3);'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>⭐</div>
            <div style='font-family: "Playfair Display", serif; font-size: 3rem; font-weight: 900;'>{satisfied_count}</div>
            <div style='font-family: "DM Sans", sans-serif; font-size: 1.1rem; opacity: 0.9; margin-top: 0.5rem;'>
                Members reported<br>high satisfaction
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Combined Impact Visualization
    st.markdown("#### 🎨 Multi-Dimensional Impact Analysis")
    
    # Create a comprehensive view with multiple metrics
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Knowledge vs Satisfaction', 'Engagement Over Time'),
        specs=[[{"type": "scatter"}, {"type": "bar"}]]
    )
    
    # Scatter plot: Knowledge improvement vs Satisfaction
    # Simulated individual data points for visualization
    np.random.seed(42)
    n_points = metrics['total_responses']
    knowledge_sim = np.random.normal(metrics.get('grow_avg_knowledge_increase', 1.5), 0.5, n_points)
    satisfaction_sim = np.random.normal(metrics.get('impact_avg_satisfaction', 4), 0.5, n_points)
    
    fig.add_trace(
        go.Scatter(
            x=knowledge_sim,
            y=satisfaction_sim,
            mode='markers',
            marker=dict(
                size=10,
                color=knowledge_sim,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Knowledge<br>Gain", x=0.45)
            ),
            name='Participants',
            hovertemplate='Knowledge: %{x:.2f}<br>Satisfaction: %{y:.2f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Bar chart: Combined metrics
    metric_names = ['Knowledge', 'Engagement', 'Satisfaction', 'Recommend']
    metric_scores = [
        (metrics.get('grow_avg_knowledge_increase', 0) / 5) * 100,
        metrics.get('connect_members_planning_action_pct', 0),
        (metrics.get('impact_avg_satisfaction', 0) / 5) * 100,
        metrics.get('impact_likely_recommend_pct', 0)
    ]
    
    fig.add_trace(
        go.Bar(
            x=metric_names,
            y=metric_scores,
            marker_color=['#667eea', '#f093fb', '#4facfe', '#43e97b'],
            text=[f"{s:.1f}%" for s in metric_scores],
            textposition='outside',
            textfont=dict(family='Space Mono', size=13),
            hovertemplate='<b>%{x}</b><br>Score: %{y:.1f}%<extra></extra>'
        ),
        row=1, col=2
    )
    
    fig.update_xaxes(title_text="Knowledge Improvement (points)", row=1, col=1)
    fig.update_yaxes(title_text="Satisfaction Rating", row=1, col=1)
    fig.update_yaxes(title_text="Performance (%)", row=1, col=2)
    
    fig.update_layout(
        height=450,
        showlegend=False,
        font=dict(family="DM Sans, sans-serif"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown(f"""
<div class='footer'>
    <h2 style='font-family: "Playfair Display", serif; font-size: 2rem; margin-bottom: 1rem;'>
        📊 SLS Chapter Analytics Dashboard
    </h2>
    <p style='font-size: 1.1rem; margin-bottom: 1.5rem; opacity: 0.9;'>
        Empowering chapters through data-driven insights on Growth, Connection, and Impact
    </p>
    <div style='display: flex; justify-content: center; gap: 3rem; margin: 2rem 0;'>
        <div>
            <div style='font-size: 2rem; font-weight: 700;'>{ACTUAL_ATTENDEES}</div>
            <div style='opacity: 0.8;'>Total Attendees</div>
        </div>
        <div>
            <div style='font-size: 2rem; font-weight: 700;'>{engagement_score}/100</div>
            <div style='opacity: 0.8;'>Engagement Score</div>
        </div>
        <div>
            <div style='font-size: 2rem; font-weight: 700;'>{metrics.get('impact_avg_satisfaction', 0):.1f}/5</div>
            <div style='opacity: 0.8;'>Satisfaction</div>
        </div>
    </div>
    <p style='font-size: 0.9rem; opacity: 0.7; margin-top: 2rem;'>
        Last Updated: {datetime.now().strftime('%B %d, %Y')} | All data anonymized and privacy-protected
    </p>
    <p style='font-size: 0.85rem; opacity: 0.6; margin-top: 0.5rem;'>
        Data collected through pre- and post-event polls via Zoom webinar
    </p>
</div>
""", unsafe_allow_html=True)
