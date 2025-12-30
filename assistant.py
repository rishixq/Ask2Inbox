from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from app_state import get_llm, get_vector_store


class Assistant:
    def __init__(self, system_prompt, message_history=None):
        self.system_prompt = system_prompt
        self.llm = get_llm()
        self.vector_store = None
        self.messages = message_history or []
        self.employee_information = {}

    # --------------------------------------------------
    # SAFE, TRIMMED POLICY CONTEXT (RAG)
    # --------------------------------------------------
    def _policy_context(self, query: str) -> str:
        if self.vector_store is None:
            self.vector_store = get_vector_store()

        try:
            docs = self.vector_store.similarity_search(query, k=3)
        except Exception:
            return "No policy context available. Answer generally."

        if not docs:
            return "No specific company policy was found. Answer generally."

        MAX_POLICY_CHARS = 1200
        text = "\n".join(d.page_content for d in docs)
        return text[:MAX_POLICY_CHARS]

    # --------------------------------------------------
    # SAFE, REDUCED EMPLOYEE CONTEXT
    # --------------------------------------------------
    def _safe_employee_context(self):
        if not self.employee_information:
            return "No employee data available."

        allowed_keys = {
            "employee_id",
            "name",
            "email",
            "phone",
            "gender",
            "role",
            "location",
            "employee_type",
            "emergency_contact",
            "address",
            "date_of_birth",
            "designation",
            "department",
            "job_level",
            "leave_balance",
            "salary",
            "skills"
        }

        return {
            k: v
            for k, v in self.employee_information.items()
            if k in allowed_keys and v is not None
        }

    # --------------------------------------------------
    # BUILD UNIFIED CHAIN (TOKEN-SAFE)
    # --------------------------------------------------
    def build_chain(self):
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                self.system_prompt
                + "\n\nEmployee Information:\n{employee_information}\n"
                + "\n\nPolicy Context:\n{policy_context}\n"
            ),
            MessagesPlaceholder("conversation_history"),
            ("human", "{user_input}")
        ])

        MAX_HISTORY = 4
        history = [
            HumanMessage(content=m.content) if m.role == "user"
            else AIMessage(content=m.content)
            for m in self.messages[-MAX_HISTORY:]
        ]

        chain = (
            {
                "employee_information": lambda _: self._safe_employee_context(),
                "policy_context": lambda q: self._policy_context(q),
                "conversation_history": lambda _: history,
                "user_input": RunnablePassthrough(),
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )

        return chain

    # --------------------------------------------------
    # MAIN ENTRY POINT (FAIL-SAFE)
    # --------------------------------------------------
    def get_response(self, user_input: str) -> str:
        try:
            chain = self.build_chain()
            response = chain.invoke(user_input)
        except Exception:
            response = (
                "I’m currently facing a temporary issue accessing internal data. "
                "Here’s a general explanation instead:\n\n"
                "Most organizations conduct appraisals annually based on "
                "goal achievement, manager feedback, and organizational performance."
            )

        self.messages.append(
            type("Msg", (), {"role": "user", "content": user_input})
        )
        self.messages.append(
            type("Msg", (), {"role": "ai", "content": response})
        )

        return response

