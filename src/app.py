# Flask web app to display tickets and diagnostic statuses in a table.
# app.py
# Author: Saad Khan

import json
import subprocess 
import sqlite3
from pathlib import Path
from flask import Flask, render_template, redirect, url_for, request

# Point to templates folder in project root
TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
app = Flask(__name__, template_folder=str(TEMPLATE_DIR))

TICKETS_FILE = Path(__file__).resolve().parent.parent / "data" / "tickets_with_results.json"
DB_PATH = Path(__file__).resolve().parent.parent / "tickets.db"

@app.route("/")
def index():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # to access by column name
    c = conn.cursor()
    c.execute('SELECT * FROM tickets')
    tickets = [dict(row) for row in c.fetchall()]
    conn.close()
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