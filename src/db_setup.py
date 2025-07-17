# Setting up database
# db_setup.py
# Author: Saad Khan

import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "tickets.db"
JSON_PATH = Path(__file__).resolve().parent.parent / "data" / "sample_tickets.json"

# Connect to SQLite
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Create table
c.execute('''
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY,
    title TEXT,
    endpoint TEXT,
    diagnostic_status TEXT
)
''')

# Load from JSON and insert into table
if JSON_PATH.exists():
    with open(JSON_PATH, "r") as f:
        tickets = json.load(f)
        for t in tickets:
            c.execute('INSERT OR IGNORE INTO tickets (id, title, endpoint, diagnostic_status) VALUES (?, ?, ?, ?)',
                      (t['id'], t['title'], t['endpoint'], t.get('diagnostic_status', 'UNKNOWN')))

conn.commit()
conn.close()
print("Database created and populated!")