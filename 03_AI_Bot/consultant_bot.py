import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load the Secret Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
# 2. Initialize the Client
client = OpenAI(api_key=api_key)

def critique_framework(user_input):
    print("\nThinking... (Connecting to Seoul Office)")
    
    # 3. The "Brain" Logic
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # We use Mini to save money (cheaper/faster)
        messages=[
            {
                "role": "system", 
                "content": """
                You are a Senior Partner at McKinsey & Company. 
                You are reviewing a candidate's case structure. 
                Your feedback is direct, critical, and MECE (Mutually Exclusive, Collectively Exhaustive).
                
                Rules:
                1. If the structure is generic, reject it brutally.
                2. If the structure is not MECE, point out the overlap immediately.
                3. Use corporate professional tone.
                4. Limit feedback to 3 bullet points.
                """
            },
            {
                "role": "user", 
                "content": user_input
            }
        ],
        temperature=0.7
    )
    
    # 4. Extract the Answer
    feedback = response.choices[0].message.content
    return feedback

# 5. The Interface
if __name__ == "__main__":
    print("=== MBB CASE CRITIQUE BOT (ALPHA) ===")
    print("Enter your case framework below (e.g., 'I would look at Revenue and Cost').")
    print("Type 'exit' to quit.\n")

    while True:
        user_case = input("Your Framework > ")
        if user_case.lower() == 'exit':
            break
        
        analysis = critique_framework(user_case)
        print("\n--- PARTNER FEEDBACK ---")
        print(analysis)
        print("-" * 30 + "\n")