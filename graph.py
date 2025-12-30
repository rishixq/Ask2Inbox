from langgraph.graph import StateGraph
from agent_state import AgentState
from intent_detector import detect_intent
from intents import Intent

from database import SessionLocal
from services.employee_service import get_full_employee_profile
from services.leave_service import apply_leave

from tools.email_tool import send_email
from prompts import SYSTEM_PROMPT
from llm_client import run_llm

from datetime import date


# --------------------------------------------------
# START NODE
# --------------------------------------------------
def start_node(state: AgentState) -> AgentState:
    return state


# --------------------------------------------------
# INTENT DETECTION
# --------------------------------------------------
def intent_node(state: AgentState) -> AgentState:
    state.intent = detect_intent(state.user_message)
    return state


# --------------------------------------------------
# ROUTING
# --------------------------------------------------
def route_by_intent(state: AgentState) -> str:
    if state.intent == Intent.APPLY_LEAVE:
        return "leave_node"

    if state.intent in (Intent.DB_QUERY, Intent.DB_AND_EMAIL):
        return "db_node"

    return "chat_node"


# --------------------------------------------------
# CHAT NODE (NO DB)
# --------------------------------------------------
def chat_node(state: AgentState) -> AgentState:
    filled_prompt = SYSTEM_PROMPT.format(
        employee_information="N/A",
        policy_context="No policy context provided."
    )

    state.final_response = run_llm(
        system_prompt=filled_prompt,
        user_message=state.user_message
    )

    return state


# --------------------------------------------------
# DB NODE (LLM + OPTIONAL EMAIL)
# --------------------------------------------------
def db_node(state: AgentState) -> AgentState:
    if not state.employee_id:
        state.final_response = "Employee not identified."
        return state

    db = SessionLocal()
    try:
        profile = get_full_employee_profile(db, employee_id=state.employee_id)

        if not profile:
            state.final_response = "Employee not found."
            return state

        state.db_result = profile

        filled_prompt = SYSTEM_PROMPT.format(
            employee_information=profile,
            policy_context="No policy context provided."
        )

        # 🔒 SINGLE LLM CALL (SOURCE OF TRUTH)
        llm_output = run_llm(
            system_prompt=filled_prompt,
            user_message=state.user_message
        )

        state.final_response = llm_output
        state.email_content = llm_output

        # 🔥 SEND EMAIL ONLY IF INTENT REQUIRES IT
        if state.intent == Intent.DB_AND_EMAIL:
            email = profile.get("email")
            if email:
                send_email(
                    to_email=email,
                    subject="Requested Employee Information",
                    body=state.email_content
                )

    finally:
        db.close()

    return state


# --------------------------------------------------
# LEAVE NODE (WRITE OP – TEMP EXCEPTION)
# --------------------------------------------------
def leave_node(state: AgentState) -> AgentState:
    if not state.employee_id:
        state.final_response = "Employee not identified."
        return state

    db = SessionLocal()
    try:
        leave = apply_leave(
            db=db,
            employee_id=state.employee_id,
            leave_type="Casual",
            start_date=date.today(),
            end_date=date.today()
        )

        profile = get_full_employee_profile(db, employee_id=state.employee_id)

        if profile and profile.get("email"):
            send_email(
                to_email=profile["email"],
                subject="Leave Application Submitted",
                body=(
                    f"Leave request submitted successfully.\n\n"
                    f"Type: {leave.leave_type}\n"
                    f"From: {leave.start_date}\n"
                    f"To: {leave.end_date}\n"
                    f"Status: {leave.status}"
                )
            )

        state.final_response = (
            f"✅ Leave applied successfully.\n\n"
            f"Type: {leave.leave_type}\n"
            f"From: {leave.start_date}\n"
            f"To: {leave.end_date}\n"
            f"Status: {leave.status}"
        )

    finally:
        db.close()

    return state


# --------------------------------------------------
# END NODE
# --------------------------------------------------
def end_node(state: AgentState) -> AgentState:
    return state


# --------------------------------------------------
# GRAPH BUILDER
# --------------------------------------------------
def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("start", start_node)
    graph.add_node("detect_intent", intent_node)
    graph.add_node("chat_node", chat_node)
    graph.add_node("db_node", db_node)
    graph.add_node("leave_node", leave_node)
    graph.add_node("end", end_node)

    graph.set_entry_point("start")

    graph.add_edge("start", "detect_intent")

    graph.add_conditional_edges(
        "detect_intent",
        route_by_intent,
        {
            "chat_node": "chat_node",
            "db_node": "db_node",
            "leave_node": "leave_node",
        }
    )

    graph.add_edge("chat_node", "end")
    graph.add_edge("db_node", "end")
    graph.add_edge("leave_node", "end")

    graph.set_finish_point("end")

    return graph.compile()
