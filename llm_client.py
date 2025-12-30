import os
from dotenv import load_dotenv
from pydantic import SecretStr

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

raw_key = os.getenv("GROQ_API_KEY")
if not raw_key:
    raise RuntimeError("GROQ_API_KEY is not set")

GROQ_API_KEY = SecretStr(raw_key)

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2,
    api_key=GROQ_API_KEY
)


def run_llm(system_prompt: str, user_message: str) -> str:
    """
    SINGLE SOURCE OF TRUTH for BOTH chat and email content.

    ❌ Do not trim
    ❌ Do not format
    ❌ Do not mutate output
    """

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message),
    ]

    response = llm.invoke(messages)
    content = response.content

    # Defensive handling (LangChain may return list in edge cases)
    if isinstance(content, list):
        return "\n".join(
            item if isinstance(item, str) else str(item)
            for item in content
        )

    return str(content)
