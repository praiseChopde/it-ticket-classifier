"""
IT Ticket Classifier
Classifies IT support requests into categories, assigns priority,
and suggests a first troubleshooting step.
"""

# ── Category keyword mapping ──────────────────────────────────────────────────
CATEGORIES = {
    "Hardware": [
        "laptop", "computer", "pc", "screen", "monitor", "keyboard", "mouse",
        "printer", "printer", "headset", "headphone", "webcam", "camera",
        "charger", "battery", "power", "won't turn on", "not turning on",
        "black screen", "blue screen", "bsod", "broken", "cracked", "damaged",
        "docking station", "dock", "usb", "port", "ram", "memory", "hard drive",
        "ssd", "fan", "overheating", "hot", "slow", "freezing", "frozen",
        "device", "peripheral", "cable", "second monitor", "display",
        "surface", "iphone", "tablet", "mobile device", "phone"
    ],
    "Network": [
        "wifi", "wi-fi", "wireless", "internet", "network", "connected",
        "connection", "vpn", "globalprotect", "ethernet", "cable", "lan",
        "no internet", "can't connect", "cannot connect", "slow internet",
        "disconnected", "drops", "dropping", "bandwidth", "remote access",
        "remote", "ping", "dns", "ip address", "firewall", "proxy",
        "network drive", "shared drive", "mapped drive", "file share"
    ],
    "Account": [
        "password", "login", "log in", "locked out", "locked", "account",
        "username", "forgot password", "reset password", "can't log in",
        "cannot log in", "expired", "access denied", "permissions",
        "active directory", "mfa", "authenticator", "two factor", "2fa",
        "sign in", "signed out", "credentials", "access", "unauthorized",
        "not authorized", "privilege", "admin rights", "elevation"
    ],
    "Software": [
        "software", "application", "app", "install", "uninstall", "update",
        "upgrade", "error", "crash", "crashing", "not opening", "won't open",
        "not working", "broken", "outlook", "teams", "excel", "word",
        "powerpoint", "office", "microsoft", "adobe", "chrome", "browser",
        "edge", "firefox", "antivirus", "virus", "malware", "pop-up",
        "popup", "license", "activation", "expired license", "sharepoint",
        "onedrive", "sync", "not syncing", "email", "calendar", "intune",
        "company portal", "enrollment", "mdm"
    ],
}

# ── Priority keyword mapping ───────────────────────────────────────────────────
HIGH_KEYWORDS = [
    "can't work", "cannot work", "urgent", "emergency", "asap", "immediately",
    "locked out", "locked", "no access", "down", "not working at all",
    "won't turn on", "black screen", "blue screen", "bsod", "data loss",
    "virus", "malware", "security", "breach", "stolen", "lost device",
    "critical", "deadline", "meeting", "presentation", "expired password",
    "can't log in", "cannot log in", "no internet", "vpn down"
]

MEDIUM_KEYWORDS = [
    "slow", "freezing", "frozen", "crashing", "crash", "error", "not syncing",
    "sync", "email", "outlook", "teams", "not receiving", "intermittent",
    "sometimes", "occasional", "keeps disconnecting", "drops"
]

# ── First troubleshooting steps ────────────────────────────────────────────────
FIRST_STEPS = {
    "Hardware": (
        "Ask the user to restart the device first. "
        "If issue persists, physically inspect the hardware for visible damage. "
        "Check all cable connections and try a different port or peripheral if available."
    ),
    "Network": (
        "Ask the user to disconnect and reconnect to Wi-Fi. "
        "If on VPN, disconnect and reconnect GlobalProtect. "
        "Run 'ipconfig /release' then 'ipconfig /renew' in Command Prompt. "
        "Ping 8.8.8.8 to test basic connectivity."
    ),
    "Account": (
        "Verify the username is correct and Caps Lock is off. "
        "Check if the account is locked in Active Directory. "
        "Reset the password via the self-service portal or IT admin tools. "
        "Ensure MFA is set up correctly if remote access is involved."
    ),
    "Software": (
        "Ask the user to close and reopen the application. "
        "Check for pending Windows or application updates. "
        "Try running the application as Administrator. "
        "If crashing, check Event Viewer for error logs."
    ),
    "Other": (
        "Gather more details from the user: what exactly happened, "
        "when it started, and what they were doing at the time. "
        "Escalate to the appropriate IT team member if needed."
    ),
}


# ── Core classification logic ─────────────────────────────────────────────────
def classify_category(text: str) -> tuple[str, dict]:
    """
    Classify the ticket text into a category.
    Returns (category, scores) where scores show keyword hit counts.
    """
    text_lower = text.lower()
    scores = {cat: 0 for cat in CATEGORIES}

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in text_lower:
                scores[category] += 1

    best_category = max(scores, key=scores.get)

    # If no keywords matched at all, return Other
    if scores[best_category] == 0:
        return "Other", scores

    return best_category, scores


def classify_priority(text: str) -> str:
    """Assign priority based on urgency keywords."""
    text_lower = text.lower()

    for keyword in HIGH_KEYWORDS:
        if keyword in text_lower:
            return "High"

    for keyword in MEDIUM_KEYWORDS:
        if keyword in text_lower:
            return "Medium"

    return "Low"


def get_first_step(category: str) -> str:
    """Return the recommended first troubleshooting step."""
    return FIRST_STEPS.get(category, FIRST_STEPS["Other"])


def classify_ticket(description: str) -> dict:
    """
    Full classification pipeline for a ticket description.
    Returns a dict with category, priority, and first_step.
    """
    if not description or not description.strip():
        raise ValueError("Ticket description cannot be empty.")

    category, scores = classify_category(description)
    priority = classify_priority(description)
    first_step = get_first_step(category)

    return {
        "description": description.strip(),
        "category": category,
        "priority": priority,
        "first_step": first_step,
        "scores": scores,
    }
