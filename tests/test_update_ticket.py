# Test suite
# test_update_ticket.py
# Author : Saad Khan

import json
from pathlib import Path
from src.update_ticket import update_tickets, UPDATED_PATH

def test_update_tickets_creates_file(tmp_path, monkeypatch):

    import src.update_ticket as updater
    updater.UPDATED_PATH = tmp_path / "tickets_with_results.json"

    update_tickets()

    # Check file exists
    assert updater.UPDATED_PATH.exists(), "Updated tickets file should be created"

    # Check contents have diagnostic_status field
    data = json.loads(updater.UPDATED_PATH.read_text())
    assert isinstance(data, list)
    for ticket in data:
        assert "diagnostic_status" in ticket, "Each ticket should have a diagnostic_status field"