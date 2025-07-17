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
    # Run diagnose.pl
    subprocess.run(["perl", "src/diagnose.pl"])
    # Run update_ticket.py
    subprocess.run(["python", "src/update_ticket.py"])
    return redirect(url_for("index"))

@app.route("/add-ticket", methods=["GET", "POST"])
def add_ticket():
    if request.method == "POST":
        title = request.form.get("title")
        endpoint = request.form.get("endpoint")
        
        if title and endpoint:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute('INSERT INTO tickets (title, endpoint, diagnostic_status) VALUES (?, ?, ?)',
                      (title, endpoint, "UNKNOWN"))
            conn.commit()
            conn.close()
            return redirect(url_for("index"))
    
    # If GET request, show the form
    return render_template("add_ticket.html")

@app.route("/delete-confirm/<int:ticket_id>", methods=["GET"])
def delete_confirm(ticket_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM tickets WHERE id = ?', (ticket_id,))
    ticket = c.fetchone()
    conn.close()
    return render_template("delete_ticket.html", ticket=ticket)

@app.route("/delete-ticket/<int:ticket_id>", methods=["POST"])
def delete_ticket(ticket_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM tickets WHERE id = ?', (ticket_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/edit-ticket/<int:ticket_id>", methods=["GET", "POST"])
def edit_ticket(ticket_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    if request.method == "POST":
        title = request.form.get("title")
        endpoint = request.form.get("endpoint")
        c.execute('UPDATE tickets SET title = ?, endpoint = ? WHERE id = ?', (title, endpoint, ticket_id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    c.execute('SELECT * FROM tickets WHERE id = ?', (ticket_id,))
    ticket = c.fetchone()
    conn.close()
    return render_template("edit_ticket.html", ticket=ticket)

if __name__ == "__main__":
    app.run(debug=True)