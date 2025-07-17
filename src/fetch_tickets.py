# fetch_tickets.py
# Author: Saad Khan

import json
from pathlib import Path

TICKETS_PATH = Path(__file__).resolve().parent.parent / "data" / "sample_tickets.json"

def fetch_tickets():
    if not TICKETS_PATH.exists():
        print(f"[ERROR] Tickets file not found at {TICKETS_PATH}")
        return []
    with open(TICKETS_PATH, "r") as f:
        tickets = json.load(f)
    print("[INFO] Fetched tickets:")
    for t in tickets:
        print(f"- #{t['id']} | {t['title']} | endpoint: {t['endpoint']}")
    return tickets

if __name__ == "__main__":
    fetch_tickets()