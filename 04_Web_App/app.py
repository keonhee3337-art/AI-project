import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
import os
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from openai import OpenAI

# PAGE SETUP
st.set_page_config(page_title="Samsung Strategy Engine", layout="wide")
st.title("📱 Samsung Electronics: AI Strategy Deck")

# 1. DATABASE CONNECTION
def get_samsung_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, "..", "05_Hanwha_Project", "corporate_data.db")
    conn = sqlite3.connect(os.path.abspath(db_path))
    query = "SELECT * FROM financial_metrics WHERE company_name='Samsung Electronics' ORDER BY year ASC"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# 2. AI CLIENT SETUP (Robust Error Handling)
api_key = st.secrets.get("OPENAI_API_KEY")
client = None
if api_key:
    client = OpenAI(api_key=api_key)

# 3. CREATE TABS
tab1, tab2, tab3 = st.tabs(["📊 Financials", "🔮 Stock Forecast", "🤖 AI Consultant"])

# --- TAB 1: FINANCIALS ---
with tab1:
    df_fin = get_samsung_data()
    if not df_fin.empty:
        latest = df_fin.iloc[-1]
        prev = df_fin.iloc[-2]
        
        c1, c2, c3 = st.columns(3)
        c1.metric("2024 Revenue", f"{latest['revenue_krw']/1e12:.1f}T KRW", f"{(latest['revenue_krw'] - prev['revenue_krw'])/1e12:.1f}T")
        c2.metric("Op Profit", f"{latest['op_profit_krw']/1e12:.1f}T KRW", "Turnaround")
        c3.metric("Margin", f"{latest['op_margin_percent']:.1f}%", f"{latest['op_margin_percent'] - prev['op_margin_percent']:.1f} pts")

        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_fin['year'], y=df_fin['revenue_krw'], name='Revenue', marker_color='#1428A0'))
        fig.add_trace(go.Scatter(x=df_fin['year'], y=df_fin['op_margin_percent'], name='Margin %', yaxis='y2', line=dict(color='red', width=3)))
        fig.update_layout(yaxis=dict(showgrid=False), yaxis2=dict(overlaying='y', side='right', showgrid=False), height=400)
        st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: STOCK FORECAST ---
with tab2:
    st.subheader("🔮 Prophet AI Forecast")
    if st.button("Run Simulation"):
        with st.spinner("Training AI..."):
            stock = yf.Ticker("005930.KS")
            hist = stock.history(period="5y").reset_index()
            df_prophet = hist[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})
            df_prophet['ds'] = df_prophet['ds'].dt.tz_localize(None)
            
            m = Prophet(daily_seasonality=True)
            m.fit(df_prophet)
            future = m.make_future_dataframe(periods=365)
            forecast = m.predict(future)
            
            fig_ai = plot_plotly(m, forecast)
            st.plotly_chart(fig_ai, use_container_width=True)

# --- TAB 3: AI CONSULTANT (RAG SYSTEM) ---
with tab3:
    st.subheader("🤖 Ask the Strategy AI")
    st.caption("This AI has access to the database above. Ask about margins, trends, or strategy.")

    if not client:
        st.error("🔑 API Key missing. Please set OPENAI_API_KEY in secrets.toml")
        st.stop()

    # Chat Interface
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Hello! I have analyzed Samsung's financial data. What would you like to know?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ex: Why did profit drop in 2023?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # RAG LOGIC: Feed the dataframe to the AI
        context_data = df_fin.to_string()
        
        system_prompt = f"""
        You are a Senior Strategic Consultant for Samsung Electronics.
        You have access to the following financial data (KRW):
        {context_data}
        
        Rules:
        1. Answer based strictly on the data provided.
        2. Be professional, concise, and insightful.
        3. If the user asks about the future, use the trends from the data to give an educated opinion.
        4. Revenue is in Won (KRW). 1T = 1 Trillion.
        """

        response = client.chat.completions.create(
            model="gpt-4o", # Or gpt-3.5-turbo if you want to save money
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        
        ai_msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": ai_msg})
        st.chat_message("assistant").write(ai_msg)