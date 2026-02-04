import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
from pdf_reader import extract_text_from_pdf 

# 1. Setup
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def start_research_bot():
    print("--- 1. READING PDF ---")
    # This calls the tool you built 5 minutes ago
    # Note: We assume 'context.pdf' is in the main folder (one level up)
    pdf_path = os.path.join(os.path.dirname(__file__), "..", "context.pdf")
    pdf_text = extract_text_from_pdf(pdf_path)
    
    # Safety Check
    if len(pdf_text) < 10:
        print("ERROR: PDF seems empty. Check the file.")
        return
    
    print(f"--- 2. MEMORIZED {len(pdf_text)} CHARACTERS ---")
    print("--- 3. READY. ASK QUESTIONS ABOUT THE DOCUMENT. ---")
    print("(Type 'exit' to quit)\n")

    while True:
        user_query = input("Your Question > ")
        if user_query.lower() == 'exit':
            break

        # 4. The RAG "Injection"
        # We put the document text INSIDE the system prompt.
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": f"""
                    You are a High-Level Analyst. 
                    Answer the user's question ONLY based on the following document text.
                    If the answer is not in the text, say "I cannot find that in the document."
                    
                    DOCUMENT TEXT:
                    {pdf_text[:30000]}  # Safety Cap: We only read the first 30k characters to save money
                    """
                },
                {
                    "role": "user", 
                    "content": user_query
                }
            ]
        )
        
        print("\n--- ANALYST REPORT ---")
        print(response.choices[0].message.content)
        print("-" * 30 + "\n")

if __name__ == "__main__":
    start_research_bot()