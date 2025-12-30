import { useState } from "react";
import ChatBubble from "./components/ChatBubble";
import Sidebar from "./components/Sidebar";
import { login, chat } from "./api";

function App() {
  const [email, setEmail] = useState("");
  const [employeeCode, setEmployeeCode] = useState("");

  const [employeeProfile, setEmployeeProfile] = useState(null);
  const [messages, setMessages] = useState([
    { role: "ai", content: "👋 Welcome! Please log in to continue." }
  ]);

  const [input, setInput] = useState("");
  const [error, setError] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [emailNotice, setEmailNotice] = useState(false);


  // -----------------------
  // LOGIN
  // -----------------------
  const handleLogin = async () => {
    setError("");
    try {
      const profile = await login(employeeCode, email);
      console.log("LOGIN RESPONSE:", profile);
      setEmployeeProfile({
        ...profile,
        id: profile.id ?? profile.employee_id
      });

      setMessages([]);
    } catch (err) {
      setError("Invalid employee code or email. Try again");
    }
  };

  const handleLogout = () => {
    setEmployeeProfile(null);
    setEmployeeCode("");
    setEmail("");
    setMessages([
      { role: "ai", content: "👋 Welcome! Please log in to continue." }
    ]);
  };

  // -----------------------
  // CHAT (ASK2INBOX LOGIC)
  // -----------------------
  const sendMessage = async () => {
    if (!input.trim() || !employeeProfile) return;

    const userMsg = { role: "user", content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput("");

    try {
      setIsTyping(true);

      console.log("EMPLOYEE ID BEING SENT:", employeeProfile.id);


      const data = await chat(
        userMsg.content,
        Number(employeeProfile.id)   // ✅ ONLY employee_id
      );

      const aiMsg = {
        role: "ai",
        content: data.response   // ✅ backend contract
      };

      setMessages(prev => [...prev, aiMsg]);
      if (data.email_sent) {
        setEmailNotice(true);
        setTimeout(() => setEmailNotice(false), 3000);
      }
    } catch (err) {
      setMessages(prev => [
        ...prev,
        { role: "ai", content: "⚠️ Server is temporarily unavailable." }
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  // -----------------------
  // LOGIN UI (UNCHANGED)
  // -----------------------
  if (!employeeProfile) {
    return (
      <div className="h-screen flex items-center justify-center bg-gradient-to-br from-[#F3D6DA] to-[#7A1E2B]">
        <div className="bg-white/80 backdrop-blur-lg p-8 rounded-2xl shadow-xl w-96 border border-gray-200">

          <div className="flex items-center justify-center mb-6">
            <div className="h-12 w-12 rounded-xl bg-white flex items-center justify-center">
              <img
                src="https://i.pinimg.com/originals/45/53/e3/4553e37f5946db5c248e4a56bef77ab5.gif"
                alt="Ask2Inbox Logo"
                className="h-full w-full object-contain p-0.5"
              />
            </div>
          </div>

          <h2 className="text-2xl font-semibold text-center mb-1">
            Ask2Inbox
          </h2>
          <p className="text-sm text-gray-600 text-center mb-6">
            Ask once. Straight to inbox.
          </p>

          <input
            value={email}
            onChange={e => setEmail(e.target.value)}
            placeholder="Enter email (e.g. employee@company.com)"
            type="email"
            className="w-full border rounded-lg px-4 py-2 mb-3 text-xs focus:outline-none focus:ring-2 focus:ring-[#7A1E2B]/50"
          />

          <input
            value={employeeCode}
            onChange={e => setEmployeeCode(e.target.value)}
            placeholder="Enter Employee Code (e.g. EMP001)"
            className="w-full border rounded-lg px-4 py-2 mb-4 text-xs focus:outline-none focus:ring-2 focus:ring-[#7A1E2B]/50"
          />

          <button
            onClick={handleLogin}
            className="w-full bg-[#b83748] text-white py-2.5 rounded-lg hover:bg-[#9c081b] transition"
          >
            Login
          </button>

          {error && (
            <p className="text-red-500 text-sm mt-3 text-center">
              {error}
            </p>
          )}
        </div>
      </div>
    );
  }

  // -----------------------
  // MAIN APP UI (UNCHANGED)
  // -----------------------
  return (
  <div className="flex h-screen bg-[#FDF6F7]">

    <Sidebar
      employee={{
        name: employeeProfile.name,
        id: employeeProfile.employee_code,
        department: employeeProfile.department,
        role: employeeProfile.role,
        joined: employeeProfile.join_date,
      }}
      onLogout={handleLogout}
    />

    <main className="flex-1 flex flex-col">

      {/* CHAT AREA */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((m, i) => (
          <ChatBubble key={i} role={m.role} content={m.content} />
        ))}

        {isTyping && (
          <div className="text-sm text-[#7A1E2B] italic">
            🤖Echo is typing…
          </div>
        )}
      </div>

      {/* EMAIL SENT NOTICE */}
      {emailNotice && (
        <div
          className="
            mx-6 mb-2
            text-xs
            text-[#7A1E2B]
            bg-[#FCEBEC]
            border border-[#D14A5A]/40
            rounded-md
            px-3 py-1
            w-fit
          "
        >
          A copy has been sent to your registered email.
        </div>
      )}

      {/* INPUT BAR */}
      <div
        className="
          border-t
          border-[#E8B1B6]/60
          bg-[#FDF6F7]
          p-4
          flex gap-3
        "
      >
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === "Enter" && sendMessage()}
          placeholder="Ask Echo anything..."
          className="
            flex-1
            border border-[#D8A2A8]
            rounded-lg
            px-4 py-2
            text-sm
            focus:outline-none
            focus:ring-2
            focus:ring-[#D14A5A]/40
            bg-white
          "
        />

        <button
          onClick={sendMessage}
          className="
            bg-[#7A1E2B]
            text-white
            font-semibold
            border border-[#7A1E2B]
            hover:bg-[#8F2432]
            transition
            rounded-lg
            px-4 py-2
          "
        >
          Send
        </button>
      </div>

    </main>
  </div>
);

}

export default App;
