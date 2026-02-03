import sqlite3
import random
from datetime import datetime, timedelta

# Connect to database (creates it if it doesn't exist)
conn = sqlite3.connect('club_data.db')
c = conn.cursor()

# 1. Create Tables
c.execute('''CREATE TABLE IF NOT EXISTS members
             (id INTEGER PRIMARY KEY, name TEXT, major TEXT, year INTEGER, status TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS events
             (event_id INTEGER PRIMARY KEY, date TEXT, event_type TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS attendance
             (attendance_id INTEGER PRIMARY KEY, member_id INTEGER, event_id INTEGER,
              FOREIGN KEY(member_id) REFERENCES members(id),
              FOREIGN KEY(event_id) REFERENCES events(event_id))''')

# 2. Generate Mock Data
majors = ['Business', 'Economics', 'CS', 'Engineering', 'Art']
statuses = ['Active', 'Passive', 'Alumni']
event_types = ['Workshop', 'Social', 'Case Study', 'Guest Speaker']

# Create 500 Members
members_data = []
for i in range(1, 501):
    members_data.append((i, f'Student_{i}', random.choice(majors), random.randint(1, 4), random.choice(statuses)))

c.executemany('INSERT OR IGNORE INTO members VALUES (?,?,?,?,?)', members_data)

# Create 20 Events
events_data = []
start_date = datetime(2023, 9, 1)
for i in range(1, 21):
    event_date = start_date + timedelta(weeks=i)
    events_data.append((i, event_date.strftime('%Y-%m-%d'), random.choice(event_types)))

c.executemany('INSERT OR IGNORE INTO events VALUES (?,?,?)', events_data)

# Create Attendance (Random)
attendance_data = []
for event_id in range(1, 21):
    # Randomly pick 30-50 members per event
    attendees = random.sample(range(1, 501), random.randint(30, 50))
    for member_id in attendees:
        attendance_data.append((member_id, event_id))

c.executemany('INSERT OR IGNORE INTO attendance (member_id, event_id) VALUES (?,?)', attendance_data)

conn.commit()
conn.close()
print("SUCCESS: 'club_data.db' created with 500 members and 20 events.")