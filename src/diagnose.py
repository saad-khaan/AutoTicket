# diagnose.py
# Author : Saad Khan

import subprocess
import platform
import datetime
import json
from pathlib import Path

# Paths
TICKETS_PATH = Path(__file__).resolve().parent.parent / "data" / "sample_tickets.json"
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
    # Load tickets
    with open(TICKETS_PATH, "r") as f:
        tickets = json.load(f)

    with open(OUTPUT_LOG, "w") as log:
        for t in tickets:
            endpoint = t.get("endpoint")
            ticket_id = t.get("id")
            status = "SUCCESS" if ping(endpoint) else "FAIL"
            timestamp = datetime.datetime.utcnow().isoformat()
            log.write(f"{timestamp} | Ticket #{ticket_id} | {endpoint} | {status}\n")
            print(f"[INFO] Ticket #{ticket_id} ({endpoint}) => {status}")

if __name__ == "__main__":
    run_diagnostics()