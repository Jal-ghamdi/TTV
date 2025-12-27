import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="SLS AU Chapter KPI Dashboard", 
    layout="wide", 
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# ============================================================================
# HEADER IMAGE
# ============================================================================

st.image(
    "sls_image.jpg",
    use_container_width=True
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 2rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #3498db;
    }
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .grow-metric {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    .connect-metric {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    .impact-metric {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 1.2rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# LOAD DATA FROM JSON FILE
# ============================================================================

@st.cache_data
def load_data():
    """Load the pre-computed metrics from JSON file"""
    # In production, this file should be in your GitHub repo
    with open('sls_kpi_data.json', 'r') as f:
        data = json.load(f)
    return data

# Load data
try:
    data = load_data()
    metrics = data['metrics']
    viz_data = data['visualization_data']
    chapter_metrics = metrics.get('chapter_metrics', {})  # Load chapter_metrics here
except FileNotFoundError:
    st.error("⚠️ Data file not found! Please ensure 'sls_kpi_data.json' is in the same directory.")
    st.stop()
except Exception as e:
    st.error(f"⚠️ Error loading data: {str(e)}")
    st.stop()

# Event attendance constants
REGISTERED = 119
TARGET = 50
ACTUAL_ATTENDEES = 54

# ============================================================================
# HEADER
# ============================================================================

st.markdown('<p class="main-header">📊 SLS Chapter KPI Dashboard</p>', unsafe_allow_html=True)
st.markdown("### Measuring Growth, Connection, and Impact")
st.markdown("---")

# ============================================================================
# TOP-LEVEL KPIs
# ============================================================================

# Event Performance Metrics
st.markdown("### 🎯 Event Performance Overview")

col1, col2, col3, col4, col5 = st.columns(5)

# Attendance metrics from your data
REGISTERED = 119
TARGET = 50
ACTUAL_ATTENDEES = 54

with col1:
    st.metric(
        label="📝 Registered",
        value=REGISTERED,
        delta=f"+{REGISTERED - TARGET} vs target",
        help="Total number of registrations"
    )

with col2:
    st.metric(
        label="🎯 Target",
        value=TARGET,
        help="Target attendance goal"
    )

with col3:
    attendance_rate = round((ACTUAL_ATTENDEES / REGISTERED) * 100, 1)
    st.metric(
        label="👥 Actual Attendees",
        value=ACTUAL_ATTENDEES,
        delta=f"{attendance_rate}% of registered",
        help="Number of people who actually attended"
    )

with col4:
    target_achievement = round((ACTUAL_ATTENDEES / TARGET) * 100, 1)
    st.metric(
        label="🏆 Target Achievement",
        value=f"{target_achievement}%",
        delta=f"+{ACTUAL_ATTENDEES - TARGET} attendees",
        help="Percentage of target achieved"
    )

with col5:
    st.metric(
        label="✅ Survey Completion",
        value=f"{metrics['match_rate_pct']}%",
        delta=f"{metrics['total_responses']} completed both",
        help="Percentage who completed both pre and post surveys"
    )

st.markdown("<br>", unsafe_allow_html=True)

# Impact & Engagement Metrics
st.markdown("### 📊 Impact & Engagement Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📋 Survey Responses (Pre)",
        value=metrics['total_participants_pre'],
        help="Total pre-survey responses"
    )

with col2:
    if 'grow_avg_knowledge_increase' in metrics:
        st.metric(
            label="📈 Avg Knowledge Increase",
            value=f"+{metrics['grow_avg_knowledge_increase']} pts",
            delta="out of 5",
            delta_color="normal"
        )

with col3:
    if 'impact_avg_satisfaction' in metrics:
        st.metric(
            label="⭐ Avg Satisfaction",
            value=f"{metrics['impact_avg_satisfaction']}/5",
            delta=f"{metrics.get('impact_satisfaction_pct', 0)}% satisfied"
        )

with col4:
    engagement_hours = metrics.get('chapter_metrics', {}).get('estimated_engagement_hours', 0)
    st.metric(
        label="⏰ Total Engagement",
        value="1.30 h"
        #value=f"{engagement_hours}h",
        help="Total member engagement hours"
    )

st.markdown("---")

# ============================================================================
# MAIN TABS
# ============================================================================

tab1, tab2, tab3 = st.tabs([
    "📈 GROW", 
    "🤝 CONNECT", 
    "💡 IMPACT"
])


# ============================================================================
# TAB 1: GROW
# ============================================================================

with tab1:
    st.markdown('<p class="section-header">📈 GROW - Member Development & Learning</p>', unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-container grow-metric">', unsafe_allow_html=True)
        st.metric(
            label="Members Reporting Growth",
            value=f"{metrics.get('grow_members_reporting_growth_pct', 0)}%",
            help="% of members who showed knowledge improvement"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-container grow-metric">', unsafe_allow_html=True)
        st.metric(
            label="Avg Knowledge Increase",
            value=f"+{metrics.get('grow_avg_knowledge_increase', 0)} points",
            help="Average increase in knowledge scores (1-5 scale)"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-container grow-metric">', unsafe_allow_html=True)
        st.metric(
            label="Significant Growth",
            value=f"{metrics.get('grow_significant_growth_pct', 0)}%",
            help="% with improvement ≥ 0.5 points"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Knowledge Improvement Chart
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 📊 Knowledge Improvement: Pre vs Post Survey")
        
        topics = viz_data['knowledge_comparison']['topics']
        pre_scores = viz_data['knowledge_comparison']['pre_scores']
        post_scores = viz_data['knowledge_comparison']['post_scores']
        
        # Calculate percentage improvements for display
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
            marker_color='#ff7f0e',
            text=[f"{s:.2f}" for s in pre_scores],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Pre-Survey: %{y:.2f}/5<extra></extra>'
        ))
        
        fig.add_trace(go.Bar(
            name='Post-Survey',
            x=topics,
            y=post_scores,
            marker_color='#1f77b4',
            text=[f"{s:.2f}<br>(+{pct:.0f}%)" for s, pct in zip(post_scores, pct_improvements)],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Post-Survey: %{y:.2f}/5<extra></extra>'
        ))
        
        fig.update_layout(
            barmode='group',
            yaxis_title='Average Score (1-5)',
            yaxis=dict(range=[0, 5.5]),
            height=450,
            hovermode='x unified',
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📈 Improvement Breakdown")
        
        improvement_dist = viz_data.get('improvement_distribution', {})
        
        if improvement_dist:
            labels = ['Significant (≥2)', 'Moderate (1-2)', 'Slight (>0)', 'No Change', 'Decreased']
            values = [
                improvement_dist.get('significant_improvement_2plus', 0),
                improvement_dist.get('moderate_improvement_1to2', 0),
                improvement_dist.get('slight_improvement_0to1', 0),
                improvement_dist.get('no_change', 0),
                improvement_dist.get('decreased', 0)
            ]
            
            fig = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=0.4,
                marker_colors=['#2ecc71', '#3498db', '#95a5a6', '#e67e22', '#e74c3c'],
                textinfo='label+percent',
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            )])
            
            fig.update_layout(
                height=450,
                showlegend=False,
                annotations=[dict(text='Improvement', x=0.5, y=0.5, font_size=16, showarrow=False)]
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Individual Topic Improvements with Percentage
    st.markdown("#### 🎯 Knowledge Improvement by Topic (Points & Percentage)")
    
    improvements = viz_data['knowledge_comparison']['improvements']
    
    # Calculate percentage improvement
    improvement_percentages = []
    for i, topic in enumerate(topics):
        if pre_scores[i] > 0:
            pct_change = ((post_scores[i] - pre_scores[i]) / pre_scores[i]) * 100
        else:
            pct_change = 0 if post_scores[i] == 0 else 100
        improvement_percentages.append(pct_change)
    
    # Create subplot with two y-axes
    fig = go.Figure()
    
    colors = ['#2ecc71' if imp > 0 else '#e74c3c' for imp in improvements]
    
    # Bar chart for point improvements
    fig.add_trace(go.Bar(
        x=topics,
        y=improvements,
        name='Points Improvement',
        marker_color=colors,
        text=[f"+{imp:.2f} pts" if imp > 0 else f"{imp:.2f} pts" for imp in improvements],
        textposition='outside',
        yaxis='y',
        hovertemplate='<b>%{x}</b><br>Points: %{y:.2f}<extra></extra>'
    ))
    
    # Line chart for percentage improvement
    fig.add_trace(go.Scatter(
        x=topics,
        y=improvement_percentages,
        name='% Improvement',
        mode='lines+markers+text',
        marker=dict(size=12, color='#e74c3c', line=dict(width=2, color='white')),
        line=dict(width=3, color='#e74c3c'),
        text=[f"+{pct:.1f}%" if pct > 0 else f"{pct:.1f}%" for pct in improvement_percentages],
        textposition='top center',
        yaxis='y2',
        hovertemplate='<b>%{x}</b><br>Percentage: %{y:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        yaxis=dict(title='Points Improvement', side='left'),
        yaxis2=dict(title='% Improvement', overlaying='y', side='right'),
        height=450,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Summary cards showing percentage improvements
    st.markdown("#### 📊 Percentage Improvement Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if len(improvement_percentages) > 0:
            st.info(f"**{topics[0]}**\n\n{pre_scores[0]:.2f} → {post_scores[0]:.2f}\n\n**+{improvement_percentages[0]:.1f}%** improvement")
    
    with col2:
        if len(improvement_percentages) > 1:
            st.success(f"**{topics[1]}**\n\n{pre_scores[1]:.2f} → {post_scores[1]:.2f}\n\n**+{improvement_percentages[1]:.1f}%** improvement")
    
    with col3:
        if len(improvement_percentages) > 2:
            st.warning(f"**{topics[2]}**\n\n{pre_scores[2]:.2f} → {post_scores[2]:.2f}\n\n**+{improvement_percentages[2]:.1f}%** improvement")

# ============================================================================
# TAB 2: CONNECT
# ============================================================================

with tab2:
    st.markdown('<p class="section-header">🤝 CONNECT - Networking & Collaboration</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-container connect-metric">', unsafe_allow_html=True)
        st.metric(
            label="Members Planning Action",
            value=f"{metrics.get('connect_members_planning_action_pct', 0)}%",
            help="% of members who plan to take action after the event"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-container connect-metric">', unsafe_allow_html=True)
        st.metric(
            label="Total Planning Action",
            value=metrics.get('connect_total_planning_action', 0),
            help="Number of members planning to take action"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-container connect-metric">', unsafe_allow_html=True)
        st.metric(
            label="Likely to Recommend",
            value=f"{metrics.get('impact_likely_recommend_pct', 0)}%",
            help="% of members likely to recommend SLS to others"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Action Plan Visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Action Plan Commitment")
        
        action_data = viz_data.get('action_plan_data', {})
        
        if action_data:
            fig = go.Figure(data=[go.Pie(
                labels=list(action_data.keys()),
                values=list(action_data.values()),
                hole=0.5,
                marker_colors=['#2ecc71', '#e74c3c'],
                textinfo='label+percent+value',
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            )])
            
            fig.update_layout(
                height=400,
                annotations=[dict(text='Action<br>Plan', x=0.5, y=0.5, font_size=16, showarrow=False)]
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🌟 Recommendation Likelihood")
        
        recommend_data = viz_data.get('recommend_data', {})
        
        if recommend_data:
            fig = go.Figure(data=[go.Bar(
                x=list(recommend_data.keys()),
                y=list(recommend_data.values()),
                marker_color='#3498db',
                text=list(recommend_data.values()),
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
            )])
            
            fig.update_layout(
                yaxis_title='Number of Participants',
                height=400,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Engagement Funnel
    st.markdown("#### 📊 Engagement & Connection Funnel")
    
    funnel_stages = ['Knowledge Improved', 'Planning Action'] #'Attended Event', 'Completed Surveys', 
    funnel_values = [
        #metrics.get('total_participants_pre', 0),
        #metrics.get('total_responses', 0),
        int(metrics.get('total_responses', 0) * metrics.get('grow_members_reporting_growth_pct', 0) / 100),
        metrics.get('connect_total_planning_action', 0)
    ]
    
    fig = go.Figure(go.Funnel(
        y=funnel_stages,
        x=funnel_values,
        textinfo="value+percent initial",
        marker={"color": ["#3498db", "#2ecc71", "#f39c12", "#e74c3c"]},
        connector={"line": {"color": "#34495e", "dash": "dot", "width": 3}}
    ))
    
    fig.update_layout(height=450)
    
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAB 3: IMPACT
# ============================================================================

with tab3:
    st.markdown('<p class="section-header">💡 IMPACT - Member Satisfaction & Results</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-container impact-metric">', unsafe_allow_html=True)
        st.metric(
            label="Avg Satisfaction",
            value=f"{metrics.get('impact_avg_satisfaction', 0)}/5",
            help="Average satisfaction score"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-container impact-metric">', unsafe_allow_html=True)
        st.metric(
            label="Satisfaction Rate",
            value=f"{metrics.get('impact_satisfaction_pct', 0)}%",
            help="% with satisfaction ≥ 4"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-container impact-metric">', unsafe_allow_html=True)
        st.metric(
            label="Recommend Rate",
            value=f"{metrics.get('impact_likely_recommend_pct', 0)}%",
            help="% likely to recommend"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-container impact-metric">', unsafe_allow_html=True)
        estimated_impact = metrics.get('impact_people_impacted_estimate', metrics.get('connect_total_planning_action', 0) * 3)
        st.metric(
            label="Est. People Impacted",
            value=estimated_impact,
            help="Estimated reach through member actions"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Satisfaction Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 😊 Satisfaction Distribution")
        
        satisfaction_data = viz_data.get('satisfaction_data', {})
        
        if satisfaction_data:
            # Sort by satisfaction level
            sorted_items = sorted(satisfaction_data.items(), 
                                 key=lambda x: ['Very dissatisfied', 'Dissatisfied', 'Neutral', 'Satisfied', 'Very satisfied'].index(x[0]) 
                                 if x[0] in ['Very dissatisfied', 'Dissatisfied', 'Neutral', 'Satisfied', 'Very satisfied'] else 2)
            labels = [item[0] for item in sorted_items]
            values = [item[1] for item in sorted_items]
            
            colors = ['#e74c3c', '#e67e22', '#f39c12', '#2ecc71', '#27ae60'][:len(labels)]
            
            fig = go.Figure(data=[go.Bar(
                x=labels,
                y=values,
                marker_color=colors,
                text=values,
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
            )])
            
            fig.update_layout(
                yaxis_title='Number of Participants',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Overall Impact Metrics")
        
        # Create a gauge chart for satisfaction
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=metrics.get('impact_avg_satisfaction', 0),
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Average Satisfaction", 'font': {'size': 20}},
            delta={'reference': 3, 'increasing': {'color': "#2ecc71"}},
            gauge={
                'axis': {'range': [None, 5], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#3498db"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 2], 'color': '#e74c3c'},
                    {'range': [2, 3], 'color': '#f39c12'},
                    {'range': [3, 4], 'color': '#f1c40f'},
                    {'range': [4, 5], 'color': '#2ecc71'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 4.5
                }
            }
        ))
        
        fig.update_layout(height=400, font={'size': 16})
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Impact Summary
    st.markdown("#### 🎯 Impact Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_improved = int(metrics.get('total_responses', 0) * metrics.get('grow_members_reporting_growth_pct', 0) / 100)
        st.info(f"**{total_improved}** members showed knowledge improvement")
    
    with col2:
        st.success(f"**{metrics.get('connect_total_planning_action', 0)}** members committed to taking action")
    
    with col3:
        satisfied = int(metrics.get('total_responses', 0) * metrics.get('impact_satisfaction_pct', 0) / 100)
        st.warning(f"**{satisfied}** members reported high satisfaction")

# ============================================================================
# TAB 4: CHAPTER ACTIVITIES
# ============================================================================

#with tab4:
  #  st.markdown('<p class="section-header">📊 CHAPTER ACTIVITIES & ENGAGEMENT</p>', unsafe_allow_html=True)
    
  #  chapter_metrics = metrics.get('chapter_metrics', {})
    
    # Attendance & Registration Metrics
  #  st.markdown("#### 📈 Attendance & Registration Metrics")
    
#    col1, col2, col3, col4, col5 = st.columns(5)
    
  #  with col1:
  #      st.metric(
  #          label="📝 Total Registrations",
  #          value=REGISTERED,
  #          help="Total number of event registrations"
  #      )
    
  #  with col2:
  #      st.metric(
  #          label="🎯 Target Attendance",
   #         value=TARGET,
   #         help="Target attendance goal"
    #    )
    
   # with col3:
  #      st.metric(
  #          label="👥 Actual Attendees",
  #          value=ACTUAL_ATTENDEES,
  #          delta=f"+{ACTUAL_ATTENDEES - TARGET} vs target",
   #         help="Number of people who actually attended"
   #     )
    
   # with col4:
   #     attendance_rate = round((ACTUAL_ATTENDEES / REGISTERED) * 100, 1)
   #     st.metric(
   #         label="📊 Attendance Rate",
   #         value=f"{attendance_rate}%",
   #         help="Actual attendees / Registrations"
   #     )
    
  #  with col5:
   #     target_achievement = round((ACTUAL_ATTENDEES / TARGET) * 100, 1)
   #     st.metric(
   #         label="🏆 Target Achievement",
    #        value=f"{target_achievement}%",
    #        help="Achievement vs target"
    #    )
    
 #   st.markdown("<br>", unsafe_allow_html=True)
    
    # Attendance Funnel
#    st.markdown("#### 🎯 Event Attendance Funnel")
    
#    funnel_stages = ['Registered', 'Target', 'Attended', 'Completed Pre-Survey', 'Completed Both Surveys']
#    funnel_values = [
#        REGISTERED,
 #       TARGET,
#        ACTUAL_ATTENDEES,
 #       metrics.get('total_participants_pre', 0),
 #       metrics.get('total_responses', 0)
 #   ]
    
 #   fig = go.Figure(go.Funnel(
   #     y=funnel_stages,
   #     x=funnel_values,
   #     textinfo="value+percent initial",
  #      marker={
    #        "color": ["#3498db", "#9b59b6", "#2ecc71", "#f39c12", "#e74c3c"],
   #         "line": {"width": 2, "color": "white"}
   #     },
    #    connector={"line": {"color": "#34495e", "dash": "dot", "width": 3}}
  #  ))
    
  #  fig.update_layout(height=450)
    
  #  st.plotly_chart(fig, use_container_width=True)
    
    # Activity Metrics
   # st.markdown("#### 📋 Survey & Engagement Metrics")
    
 #   col1, col2, col3, col4 = st.columns(4)
    
  #  with col1:
  #      st.metric(
   #         label="Event Name",
   #         value=chapter_metrics.get('event_name', 'N/A')
   #     )
    
  #  with col2:
  #      st.metric(
   #         label="Survey Completion",
    #        value=f"{chapter_metrics.get('completion_rate_pct', 0)}%",
     #       help="% who completed both surveys"
      #  )
    
   # with col3:
    #    st.metric(
     #       label="Engagement Hours",
      #      value=f"{chapter_metrics.get('estimated_engagement_hours', 0)}h",
       #     help="Estimated total engagement hours"
        #)
    
  #  with col4:
   #     response_rate = round((metrics.get('total_participants_pre', 0) / ACTUAL_ATTENDEES) * 100, 1) if ACTUAL_ATTENDEES > 0 else 0
    #    st.metric(
     #       label="Pre-Survey Response",
      #      value=f"{response_rate}%",
       #     help="% of attendees who completed pre-survey"
        #)
    
    #st.markdown("<br>", unsafe_allow_html=True)
    
    # Activities Breakdown
    #col1, col2 = st.columns([1, 1])
    
    #with col1:
     #   st.markdown("#### 📈 Knowledge Score Distribution - Pre Survey")
        
      #  pre_dist = viz_data.get('pre_score_distribution', {})
        
       # if pre_dist:
        #    labels = [f"Score {k}" for k in pre_dist.keys()]
         #   values = list(pre_dist.values())
            
         #   fig = go.Figure(data=[go.Bar(
          #      x=labels,
           #     y=values,
            #    marker_color='#ff7f0e',
             #   text=values,
              #  textposition='outside',
               # hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
            #)])
            
         #   fig.update_layout(
          #      yaxis_title='Number of Participants',
           #     height=400
            #)
            
          #  st.plotly_chart(fig, use_container_width=True)
    
    #with col2:
     #   st.markdown("#### 📈 Knowledge Score Distribution - Post Survey")
        
      #  post_dist = viz_data.get('post_score_distribution', {})
        
       # if post_dist:
        #    labels = [f"Score {k}" for k in post_dist.keys()]
         #   values = list(post_dist.values())
            
          #  fig = go.Figure(data=[go.Bar(
           #     x=labels,
            #    y=values,
             #   marker_color='#1f77b4',
              #  text=values,
               # textposition='outside',
                #hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
           # )])
            
            #fig.update_layout(
             #   yaxis_title='Number of Participants',
              #  height=400
            #)
            
           # st.plotly_chart(fig, use_container_width=True)
    
    # Satisfaction vs Recommendation
    #st.markdown("#### ⭐ Satisfaction vs Recommendation Correlation")
    
   # col1, col2 = st.columns(2)
    
    #with col1:
     #   satisfaction_data = viz_data.get('satisfaction_data', {})
      #  if satisfaction_data:
       #     fig = px.pie(
        #        names=list(satisfaction_data.keys()),
         #       values=list(satisfaction_data.values()),
          #      title='Satisfaction Breakdown',
           #     color_discrete_sequence=px.colors.diverging.RdYlGn
            #)
            #fig.update_traces(textposition='inside', textinfo='percent+label')
            #fig.update_layout(height=400)
            #st.plotly_chart(fig, use_container_width=True)
    
    #with col2:
     #   recommend_data = viz_data.get('recommend_data', {})
      #  if recommend_data:
       #     fig = px.pie(
        #        names=list(recommend_data.keys()),
         #       values=list(recommend_data.values()),
          #      title='Recommendation Likelihood Breakdown',
           #     color_discrete_sequence=px.colors.sequential.Blues
            #)
            #fig.update_traces(textposition='inside', textinfo='percent+label')
            #fig.update_layout(height=400)
            #st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 2rem;'>
    <p style='font-size: 1.1rem;'><strong>📊 SLS Chapter KPI Dashboard</strong></p>
    <p>Tracking Growth, Connection, and Impact through data-driven insights</p>
    <p style='font-size: 0.9rem;'>Last Updated: {}</p>
    <p style='font-size: 0.8rem;'>All data has been fully anonymized, and participant privacy has been strictly maintained. Data for this event was collected through pre- and post-event polls conducted during the Zoom webinar.</p>
</div>
""".format(datetime.now().strftime('%B %d, %Y')), unsafe_allow_html=True)
