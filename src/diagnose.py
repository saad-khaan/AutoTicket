# diagnose.py
# Author: Saad Khan

import subprocess
import platform
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

# Paths
DB_PATH = Path(__file__).resolve().parent.parent / "tickets.db"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "diagnostics_output"
OUTPUT_LOG = OUTPUT_DIR / "diagnostics.log"

# Make sure output folder exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def ping(host: str) -> bool:
    """
    Ping the given host once. Return True if reachable, False otherwise.
    """
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        result = subprocess.run(["ping", param, "1", host],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
        return result.returncode == 0
    except Exception as e:
        print(f"[ERROR] Ping failed: {e}")
        return False

def run_diagnostics():
    # Load tickets from the database instead of JSON
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, endpoint FROM tickets")
    tickets = c.fetchall()
    conn.close()

    with open(OUTPUT_LOG, "w") as log:
        for ticket_id, endpoint in tickets:
            status = "SUCCESS" if ping(endpoint) else "FAIL"
            timestamp = datetime.now(timezone.utc).isoformat()
            log.write(f"{timestamp} | Ticket #{ticket_id} | {endpoint} | {status}\n")
            print(f"[INFO] Ticket #{ticket_id} ({endpoint}) => {status}")

if __name__ == "__main__":
    run_diagnostics()