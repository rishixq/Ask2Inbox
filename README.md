```md
# Ask2Inbox — Agentic AI Assistant with Chat–Email Parity

**Ask2Inbox** is a production-grade, agentic Employee Self-Service (ESS) platform where users **ask once** and receive the **same AI-generated response** in both **chat and email**.

The system is designed around a **single LLM source of truth**, with email treated strictly as a **delivery channel**, not a formatter.

> 🧠 Chat = Email. Always.

---

## ✨ Key Highlights

- Agentic architecture using **LangGraph**
- Strict **chat–email parity** (same LLM output, no reformatting)
- SQL-backed employee data access
- Real email delivery via SMTP
- Clean FastAPI backend + modern React frontend
- Interview-ready, production-style design

---

## 🚀 What Ask2Inbox Can Do

- Answer general and out-of-the-box questions professionally
- Fetch structured employee data from SQL
- Decide actions dynamically based on intent
- Send identical responses to chat **and** inbox on request
- Notify users in UI when an email copy is sent

---

## 🧠 High-Level Architecture

```

User (Chat UI)
↓
FastAPI (/chat)
↓
Agent Runner (agent.py)
↓
LangGraph State Machine
├── Chat Node (LLM only)
├── DB Node (SQL + LLM)
└── Leave Node (DB write)
↓
Single LLM Output
├── Displayed in Chat
└── Sent via Email (if requested)

```

---

## 🧩 Core Design Principle

### 🔒 Single Source of Truth

- The **LLM output** is generated **once**
- That same string is:
  - Rendered in chat
  - Sent as a plain-text email
- No secondary formatting
- No email-specific templates

This avoids inconsistencies and mirrors **real enterprise systems**.

## 🛠️ Tech Stack

### Backend
- **FastAPI** — API layer
- **LangGraph** — agent orchestration
- **LangChain (Groq)** — LLM integration
- **SQLAlchemy** — database ORM
- **PostgreSQL** — employee data
- **SMTP (Gmail App Password)** — email delivery

### Frontend
- **React**
- Clean chat UI
- Branded Ask2Inbox theme
- UI-level email delivery notifications

---

## 🧪 Example Requests

### Chat only
```

Show my salary details

```

### Chat + Email
```

Email my assets

```

Result:
- Structured response shown in chat
- Same response delivered to inbox
- UI shows: “A copy has been sent to your registered email.”

---

## 📸 Screenshots

/screenshots
├── login.png
├── chat.png
├── email.png

````

## 🎥 Demo Video

```md
▶️ Demo Video: https://youtu.be/your-demo-link
```

---

## 🌍 Deployed Site

```md
🔗 Live Demo: https://ask2inbox.yourdomain.com
```

---

## ⚙️ How to Run Locally

### Backend

```bash
# Activate virtual environment
.venv\Scripts\activate

# Run FastAPI server
uvicorn main:app --reload
```

### Frontend

```bash
npm install
npm start
```

---

## 🔐 Environment Variables

Create a `.env` file (not committed):

```env
DATABASE_URL=
GROQ_API_KEY=
EMAIL_SENDER=
EMAIL_APP_PASSWORD=
```

---

## 🎯 Why This Project Matters

* Demonstrates **true agentic design**, not prompt hacks
* Clean separation of concerns:

  * API
  * Agent
  * Graph
  * Tools
* Real side-effects (SQL + Email)
* Strong focus on **correctness, parity, and UX**
* Easy to explain in interviews

---

## 👤 Author

**Rishi Kishore**

> Ask once. Straight to inbox.
