import dart_fss as dart
import pandas as pd
import os

# --- PASTE YOUR KEY HERE ---
api_key = "aa387998d4b169f33652535b58dfab311addc52d"  
dart.set_api_key(api_key=api_key)

def get_hanwha_data():
    print("--- 1. CHECKING CORPORATE LIST ---")
    # This caches the list so it doesn't download every time (saves 2 mins)
    corp_list = dart.get_corp_list()
    
    print("--- 2. SEARCHING FOR HANWHA OCEAN ---")
    hanwha = corp_list.find_by_corp_name('한화오션', exactly=True)[0]
    print(f"Target Found: {hanwha}")

    print("--- 3. EXTRACTING FINANCIALS (Since 2021) ---")
    # FIX: Changed 'bgn_year' to 'bgn_de' (Begin Date: YYYYMMDD)
    try:
        fs = hanwha.extract_fs(bgn_de='20210101') 
        
        # Save to Excel
        fs.save("hanwha_financials.xlsx")
        print(f"\nSUCCESS: Data saved to folder 'fsdata/hanwha_financials.xlsx'")
        
        print(f"\nSUCCESS: Financials downloaded to '{output_file}'")
        print("ACTION: Open this Excel file to see the raw Balance Sheet.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_hanwha_data()