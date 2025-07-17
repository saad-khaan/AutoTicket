# AutoTicket Dashboard

**AutoTicket Dashboard** is a full‑stack web application that lets you **monitor network endpoints** from a simple browser dashboard.  
You can add, edit, and delete endpoints (called *tickets*), run automated diagnostics, and instantly see whether those endpoints are reachable.

**Live Demo:** [https://autoticket-dashboard.onrender.com](https://autoticket-dashboard.onrender.com)

---

## What does this app do?

AutoTicket Dashboard is designed as a lightweight network monitoring tool.  
Here’s what it has to offer:

- **Manage tickets (endpoints)**  
  Each ticket is a record with:
  - `ID` – automatically generated
  - `Title` – a friendly name for the endpoint
  - `Endpoint` – an IP address or hostname
  - `Diagnostic Status` – automatically updated (`SUCCESS`, `FAIL`, or `UNKNOWN`)

- **Add new endpoints easily**  
  Use the “Add Ticket” form to add as many endpoints as you want.

- **Edit and delete endpoints**  
  - Edit existing tickets to change their title or endpoint.  
  - Delete tickets you no longer want to monitor (with confirmation before deletion).

- **Run diagnostics on demand**  
  Press **Run Diagnostics** to:
  - Call a Perl script (`diagnose.pl`) that pings each endpoint once.
  - Log the results (`SUCCESS` or `FAIL`) with timestamps.
  - Call a Python script (`update_ticket.py`) that reads the log and updates the database.

- **See results in real-time**  
  The dashboard updates to show each endpoint’s status:
  - ✅ Green for `SUCCESS`
  - ❌ Red for `FAIL`
  - ⚠️ Gray for `UNKNOWN` (before diagnostics)

---

## How does it work internally?

**1. Frontend (Flask templates & CSS)**  
- `index.html` shows the main dashboard and buttons.
- `add_ticket.html`, `edit_ticket.html`, and `delete_ticket.html` handle their respective forms.
- Styling is done with `static/style.css` and `static/button.css` for a clean UI.

**2. Backend (Flask server in `app.py`)**  
- Handles HTTP routes:
  - `/` – dashboard (list tickets from database)
  - `/add-ticket` – form to add a new ticket
  - `/edit-ticket/<id>` – form to edit a ticket
  - `/delete-confirm/<id>` & `/delete-ticket/<id>` – delete flow
  - `/run-diagnostics` – triggers scripts to update statuses
- Communicates with a local SQLite database (`tickets.db`).

**3. Database (SQLite)**  
- A single table: `tickets`
  ```sql
  CREATE TABLE tickets (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      title TEXT NOT NULL,
      endpoint TEXT NOT NULL,
      diagnostic_status TEXT DEFAULT 'UNKNOWN'
  );
- Autocreated if missing.

**4. Diagnostics (Perl & Python scripts)**  
- `diagnose.pl`: Loops through all tickets in the database, pings their endpoints, and writes a `diagnostics.log` with results.
- `update_ticket.py`: Reads the log and updates `diagnostic_status` in `tickets.db`.

---

## Running the App Locally

### Prerequisites
- Python 3.10+
- Perl installed (for `diagnose.pl`)

### Install dependencies
pip install -r requirements.txt

### Run the app
cd src
python app.py

--- 

## Example Tickets

| Title         | Endpoint  |
|---------------|-----------|
| Google DNS    | 8.8.8.8   |
| Cloudflare DNS| 1.1.1.1   |
| Example Site  | example.com |

---

## Example Use Cases

✅ Check availability of internal servers in your network  
✅ Monitor external endpoints like public DNS servers  
✅ Simple uptime checker for hobby projects

---

- This app does not include authentication. Anyone with the link can add/edit/delete tickets. 
- Use this in a trusted environment or add authentication before production use.