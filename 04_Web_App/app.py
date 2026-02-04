import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader

# 1. Load Secrets
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# 2. Helper Function: Read PDF
def get_pdf_text(uploaded_file):
    text = ""
    try:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            text += page.extract_text()
    except Exception as e:
        return f"Error: {e}"
    return text

# 3. The Web Layout
st.set_page_config(page_title="AI Strategy Consultant", layout="wide")

st.title("🤖 MBB Strategy Consultant Bot")
st.markdown("### Upload a 10-K or Case Study, and I will analyze it.")

# 4. The Sidebar (Upload)
with st.sidebar:
    st.header("📂 Document Center")
    uploaded_file = st.file_uploader("Upload your PDF here", type="pdf")
    
    if uploaded_file:
        st.success("File Loaded Successfully!")
        # Extract text immediately
        if 'pdf_text' not in st.session_state:
            with st.spinner("Reading document..."):
                st.session_state.pdf_text = get_pdf_text(uploaded_file)
                st.info(f"Memorized {len(st.session_state.pdf_text)} characters.")

# 5. The Chat Interface
user_query = st.text_input("Ask a question about the document:")

# FIX: Single Button Logic
if st.button("Analyze Document"):
    if not uploaded_file:
        st.warning("⚠️ Please upload a PDF in the sidebar first.")
    elif not api_key:
        st.error("ERROR: No API Key found. Check your .env file!")
    else:
        with st.spinner("Consulting the Partners..."):
            # The Brain
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system", 
                        "content": f"""
                        You are a Senior Consultant. Answer ONLY based on the document below.
                        If the answer is missing, say "Data not found in source."
                        
                        DOCUMENT CONTEXT:
                        {st.session_state.pdf_text[:40000]} 
                        """
                    },
                    {
                        "role": "user", 
                        "content": user_query
                    }
                ]
            )
            
            # The Output
            answer = response.choices[0].message.content
            st.markdown("### 💡 Partner Insight")
            st.write(answer)