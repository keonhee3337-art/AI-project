import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Samsung Strategy", layout="wide")

def get_samsung_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, "..", "05_Hanwha_Project", "corporate_data.db")
    
    conn = sqlite3.connect(os.path.abspath(db_path))
    # Query SPECIFICALLY for Samsung Electronics
    query = "SELECT * FROM financial_metrics WHERE company_name='Samsung Electronics' ORDER BY year ASC"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

df = get_samsung_data()

if df.empty:
    st.error("No Samsung data found. Did you run 'store_to_sql.py'?")
    st.stop()

# DASHBOARD
st.title("📱 Samsung Electronics: Financial Analysis")
st.markdown("### 2025 Strategic Outlook")

# METRICS
latest = df.iloc[-1]
prev = df.iloc[-2]

col1, col2, col3 = st.columns(3)
col1.metric("Revenue", f"{latest['revenue_krw']/1e12:.1f}T KRW", f"{(latest['revenue_krw'] - prev['revenue_krw'])/1e12:.1f}T")
col2.metric("Op Profit", f"{latest['op_profit_krw']/1e12:.1f}T KRW", f"{(latest['op_profit_krw'] - prev['op_profit_krw'])/1e12:.1f}T")
col3.metric("Margin", f"{latest['op_margin_percent']:.1f}%", f"{latest['op_margin_percent'] - prev['op_margin_percent']:.1f} pts")

st.divider()

# CHART
fig = go.Figure()
fig.add_trace(go.Bar(x=df['year'], y=df['revenue_krw'], name='Revenue', marker_color='#1428A0')) # Samsung Blue
fig.add_trace(go.Scatter(x=df['year'], y=df['op_margin_percent'], name='Margin %', yaxis='y2', line=dict(color='red', width=3)))

fig.update_layout(
    title="Samsung Revenue vs Margin Trend",
    yaxis=dict(title='Revenue (KRW)', showgrid=False),
    yaxis2=dict(title='Margin (%)', overlaying='y', side='right', showgrid=False),
    height=500
)
st.plotly_chart(fig, use_container_width=True)