
```md
# 📬 **Ask2Inbox — Ask Once. Straight to Inbox.**

**FastAPI · LangGraph · SQLAlchemy · Groq LLM · React**

**Ask2Inbox** is a **production-grade, agentic Employee Self-Service (ESS) platform** that allows employees to **ask questions once** and receive **identical, enterprise-ready responses** in both **chat and email**.

The system is built around a **single LLM source of truth**, ensuring **strict chat–email parity** — a critical requirement in real-world enterprise systems.

---

## 🌍 Deployed Site
👉 *(https://ask2inbox.yourdomain.com)*

---

## 🎥 Demo Video

▶️ **Watch the full working demo:**  
👉 *(https://youtu.be/your-demo-link)*

---

## 📸 Screenshots

<img width="1900" alt="Ask2Inbox Login" src="screenshots/login.png" />
<img width="1900" alt="Ask2Inbox Chat" src="screenshots/chat.png" />
<img width="1900" alt="Ask2Inbox Email" src="screenshots/email.png" />


---

## ✨ Key Capabilities

### 🧠 Intelligent Agentic Chat
- Handles **general and out-of-the-box questions**
- Maintains a **professional, modern enterprise tone**
- Responds safely using authenticated employee context

---

### 🗄️ SQL-Backed Employee Queries
- Reads structured employee data from SQL:
  - Profile
  - Salary
  - Leave balance & history
  - Skills
  - Assets
  - Goals
- No ORM objects leak beyond the service layer
- JSON-safe, serialized data only

---

### 📧 Chat–Email Parity (Core Feature)
- Email responses are generated **entirely by the LLM**
- **Same output** is:
  - Displayed in chat
  - Sent via email
- No formatting layers
- No template duplication
- Email is treated as a **delivery channel**, not a renderer

---

### 🔁 Agentic Decision-Making
The system automatically determines:
- Chat-only response
- Database read
- Database read + email
- Database write (leave application)

This mirrors **real internal enterprise assistants**, not demo bots.

---

## 🧱 Tech Stack

### Backend
- Python
- FastAPI
- LangGraph
- SQLAlchemy
- PostgreSQL
- SMTP (Email delivery)

### LLM
- Groq
- Model: `llama-3.1-8b-instant`

### Frontend
- React
- Tailwind CSS
- Custom chat UI
- Branded Ask2Inbox theme
- UI-level email delivery notifications

---


## ⚙️ How to Run Locally

### Backend
```bash
# Activate virtual environment
.venv\Scripts\activate

# Run backend
uvicorn main:app --reload
````

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

## 🎯 Why Ask2Inbox Matters

* Demonstrates **true agentic architecture**
* Enforces **chat–email parity**, a real enterprise constraint
* Clean separation of concerns
* Real side effects (SQL + Email)
* Fully explainable in interviews
* Production-style system, not a demo chatbot

---

## 👤 Author

Built by **Rishi Kishore**

GitHub: [https://github.com/rishixq](https://github.com/rishixq)


> **Ask once. Straight to inbox.**

