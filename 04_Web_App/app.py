import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
import os
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly

# PAGE SETUP
st.set_page_config(page_title="Samsung Strategy Engine", layout="wide")
st.title("📱 Samsung Electronics: AI Strategy Deck")

# 1. DATABASE CONNECTION (For Financials)
def get_samsung_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, "..", "05_Hanwha_Project", "corporate_data.db")
    conn = sqlite3.connect(os.path.abspath(db_path))
    query = "SELECT * FROM financial_metrics WHERE company_name='Samsung Electronics' ORDER BY year ASC"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# 2. CREATE TABS
tab1, tab2 = st.tabs(["📊 Financial Fundamentals", "🔮 Stock Price AI Forecast"])

# --- TAB 1: FINANCIALS (SQL DATA) ---
with tab1:
    df_fin = get_samsung_data()
    if not df_fin.empty:
        # Metrics
        latest = df_fin.iloc[-1]
        prev = df_fin.iloc[-2]
        
        c1, c2, c3 = st.columns(3)
        c1.metric("2024 Revenue", f"{latest['revenue_krw']/1e12:.1f}T KRW", f"{(latest['revenue_krw'] - prev['revenue_krw'])/1e12:.1f}T")
        c2.metric("Op Profit", f"{latest['op_profit_krw']/1e12:.1f}T KRW", f"Turnaround")
        c3.metric("Op Margin", f"{latest['op_margin_percent']:.1f}%", f"{latest['op_margin_percent'] - prev['op_margin_percent']:.1f} pts")

        # Chart
        st.subheader("Financial Recovery Trend")
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_fin['year'], y=df_fin['revenue_krw'], name='Revenue', marker_color='#1428A0'))
        fig.add_trace(go.Scatter(x=df_fin['year'], y=df_fin['op_margin_percent'], name='Margin %', yaxis='y2', line=dict(color='red', width=3)))
        fig.update_layout(
            yaxis=dict(title='Revenue', showgrid=False),
            yaxis2=dict(title='Margin %', overlaying='y', side='right', showgrid=False),
            height=400,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Run 'store_to_sql.py' first!")

# --- TAB 2: AI FORECAST (PROPHET) ---
with tab2:
    st.subheader("🔮 AI Price Prediction (Prophet Model)")
    st.markdown("The AI model analyzes 5 years of daily trading data to forecast the **Next 365 Days**.")

    if st.button("🚀 Run AI Simulation"):
        with st.spinner("Training AI Model on Real-Time Data..."):
            # A. Fetch Data
            stock = yf.Ticker("005930.KS")
            hist = stock.history(period="5y").reset_index()
            
            # B. Prepare for Prophet
            df_prophet = hist[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})
            df_prophet['ds'] = df_prophet['ds'].dt.tz_localize(None)

            # C. Train Model
            m = Prophet(daily_seasonality=True)
            m.fit(df_prophet)
            
            # D. Predict
            future = m.make_future_dataframe(periods=365)
            forecast = m.predict(future)

            # E. Visualize (Interactive)
            st.success("Prediction Complete!")
            
            # Use Prophet's built-in Plotly support for interactivity
            fig_ai = plot_plotly(m, forecast)
            fig_ai.update_layout(
                title="Samsung Electronics: 1-Year Price Target",
                yaxis_title="Stock Price (KRW)",
                xaxis_title="Date",
                height=600
            )
            st.plotly_chart(fig_ai, use_container_width=True)

            # F. Insight Card
            pred = forecast.iloc[-1]
            st.info(f"💡 **AI Insight:** The model predicts a price of **{pred['yhat']:.0f} KRW** exactly one year from now (Best Case: {pred['yhat_upper']:.0f} KRW).")