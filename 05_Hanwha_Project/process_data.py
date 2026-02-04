import pandas as pd
import os

file_path = "fsdata/hanwha_financials.xlsx"

def clean_financials():
    print("--- 1. LOADING DATA (With Header Fix) ---")
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    # STEP A: Read the Dates (Row 0)
    # We read just the top few rows to figure out the structure
    df_raw = pd.read_excel(file_path, sheet_name="Data_is", header=None)
    
    # Row 0 contains dates like '20230101-20231231'
    # Row 1 contains headers like 'concept_id'
    
    # Let's map column INDICES to YEARS
    year_map = {}
    for col_idx in df_raw.columns:
        val = str(df_raw.iloc[0, col_idx]) # Value in Row 0
        if "20" in val and "-" in val:     # It looks like a date range
            year = val[:4]                 # Extract '2023'
            year_map[col_idx] = year
    
    print(f"Detected Years: {list(year_map.values())}")

    # STEP B: Read the Data (Using Row 1 as header)
    df = pd.read_excel(file_path, sheet_name="Data_is", header=1)
    
    clean_data = []
    
    # Find the rows we need
    # We look for 'Revenue' and 'Operating Income'
    # DART uses specific codes. We check if the code exists in the 'concept_id' column.
    
    # Filter safely
    rev_row = df[df['concept_id'] == 'ifrs-full_Revenue']
    prof_row = df[df['concept_id'] == 'dart_OperatingIncomeLoss']
    
    if rev_row.empty or prof_row.empty:
        print("CRITICAL: Could not find Revenue/Profit rows. Checking alternative codes...")
        # Fallback for some companies
        prof_row = df[df['concept_id'] == 'ifrs-full_ProfitLossFromOperatingActivities']

    # STEP C: Extract Data using the Year Map
    for col_idx, year in year_map.items():
        # We need the column NAME that corresponds to this index
        # Since we reloaded with header=1, the column names are from Row 1
        col_name = df.columns[col_idx]
        
        try:
            rev = rev_row[col_name].values[0]
            prof = prof_row[col_name].values[0]
            
            clean_data.append({
                "Year": year,
                "Revenue": rev,
                "Op_Profit": prof
            })
        except Exception as e:
            pass # Skip empty columns

    # Finalize
    df_clean = pd.DataFrame(clean_data).sort_values("Year")
    
    # Ratios
    df_clean['Op_Margin_Percent'] = (df_clean['Op_Profit'] / df_clean['Revenue']) * 100
    
    print("\n--- 2. FINAL DATA ---")
    print(df_clean[['Year', 'Revenue', 'Op_Profit', 'Op_Margin_Percent']])
    
    df_clean.to_csv("05_Hanwha_Project/hanwha_clean.csv", index=False)
    print("\nSUCCESS: Saved to '05_Hanwha_Project/hanwha_clean.csv'")

if __name__ == "__main__":
    clean_financials()