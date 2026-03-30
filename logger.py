"""
Ticket Logger
Logs classified tickets to a CSV file for record-keeping,
mirroring a real help desk intake pipeline.
"""

import csv
import os
from datetime import datetime


LOG_FILE = "ticket_log.csv"

HEADERS = [
    "ticket_id",
    "timestamp",
    "description",
    "category",
    "priority",
    "first_step",
]


def _get_next_ticket_id() -> str:
    """Generate a sequential ticket ID based on existing log entries."""
    if not os.path.exists(LOG_FILE):
        return "TKT-001"

    with open(LOG_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        return "TKT-001"

    last_id = rows[-1]["ticket_id"]  # e.g. TKT-042
    try:
        number = int(last_id.split("-")[1]) + 1
        return f"TKT-{number:03d}"
    except (IndexError, ValueError):
        return f"TKT-{len(rows) + 1:03d}"


def log_ticket(result: dict) -> str:
    """
    Append a classified ticket to the CSV log.
    Returns the ticket ID assigned.
    """
    ticket_id = _get_next_ticket_id()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    file_exists = os.path.exists(LOG_FILE)

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "ticket_id": ticket_id,
            "timestamp": timestamp,
            "description": result["description"],
            "category": result["category"],
            "priority": result["priority"],
            "first_step": result["first_step"],
        })

    return ticket_id


def view_log() -> list[dict]:
    """Return all logged tickets as a list of dicts."""
    if not os.path.exists(LOG_FILE):
        return []

    with open(LOG_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)
