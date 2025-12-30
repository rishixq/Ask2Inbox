from enum import Enum


class Intent(str, Enum):
    # Simple chat, no action needed
    CHAT = "CHAT"

    # Read data from SQL and respond
    DB_QUERY = "DB_QUERY"

    # Read data from SQL and send email
    DB_AND_EMAIL = "DB_AND_EMAIL"

    # 👇 NEW: Write leave request to DB
    APPLY_LEAVE = "APPLY_LEAVE"
