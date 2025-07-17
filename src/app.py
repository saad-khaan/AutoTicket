# Flask web app to display tickets and diagnostic statuses in a table.
# app.py
# Author : Saad Khan

import json
from pathlib import Path
from flask import Flask, render_template

# Point to templates folder in project root
TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
app = Flask(__name__, template_folder=str(TEMPLATE_DIR))

TICKETS_FILE = Path(__file__).resolve().parent.parent / "data" / "tickets_with_results.json"

@app.route("/")
def index():
    if TICKETS_FILE.exists():
        with open(TICKETS_FILE, "r") as f:
            tickets = json.load(f)
    else:
        tickets = []
    return render_template("index.html", tickets=tickets)

if __name__ == "__main__":
    app.run(debug=True)