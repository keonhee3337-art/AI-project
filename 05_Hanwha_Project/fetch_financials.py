import dart_fss as dart
import pandas as pd
import os

# --- API KEY ---
api_key = "aa387998d4b169f33652535b58dfab311addc52d" 
dart.set_api_key(api_key=api_key)

def get_financials():
    print("--- 1. CHECKING CORPORATE LIST ---")
    corp_list = dart.get_corp_list()
    
    print("--- 2. FETCHING SAMSUNG ELECTRONICS DATA ---")
    # HERE IS THE CODE YOU ASKED FOR:
    # We use 'exactly=True' because we now know the name is definitely '삼성전자'
    target_corp = corp_list.find_by_corp_name('삼성전자', exactly=True)[0]
    
    print(f"Target Found: {target_corp.corp_name} (Code: {target_corp.stock_code})")

    print("--- 3. DOWNLOADING FINANCIAL STATEMENTS (Since 2021) ---")
    try:
        # Download data starting from Jan 1, 2021
        fs = target_corp.extract_fs(bgn_de='20210101') 
        
        # IMPORTANT: We save to the SAME filename as before ('hanwha_financials.xlsx')
        # This is a trick so we don't have to edit your processing scripts.
        output_file = "hanwha_financials.xlsx" 
        fs.save(output_file)
        
        print(f"\nSUCCESS: Data saved to 'fsdata/{output_file}'")
        print("ACTION: Now run 'process_data.py' to clean this new Samsung data.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_financials()