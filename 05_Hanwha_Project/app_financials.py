import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# 1. PAGE SETUP
st.set_page_config(page_title="Hanwha Ocean Strategy", layout="wide")

# 2. SQL CONNECTION FUNCTION
def get_data_from_sql():
    # Connect to the database we created in the previous step
    conn = sqlite3.connect("05_Hanwha_Project/corporate_data.db")
    # Query: Get everything, sorted by year
    query = "SELECT * FROM financial_metrics ORDER BY year ASC"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# 3. LOAD DATA
try:
    df = get_data_from_sql()
except Exception as e:
    st.error(f"Error connecting to Database: {e}")
    st.stop()

# 4. DASHBOARD HEADER
st.title("🚢 Hanwha Ocean: Financial Turnaround Analysis")
st.markdown("### Strategic Dashboard (Built with SQL & Python)")

# 5. KPI METRICS (The Top Bar)
# Compare 2024 (Latest) vs 2023 (Previous)
latest = df.iloc[-1] # 2024
prev = df.iloc[-2]   # 2023

col1, col2, col3 = st.columns(3)
col1.metric("2024 Revenue", f"{latest['revenue_krw']/1e12:.1f}T KRW", f"{(latest['revenue_krw'] - prev['revenue_krw'])/1e12:.1f}T Growth")
col2.metric("Operating Profit", f"{latest['op_profit_krw']/1e9:.0f}B KRW", "Turnaround Success")
col3.metric("Profit Margin", f"{latest['op_margin_percent']:.1f}%", f"{latest['op_margin_percent'] - prev['op_margin_percent']:.1f}% vs Last Year")

st.divider()

# 6. VISUALIZATION & STRATEGY SIMULATOR
col_chart, col_sim = st.columns([2, 1])

with col_chart:
    st.subheader("📉 The Recovery Trend (7-Year History)")
    
    # Create a dual-axis chart
    fig, ax1 = plt.subplots(figsize=(10, 5))
    
    # Bar Chart: Revenue
    sns.barplot(data=df, x='year', y='revenue_krw', ax=ax1, color='#e0e0e0', alpha=0.6)
    ax1.set_ylabel("Revenue (KRW)", color='gray')
    ax1.set_ylim(0, max(df['revenue_krw'])*1.3)
    
    # Line Chart: Profit Margin (The most important metric)
    ax2 = ax1.twinx()
    sns.lineplot(data=df, x='year', y='op_margin_percent', ax=ax2, color='#0052cc', marker='o', linewidth=3)
    ax2.set_ylabel("Operating Margin (%)", color='#0052cc')
    ax2.axhline(0, color='black', linewidth=1, linestyle='--') # The "Break-even" line
    
    st.pyplot(fig)

with col_sim:
    st.subheader("🛠️ Strategy Simulator")
    st.write("Adjust 2025 targets to see profit impact:")
    
    # Interactive Sliders
    growth_input = st.slider("Revenue Growth Target (%)", -10, 30, 10)
    margin_input = st.slider("Target Margin (%)", -5.0, 10.0, 2.5)
    
    # Calculate Projection
    projected_rev = latest['revenue_krw'] * (1 + growth_input/100)
    projected_profit = projected_rev * (margin_input/100)
    
    st.markdown("---")
    st.markdown(f"**2025 Projected Profit:**")
    
    # Dynamic Color Logic
    if projected_profit > 0:
        st.success(f"{projected_profit/1e9:.0f} Billion KRW")
    else:
        st.error(f"{projected_profit/1e9:.0f} Billion KRW")