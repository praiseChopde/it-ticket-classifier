# IT Ticket Classifier

A command-line tool that classifies IT support requests into categories, assigns priority levels, suggests a first troubleshooting step, and logs every ticket to a CSV file — mirroring a real help desk intake pipeline.

Built as a portfolio project demonstrating practical understanding of IT support workflows and Python software design.

---

## Demo

```
──────────────────────────────────────────────────────
   IT Ticket Classifier — City of Saint John IT Team
──────────────────────────────────────────────────────

  Commands:
    classify  — classify a new support request
    log       — view all logged tickets
    quit      — exit

> classify

  Describe the IT issue:
  > My laptop won't connect to the Wi-Fi network after the Windows update

Ticket ID  :  TKT-001
Category   :  Network
Priority   :  High

First Step :
  Ask the user to disconnect and reconnect to Wi-Fi.
  If on VPN, disconnect and reconnect GlobalProtect.
  Run 'ipconfig /release' then 'ipconfig /renew' in
  Command Prompt. Ping 8.8.8.8 to test basic
  connectivity.

──────────────────────────────────────────────────────
```

---

## Features

- **5 classification categories** — Hardware, Network, Account, Software, Other
- **3 priority levels** — High, Medium, Low (based on urgency keyword detection)
- **Tailored first step** — each category has a specific, actionable first troubleshooting response
- **CSV ticket log** — every classified ticket is saved to `ticket_log.csv` with a unique ID and timestamp
- **Two modes** — interactive CLI or single-shot command-line argument
- **17 unit tests** — full test coverage across classification, priority, and pipeline logic

---

## Project Structure

```
it-ticket-classifier/
├── classifier.py        # Core classification logic (category + priority + first step)
├── logger.py            # CSV ticket logging with auto-incrementing ticket IDs
├── main.py              # CLI entry point (interactive + single-shot modes)
├── test_classifier.py   # 17 unit tests
└── ticket_log.csv       # Auto-generated on first run
```

---

## How to Run

**Requirements:** Python 3.10+ — no external libraries needed.

**Interactive mode:**
```bash
python main.py
```

**Single-shot mode:**
```bash
python main.py "My password expired and I can't log in to my workstation"
```

**Run tests:**
```bash
python test_classifier.py
```

---

## Classification Logic

### Categories
Each ticket description is scanned for keywords mapped to 5 categories:

| Category | Example keywords |
|---|---|
| Hardware | laptop, monitor, printer, keyboard, battery, blue screen, overheating |
| Network | wifi, vpn, globalprotect, ethernet, no internet, mapped drive |
| Account | password, locked out, expired, MFA, active directory, access denied |
| Software | outlook, teams, crash, install, update, error, intune, sharepoint |
| Other | anything that doesn't match the above |

The category with the most keyword hits wins. Ties go to the first match.

### Priority
| Level | Triggered by |
|---|---|
| High | locked out, urgent, blue screen, virus, no internet, can't work |
| Medium | slow, freezing, crashing, not syncing, intermittent |
| Low | everything else (e.g. hardware requests, minor issues) |

---

## Sample Ticket Log Output

```
ticket_id  timestamp            category   priority  description
TKT-001    2026-03-30 22:14:05  Network    High      My laptop won't connect to Wi-Fi...
TKT-002    2026-03-30 22:15:33  Account    High      Password expired, locked out of workstation
TKT-003    2026-03-30 22:16:01  Software   Medium    Outlook keeps crashing when opening attachments
TKT-004    2026-03-30 22:17:44  Hardware   Low       Requesting a second monitor for my workstation
```



## Why I Built This

The City of Saint John IT team handles hundreds of support requests across municipal departments. Effective triage — quickly identifying what category an issue falls into and what to do first — is one of the most critical daily tasks in deskside IT support.

This tool formalizes that process in code, demonstrating that I understand how IT support workflows actually function before day one on the job.

I got help from youtube videos, stack overflow and AI agents to finalize and underestand the in's and out's of the project. 

## About

Built by **Praise Chopde** 
Computer Science student, University of New Brunswick (2024–2028)
