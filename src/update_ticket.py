# update_ticket.py
# Author: Saad Khan

import json
from pathlib import Path

# Paths
TICKETS_PATH = Path(__file__).resolve().parent.parent / "data" / "sample_tickets.json"
LOG_PATH = Path(__file__).resolve().parent.parent / "data" / "diagnostics_output" / "diagnostics.log"
UPDATED_PATH = Path(__file__).resolve().parent.parent / "data" / "tickets_with_results.json"

def update_tickets():
    # Load the original tickets
    with open(TICKETS_PATH, "r") as f:
        tickets = json.load(f)

    # Read the log and map ticket_id -> status
    results = {}
    with open(LOG_PATH, "r") as log:
        for line in log:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 4:
                ticket_id = parts[1].replace("Ticket #", "").strip()
                status = parts[3]
                results[ticket_id] = status

    # Update each ticket with diagnostic status
    for t in tickets:
        t_id = str(t.get("id"))
        t["diagnostic_status"] = results.get(t_id, "UNKNOWN")

    # Write updated tickets to a new JSON file
    with open(UPDATED_PATH, "w") as f:
        json.dump(tickets, f, indent=2)

    print(f"[INFO] Updated tickets written to {UPDATED_PATH}")

if __name__ == "__main__":
    update_tickets()