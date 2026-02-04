import streamlit as st
import os
from openai import OpenAI
from pypdf import PdfReader

# --- SECURITY & CONFIGURATION ---
# We wrap this in a try-except block.
# On your laptop, it loads .env.
# On the Cloud, it skips this because .env doesn't exist there.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # This means we are on the cloud, so we pass
    pass

# Try to get key from Environment (Laptop) OR Streamlit Secrets (Cloud)
api_key = os.getenv("OPENAI_API_KEY")

# If os.getenv failed, try Streamlit's native secret manager
if not api_key:
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except:
        pass

# Initialize Client only if key exists
client = None
if api_key:
    client = OpenAI(api_key=api_key)
# -------------------------------

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
        if 'pdf_text' not in st.session_state:
            with st.spinner("Reading document..."):
                st.session_state.pdf_text = get_pdf_text(uploaded_file)
                st.info(f"Memorized {len(st.session_state.pdf_text)} characters.")

# 5. The Chat Interface
user_query = st.text_input("Ask a question about the document:")

if st.button("Analyze Document"):
    if not uploaded_file:
        st.warning("⚠️ Please upload a PDF in the sidebar first.")
    elif not api_key:
        st.error("🚨 CRITICAL ERROR: API Key is missing. Please configure secrets on Streamlit Cloud.")
    else:
        with st.spinner("Consulting the Partners..."):
            try:
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
                answer = response.choices[0].message.content
                st.markdown("### 💡 Partner Insight")
                st.write(answer)
            except Exception as e:
                st.error(f"API Error: {e}")