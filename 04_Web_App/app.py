import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go # <--- The Pro Graphing Library
import os

# 1. PAGE SETUP
st.set_page_config(page_title="Hanwha Ocean Strategy", layout="wide")

# 2. DATABASE CONNECTION
def get_data_from_sql():
    # Robust Path Finding
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, "..", "05_Hanwha_Project", "corporate_data.db")
    db_path = os.path.abspath(db_path)
    
    if not os.path.exists(db_path):
        st.error(f"❌ DATABASE NOT FOUND at: {db_path}")
        st.stop()

    conn = sqlite3.connect(db_path)
    try:
        query = "SELECT * FROM financial_metrics ORDER BY year ASC"
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"❌ SQL ERROR: {e}")
        st.stop()
    finally:
        conn.close()

# 3. LOAD DATA
df = get_data_from_sql()

# 4. DASHBOARD HEADER
st.title("🚢 Hanwha Ocean: Strategic Turnaround")
st.markdown("### Financial Performance & 2025 Simulator")

# 5. KPI METRICS
latest = df.iloc[-1] # 2024
prev = df.iloc[-2]   # 2023

col1, col2, col3 = st.columns(3)
col1.metric("2024 Revenue", f"{latest['revenue_krw']/1e12:.1f}T KRW", f"{(latest['revenue_krw'] - prev['revenue_krw'])/1e12:.1f}T Growth")
col2.metric("Operating Profit", f"{latest['op_profit_krw']/1e9:.0f}B KRW", "Turnaround Success")
col3.metric("Profit Margin", f"{latest['op_margin_percent']:.1f}%", f"{latest['op_margin_percent'] - prev['op_margin_percent']:.1f}pts vs '23")

st.divider()

# 6. VISUALIZATION (PLOTLY COMBO CHART)
col_chart, col_sim = st.columns([2, 1])

with col_chart:
    st.subheader("📉 Financial History (2018-2024)")
    
    # Create the Interactive Plot
    fig = go.Figure()

    # Trace 1: Revenue Bars (Left Axis)
    fig.add_trace(go.Bar(
        x=df['year'],
        y=df['revenue_krw'],
        name='Revenue (KRW)',
        marker_color='lightgray',
        yaxis='y'
    ))

    # Trace 2: Margin Line (Right Axis)
    fig.add_trace(go.Scatter(
        x=df['year'],
        y=df['op_margin_percent'],
        name='Op Margin (%)',
        mode='lines+markers',
        marker=dict(size=10, color='#0052cc'),
        line=dict(width=3, color='#0052cc'),
        yaxis='y2'
    ))

    # Layout: Dual Axis Magic
    fig.update_layout(
        title="",
        xaxis=dict(title='Year'),
        yaxis=dict(
            title='Revenue (KRW)',
            showgrid=False
        ),
        yaxis2=dict(
            title='Operating Margin (%)',
            overlaying='y',
            side='right',
            showgrid=False,
            range=[-40, 10] # Fix the range so it looks clean
        ),
        legend=dict(x=0.01, y=0.99),
        template="plotly_white",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

# 7. STRATEGY SIMULATOR
with col_sim:
    st.subheader("🛠️ Strategy Simulator")
    st.info("Scenario: Can we reach 5% Margin in 2025?")
    
    # Sliders
    growth_input = st.slider("Revenue Growth (%)", -10, 30, 10)
    margin_input = st.slider("Target Margin (%)", -5.0, 10.0, 3.5)
    
    # Math
    projected_rev = latest['revenue_krw'] * (1 + growth_input/100)
    projected_profit = projected_rev * (margin_input/100)
    
    st.markdown("---")
    
    # Dynamic Result Card
    st.markdown(f"**2025 Projected Financials**")
    
    # Revenue Display
    st.metric("Proj. Revenue", f"{projected_rev/1e12:.1f}T KRW")
    
    # Profit Display with Logic
    if projected_profit > 0:
        st.success(f"PROFIT: {projected_profit/1e9:.0f} Billion KRW")
    else:
        st.error(f"LOSS: {projected_profit/1e9:.0f} Billion KRW")