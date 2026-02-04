import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. Connect to Database
db_path = "club_data.db"

def plot_growth_trajectory():
    print("--- 1. CONNECTING TO SQL ---")
    conn = sqlite3.connect(db_path)
    
    # 2. The Query: Get Monthly Volume
    # FIX: We use COUNT(*) to count rows regardless of column names
    query = """
    SELECT 
        strftime('%Y-%m', e.date) as month, 
        COUNT(*) as monthly_volume
    FROM attendance a
    JOIN events e ON a.event_id = e.event_id
    GROUP BY month
    ORDER BY month
    """
    
    # 3. Load Data
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if df.empty:
        print("Error: No data found.")
        return

    # 4. The "Hockey Stick" Math (Cumulative Sum)
    df['cumulative_volume'] = df['monthly_volume'].cumsum()
    
    print("--- 2. GENERATING STRATEGIC CHART ---")
    
    # 5. Draw the Chart
    plt.figure(figsize=(10, 6))
    
    # Plotting the Cumulative Line
    plt.plot(df['month'], df['cumulative_volume'], marker='o', linestyle='-', color='#0052cc', linewidth=3)
    plt.fill_between(df['month'], df['cumulative_volume'], color='#0052cc', alpha=0.1)
    
    # Styling
    plt.title("Cumulative Operational Scale (Member Sessions)", fontsize=16, fontweight='bold')
    plt.xlabel("Timeline", fontsize=12)
    plt.ylabel("Total Sessions Delivered", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(rotation=45)
    
    # Save
    plt.tight_layout()
    plt.savefig("02_Python_Viz/growth_chart.png")
    print(f"SUCCESS: Chart saved to '02_Python_Viz/growth_chart.png'")
    print(f"Current Cumulative Volume: {df['cumulative_volume'].iloc[-1]}")

# --- EXECUTION BLOCK ---
if __name__ == "__main__":
    plot_growth_trajectory()