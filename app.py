import streamlit as st
import os
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="PulseMetrics: Health & Fitness Analytics", 
    page_icon="💓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ENHANCED TYPOGRAPHY & MODERN SIDEBAR CSS ---
st.markdown("""
    <style>
        /* Global Font Size & Clean Smoothing */
        html, body, [class*="css"] {
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            font-size: 16px;
        }
        
        /* Main Page Headers */
        .main-title {
            font-size: 36px !important;
            font-weight: 800 !important;
            color: #FFFFFF !important;
            letter-spacing: -0.03em;
        }
        
        .sub-title {
            font-size: 18px !important;
            color: #94A3B8 !important;
            font-weight: 400;
            margin-bottom: 25px;
        }
        
        /* Modern Dark Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #0F172A;
            border-right: 1px solid #1E293B;
            padding-top: 10px;
        }
        
        /* Sidebar Radio Navigation Items */
        [data-testid="stSidebar"] .stRadio label {
            font-size: 15px !important;
            font-weight: 600 !important;
            color: #CBD5E1 !important;
            padding: 10px 14px;
            border-radius: 10px;
            margin-bottom: 5px;
            transition: all 0.2s ease;
        }
        
        [data-testid="stSidebar"] .stRadio label:hover {
            background-color: #1E293B;
            color: #FFFFFF !important;
            cursor: pointer;
        }
        
        /* Highlighted Card Container Styling */
        .metric-card {
            background-color: #1E293B;
            border: 1px solid #334155;
            padding: 24px;
            border-radius: 16px;
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
            text-align: center;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-4px);
            border-color: #3B82F6;
        }
        
        .metric-title {
            font-size: 13px;
            color: #94A3B8;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 10px;
        }
        
        .metric-value {
            font-size: 30px;
            font-weight: 800;
            color: #38BDF8;
        }
        
        /* Insight Cards Styling */
        .insight-box {
            background-color: #1E293B;
            border-left: 5px solid #3B82F6;
            padding: 20px;
            border-radius: 0 12px 12px 0;
            margin-bottom: 15px;
            color: #E2E8F0;
        }
    </style>
""", unsafe_allow_html=True)

# --- DATABASE CONNECTION & AUTO-BUILDING ---
@st.cache_resource
def load_data():
    db_file = 'fitbit_data.db'
    csv_file = 'master_merged_fitbit_data.csv' # Make sure this matches your CSV filename!
    
    # If database doesn't exist (like on Streamlit Cloud), build it from the CSV
    if not os.path.exists(db_file):
        if os.path.exists(csv_file):
            conn = sqlite3.connect(db_file, check_same_thread=False)
            temp_df = pd.read_csv(csv_file)
            temp_df.to_sql('master_data', conn, if_exists='replace', index=False)
            conn.close()
        else:
            st.error(f"Critical Error: Neither '{db_file}' nor '{csv_file}' found in repository!")
            return pd.DataFrame()

    # Normal connection once database exists
    conn = sqlite3.connect(db_file, check_same_thread=False)
    df = pd.read_sql("SELECT * FROM master_data", conn)
    conn.close()
    return df

master_df = load_data()

# --- PROMINENT SAAS BRANDING HEADER IN SIDEBAR ---
st.sidebar.markdown("""
    <div style="background: linear-gradient(135deg, #1E293B, #0F172A); border: 1px solid #334155; padding: 20px; border-radius: 16px; text-align: center; margin-bottom: 20px; box-shadow: 0 6px 16px rgba(0,0,0,0.3);">
        <div style="font-size: 40px; margin-bottom: 6px;">💓</div>
        <div style="font-size: 22px; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em;">PulseMetrics</div>
        <div style="font-size: 11px; font-weight: 700; color: #38BDF8; text-transform: uppercase; letter-spacing: 0.12em; margin-top: 4px;">Intelligence Suite</div>
    </div>
""", unsafe_allow_html=True)

nav = st.sidebar.radio(
    "Navigation Workspace", 
    [
        "📊 Executive Overview", 
        "🎯 User Behavioral Segmentation", 
        "📈 Deep Correlation Hub", 
        "💡 Strategic Insights", 
        "⚙️ SQL Engine & Sandbox"
    ]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Global Data Filters")
selected_users = st.sidebar.multiselect("Filter Specific User IDs:", options=master_df['Id'].unique())

# Filter dataframe
df = master_df[master_df['Id'].isin(selected_users)] if selected_users else master_df

# ==========================================
# PAGE 1: EXECUTIVE OVERVIEW
# ==========================================
if nav == "📊 Executive Overview":
    st.markdown('<p class="main-title">PulseMetrics Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Smart Device Intelligence & Biometric Insights Suite</p>', unsafe_allow_html=True)

    total_users = df['Id'].nunique()
    avg_steps = int(df['TotalSteps'].mean())
    avg_calories = int(df['Calories'].mean())
    avg_sedentary = int(df['SedentaryMinutes'].mean())
    mean_sleep = df['TotalMinutesAsleep'].mean() if ('TotalMinutesAsleep' in df.columns and not df['TotalMinutesAsleep'].dropna().empty) else 0
    avg_sleep = int(mean_sleep) if pd.notna(mean_sleep) else 0
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Active Users</div><div class="metric-value">{total_users}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Daily Steps</div><div class="metric-value">{avg_steps:,}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Calories</div><div class="metric-value">{avg_calories:,}</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Sedentary</div><div class="metric-value">{avg_sedentary}m</div></div>', unsafe_allow_html=True)
    with col5:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Sleep</div><div class="metric-value">{avg_sleep}m</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("🔥 Energy Expenditure vs. Steps")
        fig_scatter = px.scatter(
            df, x='TotalSteps', y='Calories', color='Calories',
            color_continuous_scale='Viridis', opacity=0.8,
            labels={'TotalSteps': 'Total Daily Steps', 'Calories': 'Calories Burned'}
        )
        fig_scatter.update_layout(template='plotly_dark', height=400, margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_scatter, use_container_width=True)

    with c2:
        st.subheader("⏱️ Daily Activity Allocation")
        activity_melted = df[['VeryActiveMinutes', 'FairlyActiveMinutes', 'LightlyActiveMinutes', 'SedentaryMinutes']].mean().reset_index()
        activity_melted.columns = ['Activity Type', 'Average Minutes']
        
        fig_bar = px.bar(
            activity_melted, x='Average Minutes', y='Activity Type', orientation='h',
            color='Average Minutes', color_continuous_scale='Plasma'
        )
        fig_bar.update_layout(template='plotly_dark', height=400, margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_bar, use_container_width=True)

# ==========================================
# PAGE 2: USER BEHAVIORAL SEGMENTATION
# ==========================================
elif nav == "🎯 User Behavioral Segmentation":
    st.markdown('<p class="main-title">Consumer Segmentation</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Clustering users by activity intensity thresholds and behavioral habits.</p>', unsafe_allow_html=True)

    user_agg = df.groupby('Id').agg({'TotalSteps': 'mean', 'Calories': 'mean', 'SedentaryMinutes': 'mean'}).reset_index()
    
    def classify_user(steps):
        if steps < 5000: return "Sedentary (< 5k)"
        elif steps < 8000: return "Moderately Active (5k-8k)"
        else: return "Highly Active (8k+)"
        
    user_agg['Activity_Tier'] = user_agg['TotalSteps'].apply(classify_user)

    col_a, col_b = st.columns([2, 1])
    with col_a:
        fig_pie = px.pie(
            user_agg, names='Activity_Tier', title="User Distribution by Activity Tier",
            hole=0.5, color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_pie.update_layout(template='plotly_dark', height=450)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col_b:
        st.subheader("Segment Breakdown")
        st.dataframe(user_agg[['Id', 'Activity_Tier']], use_container_width=True, height=380)

# ==========================================
# PAGE 3: DEEP CORRELATION HUB
# ==========================================
elif nav == "📈 Deep Correlation Hub":
    st.markdown('<p class="main-title">Advanced Correlation Hub</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Explore metric relationships with custom regression lines and variable mapping.</p>', unsafe_allow_html=True)

    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    
    col_x, col_y = st.columns(2)
    with col_x: x_axis = st.selectbox("X-Axis Metric:", numeric_cols, index=1)
    with col_y: y_axis = st.selectbox("Y-Axis Metric:", numeric_cols, index=4)

    fig_custom = px.scatter(
        df, x=x_axis, y=y_axis, color='Calories',
        trendline="ols", color_continuous_scale='Turbo'
    )
    fig_custom.update_layout(template='plotly_dark', height=480)
    st.plotly_chart(fig_custom, use_container_width=True)

# ==========================================
# PAGE 4: STRATEGIC INSIGHTS & RECOMMENDATIONS
# ==========================================
elif nav == "💡 Strategic Insights":
    st.markdown('<p class="main-title">Strategic Insights & Recommendations</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Data-driven marketing and product recommendations based on consumer biometric trends.</p>', unsafe_allow_html=True)

    st.markdown("""
        <div class="insight-box">
            <h3>🚨 1. High Sedentary Risk Mitigation</h3>
            <p><b>Finding:</b> Users spend an average of ~990 minutes (~16.5 hours) per day in sedentary behavior.<br>
            <b>Recommendation:</b> Introduce smart app push-notifications and gentle vibration alerts on smart devices encouraging users to stand up or take a 5-minute light walk every hour.</p>
        </div>
        
        <div class="insight-box">
            <h3>🎯 2. Personalized Step-Goal Tiers</h3>
            <p><b>Finding:</b> Many users fall significantly short of the standard 10,000-step daily target.<br>
            <b>Recommendation:</b> Instead of a rigid global target, implement an adaptive milestone algorithm in the app that gradually scales step goals based on the user's historical baseline.</p>
        </div>

        <div class="insight-box">
            <h3>🌙 3. Sleep & Recovery Optimization</h3>
            <p><b>Finding:</b> Users average ~7 hours of sleep with noticeable time spent awake in bed.<br>
            <b>Recommendation:</b> Build sleep coaching insights that correlate late-evening sedentary behavior or low daily activity with restless sleep patterns.</p>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# PAGE 5: SQL ENGINE & SANDBOX
# ==========================================
elif nav == "⚙️ SQL Engine & Sandbox":
    st.markdown('<p class="main-title">Relational SQL Engine</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Direct SQLite database schema inspection and live query execution environment.</p>', unsafe_allow_html=True)

    conn = sqlite3.connect('fitbit_data.db')
    
    tab_sql1, tab_sql2 = st.tabs(["Master Table Schema", "Live SQL Query Sandbox"])

    with tab_sql1:
        st.dataframe(master_df.head(100), use_container_width=True)
        
        csv = master_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Master CSV Dataset",
            data=csv,
            file_name='master_merged_fitbit_data.csv',
            mime='text/csv',
        )

    with tab_sql2:
        default_query = "SELECT Id, COUNT(*) as TotalLogs, ROUND(AVG(TotalSteps), 0) as MeanSteps FROM master_data GROUP BY Id ORDER BY MeanSteps DESC LIMIT 10;"
        query_input = st.text_area("SQL Query Editor:", value=default_query, height=120)
        
        if st.button("Run SQL Query"):
            try:
                res_df = pd.read_sql(query_input, conn)
                st.success("Query executed successfully!")
                st.dataframe(res_df, use_container_width=True)
            except Exception as e:
                st.error(f"Execution Error: {e}")
                
    conn.close()
