import sqlite3
import pandas as pd
import os

# 1. SETUP PATHS
csv_path = "05_Hanwha_Project/hanwha_clean.csv"
db_path = "05_Hanwha_Project/corporate_data.db"

def init_db():
    print("--- 1. INITIALIZING DATA WAREHOUSE ---")
    
    # Connect to SQLite (Creates the file if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # SQL QUERY: Design the Schema
    # We use 'IF NOT EXISTS' so we don't break it if we run it twice
    create_table_query = """
    CREATE TABLE IF NOT EXISTS financial_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT DEFAULT 'Hanwha Ocean',
        year INTEGER,
        revenue_krw REAL,
        op_profit_krw REAL,
        op_margin_percent REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    cursor.execute(create_table_query)
    print("✅ SQL Schema Created: Table 'financial_metrics' is ready.")
    
    # 2. LOAD DATA FROM CSV
    print("\n--- 2. MIGRATING DATA (CSV -> SQL) ---")
    if not os.path.exists(csv_path):
        print("Error: CSV not found.")
        return

    df = pd.read_csv(csv_path)
    
    # 3. INSERT LOOP (The "Ingestion")
    # We clear old data for this company first to avoid duplicates
    cursor.execute("DELETE FROM financial_metrics WHERE company_name = 'Hanwha Ocean'")
    
    for index, row in df.iterrows():
        # SQL INSERT COMMAND
        insert_query = """
        INSERT INTO financial_metrics (year, revenue_krw, op_profit_krw, op_margin_percent)
        VALUES (?, ?, ?, ?)
        """
        data_tuple = (row['Year'], row['Revenue'], row['Op_Profit'], row['Op_Margin_Percent'])
        cursor.execute(insert_query, data_tuple)
        print(f"   -> Ingested Record: Year {int(row['Year'])}")

    # Commit (Save) changes
    conn.commit()
    conn.close()
    print("\n✅ SUCCESS: Data is now secure in 'corporate_data.db'")

def verify_sql():
    print("\n--- 3. VERIFICATION (Running SQL Query) ---")
    conn = sqlite3.connect(db_path)
    
    # CONSULTANT QUERY: "Show me the years where we were profitable"
    sql_query = "SELECT year, op_margin_percent FROM financial_metrics WHERE op_profit_krw > 0"
    
    df_result = pd.read_sql_query(sql_query, conn)
    print("Executed Query: [SELECT year FROM financial_metrics WHERE profit > 0]")
    print(df_result)
    conn.close()

if __name__ == "__main__":
    init_db()
    verify_sql()