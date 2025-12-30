from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from intents import Intent


from database import SessionLocal
from services.employee_service import (
    get_employee_by_code,
    get_full_employee_profile
)

from agent import run_agent

app = FastAPI(title="Ask2Inbox API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Models ----------
class LoginRequest(BaseModel):
    employee_code: str
    email: str


class ChatRequest(BaseModel):
    message: str
    employee_id: int


@app.get("/")
def health():
    return {"status": "Ask2Inbox backend running"}


# ---------- Login ----------
@app.post("/login")
def login(data: LoginRequest):
    db = SessionLocal()
    try:
        emp = get_employee_by_code(db, data.employee_code)

        if not emp:
            raise HTTPException(status_code=404, detail="Employee not found")

        if not data.email:
            raise HTTPException(status_code=400, detail="Email is required")

        if emp.email.lower() != data.email.lower():
            raise HTTPException(
                status_code=401,
                detail="Employee code and email do not match"
            )

        return get_full_employee_profile(db, employee_id=emp.id)  # type: ignore[arg-type]




    finally:
        db.close()


# ---------- Chat (Agentic) ----------
@app.post("/chat")
def chat(request: ChatRequest):
    state = run_agent(
        user_message=request.message,
        employee_id=request.employee_id
    )

    return {
        "intent": state.intent.value if state.intent else None,
        "response": state.final_response,
        "email_sent": state.intent == Intent.DB_AND_EMAIL
    }
