import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def create_growth_chart():
    # 1. Connect to the Database
    conn = sqlite3.connect('club_data.db')
    
    # 2. Run the "Growth" Query (Same as Q5)
    query = """
    WITH MonthlyStats AS (
        SELECT strftime('%Y-%m', e.date) as month, COUNT(*) as visits
        FROM attendance a
        JOIN events e ON a.event_id = e.event_id
        GROUP BY month
    )
    SELECT month, visits FROM MonthlyStats ORDER BY month
    """
    
    # 3. Load into Pandas DataFrame (The "Excel" of Python)
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # 4. Setup the Plot (The "McKinsey Style" Look)
    plt.figure(figsize=(10, 6))
    plt.plot(df['month'], df['visits'], marker='o', linestyle='-', color='#005eb8', linewidth=2)
    
    # 5. Add Labels
    plt.title('Member Engagement Trends (MoM)', fontsize=14, fontweight='bold')
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Total Visits', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    
    # 6. Annotate the Peak
    peak_visits = df['visits'].max()
    peak_month = df.loc[df['visits'].idxmax(), 'month']
    plt.annotate(f'Peak: {peak_visits}', xy=(peak_month, peak_visits), xytext=(peak_month, peak_visits+5),
                 arrowprops=dict(facecolor='black', shrink=0.05))

    # 7. Save
    plt.tight_layout()
    plt.savefig('02_Python_Viz/engagement_trend.png')
    print("SUCCESS: Chart generated at '02_Python_Viz/engagement_trend.png'")

if __name__ == "__main__":
    create_growth_chart()