import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import os
from openai import OpenAI
from pypdf import PdfReader

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="MBB AI Consultant", layout="wide")

# Handle Secrets (Local vs Cloud)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except:
        pass

if api_key:
    client = OpenAI(api_key=api_key)

# --- 2. HELPER FUNCTIONS ---
def get_pdf_text(uploaded_file):
    text = ""
    try:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            text += page.extract_text()
    except Exception as e:
        return f"Error: {e}"
    return text

def get_chart_data():
    # Connect to the database file
    # Note: This assumes club_data.db is uploaded to your GitHub!
    try:
        conn = sqlite3.connect('club_data.db')
        query = """
        SELECT 
            strftime('%Y-%m', e.date) as month, 
            COUNT(*) as monthly_volume
        FROM attendance a
        JOIN events e ON a.event_id = e.event_id
        GROUP BY month
        ORDER BY month
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        df['cumulative_volume'] = df['monthly_volume'].cumsum()
        return df
    except Exception as e:
        st.error(f"Database Error: {e}")
        return pd.DataFrame()

# --- 3. THE UI ---
st.title("🤖 MBB Strategy & Analytics Suite")
st.markdown("### Powered by OpenAI & Python SQL Engine")

# TABS: The "App Store" feel
tab1, tab2 = st.tabs(["📄 AI Document Analyst", "📈 Growth Strategy Dashboard"])

# --- TAB 1: RAG BOT (Your existing code) ---
with tab1:
    col1, col2 = st.columns([1, 2])
    with col1:
        uploaded_file = st.file_uploader("Upload 10-K / PDF", type="pdf")
        if uploaded_file:
            st.success("File Processed.")
            if 'pdf_text' not in st.session_state:
                with st.spinner("Reading..."):
                    st.session_state.pdf_text = get_pdf_text(uploaded_file)
    
    with col2:
        user_query = st.text_input("Ask a strategic question:")
        if st.button("Analyze Document"):
            if not uploaded_file:
                st.warning("Upload a PDF first.")
            elif not api_key:
                st.error("API Key missing.")
            else:
                with st.spinner("Consulting Partners..."):
                    try:
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": f"Answer based on: {st.session_state.pdf_text[:40000]}"},
                                {"role": "user", "content": user_query}
                            ]
                        )
                        st.write(response.choices[0].message.content)
                    except Exception as e:
                        st.error(f"Error: {e}")

# --- TAB 2: ANALYTICS (The New Feature) ---
with tab2:
    st.header("Operational Scale Analysis")
    st.markdown("Real-time visualization of engagement metrics from SQL Database.")
    
    if st.button("Generate Growth Chart"):
        df = get_chart_data()
        if not df.empty:
            # Draw the Matplotlib Chart
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(df['month'], df['cumulative_volume'], marker='o', linestyle='-', color='#0052cc', linewidth=2)
            ax.fill_between(df['month'], df['cumulative_volume'], color='#0052cc', alpha=0.1)
            ax.set_title("Cumulative Operational Volume (Sessions)", fontweight='bold')
            ax.set_ylabel("Total Sessions")
            ax.grid(True, linestyle='--', alpha=0.5)
            
            # Display in Streamlit
            st.pyplot(fig)
            
            # Show the raw data below
            st.markdown("#### Raw Data Feed")
            st.dataframe(df)
        else:
            st.warning("No data found. Ensure 'club_data.db' is in the repository.")