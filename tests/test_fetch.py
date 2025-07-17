# Test suite
# test_fetch.py
# Author : Saad Khan

import json
from pathlib import Path
from src.fetch_tickets import fetch_tickets

def test_fetch_returns_list():
    tickets = fetch_tickets()
    assert isinstance(tickets, list), "fetch_tickets should return a list"

def test_ticket_fields_present():
    tickets = fetch_tickets()
    assert all("id" in t and "endpoint" in t for t in tickets), "Each ticket should have id and endpoint"