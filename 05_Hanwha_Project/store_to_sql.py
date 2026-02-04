import sqlite3
import pandas as pd
import os

# 1. SETUP PATHS
csv_path = "05_Hanwha_Project/hanwha_clean.csv" # (Data is Samsung, but filename is same)
db_path = "05_Hanwha_Project/corporate_data.db"

def init_db():
    print("--- 1. INITIALIZING DATA WAREHOUSE ---")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table with 'Samsung Electronics' as the default name
    create_table_query = """
    CREATE TABLE IF NOT EXISTS financial_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT DEFAULT 'Samsung Electronics', 
        year INTEGER,
        revenue_krw REAL,
        op_profit_krw REAL,
        op_margin_percent REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    cursor.execute(create_table_query)
    print("✅ SQL Schema Ready.")
    
    print("\n--- 2. MIGRATING SAMSUNG DATA ---")
    if not os.path.exists(csv_path):
        print("Error: CSV not found.")
        return

    df = pd.read_csv(csv_path)
    
    # Clear old Samsung data (if any) to prevent duplicates
    # Note: We are NOT deleting Hanwha data; both can exist in the DB!
    cursor.execute("DELETE FROM financial_metrics WHERE company_name = 'Samsung Electronics'")
    
    for index, row in df.iterrows():
        insert_query = """
        INSERT INTO financial_metrics (company_name, year, revenue_krw, op_profit_krw, op_margin_percent)
        VALUES (?, ?, ?, ?, ?)
        """
        # Explicitly insert 'Samsung Electronics'
        data_tuple = ('Samsung Electronics', row['Year'], row['Revenue'], row['Op_Profit'], row['Op_Margin_Percent'])
        cursor.execute(insert_query, data_tuple)
        print(f"   -> Ingested Samsung Record: {int(row['Year'])}")

    conn.commit()
    conn.close()
    print("\n✅ SUCCESS: Samsung Data stored in 'corporate_data.db'")

if __name__ == "__main__":
    init_db()