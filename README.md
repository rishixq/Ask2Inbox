# 📬 **Ask2Inbox — Ask Once. Straight to Inbox.**

**FastAPI · LangGraph · SQLAlchemy · Groq LLM · React**

**Ask2Inbox** is a **production-style, agentic Employee Self-Service (ESS) platform** that allows employees to **ask a question once** and receive **identical, enterprise-ready responses** in both **chat and email** — through a modern, ChatGPT-style interface.

Built with **clean architecture**, **deployment-ready practices**, and **real-world enterprise constraints**, Ask2Inbox treats **email as a delivery channel, not a formatter**, enforcing strict **chat–email parity**.

---

## 🌍 Deployed Site

👉 *(https://ask2-inbox.vercel.app/)*
Note: SMTP is blocked on most PaaS platforms; production systems use transactional email APIs. So, my email feature won't work in the deployed site but does work in live browser.

---

## 🎥 Demo Video

▶️ **Watch the full working demo:**
👉 *([https://youtu.be/ojo1_EWkHsU](https://youtu.be/ojo1_EWkHsU))*

## Screenshot

<img width="1869" height="899" alt="Screenshot 2026-01-01 122047" src="https://github.com/user-attachments/assets/6817d95a-884e-469e-a704-7d01b3a0b889" />


---

## ✨ Key Capabilities

### 🧠 Intelligent Agentic Chat

* Handles **general and out-of-the-box questions**
* Maintains a **professional, modern enterprise tone**
* Operates using authenticated employee context
* Responds like a real internal corporate assistant, not a demo bot

---

### 🗄️ SQL-Backed Employee Intelligence

* Reads structured employee data from a relational database:

  * Profile details
  * Salary information
  * Leave balance and history
  * Skills
  * Assets
  * Performance goals
* No ORM objects leak beyond the service layer
* JSON-safe, serialized data only

---

### 📧 Chat–Email Parity (Core System Constraint)

* Email responses are generated **entirely by the LLM**
* The **same response** is:

  * Displayed in chat
  * Sent via email
* No email templates
* No formatting layers
* No duplicated rendering logic

Email is treated strictly as a **transport mechanism**, mirroring real enterprise systems.

---

### 🔁 Agentic Decision-Making

The system dynamically determines how to handle each request:

* **Chat only** → LLM response
* **DB query** → SQL read + LLM response
* **DB + Email** → SQL read + LLM response + email delivery
* **DB write** → Controlled actions (e.g., leave application)

This mirrors **real internal enterprise assistants**, not static workflows.

---

## 🧠 How Ask2Inbox Works (End-to-End)

1. Employee logs in using employee code and email
2. Backend authenticates and resolves `employee_id`
3. Employee sends a chat message
4. Agent runner initializes agent state
5. LangGraph orchestrates execution:

   * Intent detection
   * Node routing
6. Appropriate node executes:

   * Chat
   * Database read
   * Database read + email
   * Database write
7. A **single LLM response** is generated
8. Response is:

   * Returned to chat
   * Sent via email (if requested)

This reflects **real-world internal AI assistants**, not demo-only bots.

---

## 🧱 Tech Stack

### Backend

* Python
* FastAPI
* LangGraph
* SQLAlchemy
* PostgreSQL
* SMTP (Email delivery)

### LLM

* Groq
* Model: `llama-3.1-8b-instant`

### Frontend

* React
* Tailwind CSS
* Custom Chat UI (no heavy UI libraries)
* Ask2Inbox-branded design
* UI-level email delivery notifications

---

## 📁 Project Structure

```
Ask2Inbox/
│
├── main.py                 # FastAPI app & API routes
├── agent.py                # Agent runner
├── graph.py                # LangGraph state machine
├── agent_state.py          # AgentState definition
├── intent_detector.py      # Intent classification
│
├── database.py             # SQLAlchemy engine & session
├── models.py               # Employee-related models
├── services/
│   ├── employee_service.py
│   └── leave_service.py
│
├── tools/
│   └── email_tool.py       # SMTP email sender
│
├── llm_client.py           # Groq LLM wrapper
├── prompts.py              # System prompt (Echo persona)
│
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── api.js
│   │   └── components/
│   │       ├── Sidebar.jsx
│   │       └── ChatBubble.jsx
│
├── screenshots/            # Project screenshots
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🧠 What Ask2Inbox Demonstrates

* Real-world **agentic architecture**
* Strict **chat–email parity**
* Intent-driven orchestration using LangGraph
* SQL-backed enterprise data access
* Safe side effects (email + DB writes)
* Full-stack AI system design
* Enterprise-focused UX and constraints

---

## 👤 Author

Built by **Rishi Kishore**
GitHub: [https://github.com/rishixq](https://github.com/rishixq)


