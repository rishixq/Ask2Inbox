from agent_state import AgentState
from graph import build_graph

agent_graph = build_graph()


def run_agent(user_message: str, employee_id: int) -> AgentState:
    state = AgentState(
        user_message=user_message,
        employee_id=employee_id
    )

    result = agent_graph.invoke(state)
    return AgentState(**result)
