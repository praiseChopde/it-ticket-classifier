"""
IT Ticket Classifier — Command Line Interface
Run this file to classify IT support requests interactively.
"""

import sys
from classifier import classify_ticket
from logger import log_ticket, view_log


# ── Display helpers ───────────────────────────────────────────────────────────
PRIORITY_COLORS = {
    "High":   "\033[91m",  # red
    "Medium": "\033[93m",  # yellow
    "Low":    "\033[92m",  # green
}
CATEGORY_COLORS = {
    "Hardware": "\033[94m",   # blue
    "Network":  "\033[96m",   # cyan
    "Account":  "\033[95m",   # magenta
    "Software": "\033[93m",   # yellow
    "Other":    "\033[90m",   # gray
}
RESET = "\033[0m"
BOLD  = "\033[1m"


def color(text: str, code: str) -> str:
    return f"{code}{text}{RESET}"


def print_banner():
    print(f"\n{BOLD}{'─' * 58}{RESET}")
    print(f"{BOLD}   IT Ticket Classifier — City of Saint John IT Team{RESET}")
    print(f"{BOLD}{'─' * 58}{RESET}\n")


def print_result(ticket_id: str, result: dict):
    cat   = result["category"]
    pri   = result["priority"]
    step  = result["first_step"]

    cat_color = CATEGORY_COLORS.get(cat, "")
    pri_color = PRIORITY_COLORS.get(pri, "")

    print(f"\n{BOLD}Ticket ID  :{RESET}  {ticket_id}")
    print(f"{BOLD}Category   :{RESET}  {color(cat, cat_color)}")
    print(f"{BOLD}Priority   :{RESET}  {color(pri, pri_color)}")
    print(f"\n{BOLD}First Step :{RESET}")
    # Word-wrap the first step at 56 chars
    words = step.split()
    line = "  "
    for word in words:
        if len(line) + len(word) + 1 > 58:
            print(line)
            line = "  " + word
        else:
            line += (" " if line.strip() else "") + word
    if line.strip():
        print(line)
    print(f"\n{BOLD}{'─' * 58}{RESET}")


def print_log(tickets: list[dict]):
    if not tickets:
        print("\n  No tickets logged yet.\n")
        return

    print(f"\n{BOLD}  {'ID':<10} {'Time':<20} {'Category':<12} {'Priority':<8} {'Description'}{RESET}")
    print(f"  {'─'*9} {'─'*19} {'─'*11} {'─'*7} {'─'*30}")
    for t in tickets:
        desc = t["description"][:35] + "..." if len(t["description"]) > 35 else t["description"]
        cat_color  = CATEGORY_COLORS.get(t["category"], "")
        pri_color  = PRIORITY_COLORS.get(t["priority"], "")
        print(
            f"  {t['ticket_id']:<10} "
            f"{t['timestamp']:<20} "
            f"{color(t['category'], cat_color):<22} "
            f"{color(t['priority'], pri_color):<18} "
            f"{desc}"
        )
    print()


def interactive_mode():
    print_banner()
    print("  Commands:")
    print("    classify  — classify a new support request")
    print("    log       — view all logged tickets")
    print("    quit      — exit\n")

    while True:
        try:
            cmd = input(f"{BOLD}> {RESET}").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\n\n  Goodbye.\n")
            break

        if cmd in ("quit", "exit", "q"):
            print("\n  Goodbye.\n")
            break

        elif cmd in ("classify", "c", ""):
            print(f"\n  {BOLD}Describe the IT issue:{RESET}")
            try:
                description = input("  > ").strip()
            except (KeyboardInterrupt, EOFError):
                print()
                continue

            if not description:
                print("  Please enter a description.\n")
                continue

            try:
                result    = classify_ticket(description)
                ticket_id = log_ticket(result)
                print_result(ticket_id, result)
            except ValueError as e:
                print(f"\n  Error: {e}\n")

        elif cmd in ("log", "l", "history"):
            tickets = view_log()
            print_log(tickets)

        else:
            print(f"  Unknown command '{cmd}'. Type 'classify', 'log', or 'quit'.\n")


def single_shot_mode(description: str):
    """Classify a single ticket passed as a command-line argument."""
    try:
        result    = classify_ticket(description)
        ticket_id = log_ticket(result)
        print_banner()
        print_result(ticket_id, result)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # e.g. python main.py "My laptop won't connect to Wi-Fi"
        single_shot_mode(" ".join(sys.argv[1:]))
    else:
        interactive_mode()
