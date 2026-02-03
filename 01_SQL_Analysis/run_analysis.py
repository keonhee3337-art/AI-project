import sqlite3

def run_analysis():
    # Connect to database
    conn = sqlite3.connect('club_data.db')
    c = conn.cursor()
    
    # Prepare the output file
    with open('Executive_Brief.txt', 'w', encoding='utf-8') as f:
        f.write(f"CLUB ANALYTICS REPORT - {datetime.now().strftime('%Y-%m-%d')}\n")
        f.write("="*50 + "\n\n")

        # --- HELPER FUNCTION TO WRITE TO FILE ---
        def write_query(title, query):
            f.write(f"### {title} ###\n")
            try:
                c.execute(query)
                results = c.fetchall()
                if not results:
                    f.write("No results found.\n")
                else:
                    # Get column headers
                    names = [description[0] for description in c.description]
                    f.write(f"{str(names)}\n")
                    # Write rows
                    for row in results:
                        f.write(f"{str(row)}\n")
            except Exception as e:
                f.write(f"ERROR: {e}\n")
            f.write("\n" + "-"*30 + "\n\n")

        # --- Q1: TALENT SOURCING ---
        sql_q1 = """
        SELECT name, major 
        FROM members 
        WHERE year = 4
        """
        write_query("Q1: SENIOR TALENT LIST", sql_q1)

        # --- Q2: DIVERSITY AUDIT ---
        sql_q2 = """
        SELECT major, COUNT(*) as count 
        FROM members 
        GROUP BY major 
        ORDER BY count DESC
        """
        write_query("Q2: MEMBER BREAKDOWN BY MAJOR", sql_q2)

        # --- Q3: ENGAGEMENT CHECK (FIXED) ---
        # Logic: SELECT name -> FROM members -> JOIN attendance -> GROUP BY ID -> COUNT
        sql_q3 = """
        SELECT m.name, COUNT(a.event_id) as attendance_count
        FROM members m
        JOIN attendance a ON m.id = a.member_id
        GROUP BY m.id
        ORDER BY attendance_count DESC
        LIMIT 5
        """
        write_query("Q3: TOP 5 MOST ACTIVE MEMBERS", sql_q3)

        # --- Q4: STRETCH GOAL (PASSIVE ANALYSIS) ---
        sql_q4 = """
        SELECT major, COUNT(*) as count
        FROM members
        WHERE status = 'Passive'
        GROUP BY major
        ORDER BY count DESC
        """
        write_query("Q4: PASSIVE MEMBER ANALYSIS", sql_q4)

    conn.close()
    print("SUCCESS: Report generated at 'Executive_Brief.txt'")

from datetime import datetime
if __name__ == "__main__":
    run_analysis()