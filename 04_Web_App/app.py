import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. PAGE SETUP
st.set_page_config(page_title="Hanwha Ocean Strategy", layout="wide")

# 2. DATABASE CONNECTION (Path Fixed for Subfolder Deployment)
def get_data_from_sql():
    # Get the folder where THIS file (04_Web_App/app.py) lives
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Go UP one level to root, then DOWN into 05_Hanwha_Project
    # '..' means "Go up to the parent folder"
    db_path = os.path.join(current_dir, "..", "05_Hanwha_Project", "corporate_data.db")
    
    # Clean up the path (removes the '..' to make it a real path)
    db_path = os.path.abspath(db_path)
    
    if not os.path.exists(db_path):
        st.error(f"❌ DATABASE NOT FOUND at: {db_path}")
        st.write("Current working directory:", os.getcwd())
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
st.title("🚢 Hanwha Ocean: Financial Turnaround Analysis")
st.markdown("### Strategic Dashboard (Built with SQL & Python)")

# 5. KPI METRICS
latest = df.iloc[-1] # 2024
prev = df.iloc[-2]   # 2023

col1, col2, col3 = st.columns(3)
col1.metric("2024 Revenue", f"{latest['revenue_krw']/1e12:.1f}T KRW", f"{(latest['revenue_krw'] - prev['revenue_krw'])/1e12:.1f}T Growth")
col2.metric("Operating Profit", f"{latest['op_profit_krw']/1e9:.0f}B KRW", "Turnaround Success")
col3.metric("Profit Margin", f"{latest['op_margin_percent']:.1f}%", f"{latest['op_margin_percent'] - prev['op_margin_percent']:.1f}% vs Last Year")

st.divider()

# 6. VISUALIZATION
col_chart, col_sim = st.columns([2, 1])

with col_chart:
    st.subheader("📉 The Recovery Trend (7-Year History)")
    fig, ax1 = plt.subplots(figsize=(10, 5))
    
    sns.barplot(data=df, x='year', y='revenue_krw', ax=ax1, color='#e0e0e0', alpha=0.6)
    ax1.set_ylabel("Revenue (KRW)", color='gray')
    ax1.set_ylim(0, max(df['revenue_krw'])*1.3)
    
    ax2 = ax1.twinx()
    sns.lineplot(data=df, x='year', y='op_margin_percent', ax=ax2, color='#0052cc', marker='o', linewidth=3)
    ax2.set_ylabel("Operating Margin (%)", color='#0052cc')
    ax2.axhline(0, color='black', linewidth=1, linestyle='--')
    
    st.pyplot(fig)

with col_sim:
    st.subheader("🛠️ Strategy Simulator")
    st.write("Adjust 2025 targets:")
    growth_input = st.slider("Revenue Growth Target (%)", -10, 30, 10)
    margin_input = st.slider("Target Margin (%)", -5.0, 10.0, 2.5)
    
    projected_rev = latest['revenue_krw'] * (1 + growth_input/100)
    projected_profit = projected_rev * (margin_input/100)
    
    st.markdown("---")
    st.markdown(f"**2025 Projected Profit:**")
    if projected_profit > 0:
        st.success(f"{projected_profit/1e9:.0f} Billion KRW")
    else:
        st.error(f"{projected_profit/1e9:.0f} Billion KRW")