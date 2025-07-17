# Flask web app to display tickets and diagnostic statuses in a table.
# app.py
# Author: Saad Khan

import json
import subprocess 
from pathlib import Path
from flask import Flask, render_template, redirect, url_for, request

# Point to templates folder in project root
TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
app = Flask(__name__, template_folder=str(TEMPLATE_DIR))

TICKETS_FILE = Path(__file__).resolve().parent.parent / "data" / "tickets_with_results.json"

@app.route("/")
def index():
    """Render dashboard with ticket data."""
    if TICKETS_FILE.exists():
        with open(TICKETS_FILE, "r") as f:
            tickets = json.load(f)
    else:
        tickets = []
    return render_template("index.html", tickets=tickets)

@app.route("/run-diagnostics", methods=["POST"])
def run_diagnostics():
    """Run the diagnostics and update tickets, then redirect to dashboard."""
    # Run diagnose.py
    subprocess.run(["python", "src/diagnose.py"])
    # Run update_ticket.py
    subprocess.run(["python", "src/update_ticket.py"])
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)