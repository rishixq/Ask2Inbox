from intents import Intent


EMAIL_TRIGGERS = ["email", "mail", "send"]

ESS_KEYWORDS = [
    "salary", "ctc", "payslip",
    "leave", "assets", "skills",
    "profile", "details"
]


def detect_intent(text: str) -> Intent:
    msg = text.lower()

    # APPLY LEAVE (explicit action)
    if "apply leave" in msg:
        return Intent.APPLY_LEAVE

    # EMAIL + ESS DATA
    if any(e in msg for e in EMAIL_TRIGGERS) and any(k in msg for k in ESS_KEYWORDS):
        return Intent.DB_AND_EMAIL

    # ESS VIEW ONLY
    if any(k in msg for k in ESS_KEYWORDS):
        return Intent.DB_QUERY

    # DEFAULT CHAT
    return Intent.CHAT
