from typing import Optional, Dict
from dataclasses import dataclass
from intents import Intent


@dataclass
class AgentState:
    user_message: str
    employee_id: Optional[int] = None

    intent: Optional[Intent] = None
    db_result: Optional[Dict] = None

    # 🔒 SINGLE SOURCE OF TRUTH
    final_response: Optional[str] = None
    email_content: Optional[str] = None
