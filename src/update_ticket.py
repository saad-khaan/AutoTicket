# update_ticket.py
# Author: Saad Khan

import sqlite3
from pathlib import Path

# Paths
DB_PATH = Path(__file__).resolve().parent.parent / "tickets.db"
LOG_PATH = Path(__file__).resolve().parent.parent / "data" / "diagnostics_output" / "diagnostics.log"

def update_tickets_db():
    # Connect to SQLite database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Read the log and map ticket_id -> status
    results = {}
    if LOG_PATH.exists():
        with open(LOG_PATH, "r") as log:
            for line in log:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 4:
                    ticket_id = parts[1].replace("Ticket #", "").strip()
                    status = parts[3]
                    results[ticket_id] = status
    else:
        print(f"[WARN] Log file not found at {LOG_PATH}")
        conn.close()
        return

    # Update each ticket in the database with diagnostic status
    updated_count = 0
    for t_id, status in results.items():
        c.execute('UPDATE tickets SET diagnostic_status = ? WHERE id = ?', (status, t_id))
        if c.rowcount > 0:
            updated_count += 1

    conn.commit()
    conn.close()
    print(f"[INFO] Updated {updated_count} tickets in the database at {DB_PATH}")

if __name__ == "__main__":
    update_tickets_db()