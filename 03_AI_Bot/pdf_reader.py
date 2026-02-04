from pypdf import PdfReader

def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        # Loop through every page and grab the text
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

if __name__ == "__main__":
    # Test it immediately
    print("--- EXTRACTING TEXT ---")
    content = extract_text_from_pdf("context.pdf")
    # Print the first 500 characters to check
    print(content[:500])
    print("\n--- SUCCESS ---")