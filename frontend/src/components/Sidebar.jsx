// src/components/Sidebar.jsx

import React from "react";

const Sidebar = ({ employee, onLogout }) => {
  return (
    <aside className="w-72 h-screen bg-gradient-to-b from-[#4B0F1C] to-[#2A070D]
 text-white font-bold mt-3 flex flex-col px-6 py-5">
      
      {/* Logo */}
      <div className="flex items-center gap-3 mb-8">
        <div className="h-10 w-10 rounded-xl bg-white flex items-center justify-center overflow-hidden">

          <img
            src="https://i.pinimg.com/originals/45/53/e3/4553e37f5946db5c248e4a56bef77ab5.gif"
            alt="Ask2Inbox Logo"
            className="h-full w-full object-contain p-1"
          />
        </div>
        <div>
          <h1 className="text-lg font-bold">Ask2Inbox</h1>
          <p className="text-xs text-[#FFD6DA] font-semibold space-y-1">
            Ask once. Straight to inbox.
          </p>
        </div>
      </div>

      <div className="border-b border-gray-800 mb-6" />

      {/* Employee Card */}
      <div className="bg-gradient-to-br from-[#4A1422] to-[#2A070D]
    border border-[#B23A48]/60
    shadow-[0_0_25px_rgba(178,58,72,0.25)]
    rounded-xl
    p-4 mb-6">
        <div className="flex items-center gap-2 mb-3">
          <div className="h-8 w-8 rounded-full bg-black flex items-center justify-center text-sm">
            👤
          </div>
          <h2 className="text-sm text-white font-bold">
            {employee.name}
          </h2>
        </div>

        <div className="text-xs text-gray-300 font-semibold mt-3 space-y-1">
          <p>
            <span className="text-sm text-white font-bold">ID:</span>{" "}
            {employee.id}
          </p>
          <p>
            <span className="text-sm text-white font-bold">Department:</span>{" "}
            {employee.department}
          </p>
          <p>
            <span className="text-sm text-white font-bold">Role:</span>{" "}
            {employee.role}
          </p>
          <p>
            <span className="text-sm text-white font-bold">Joined:</span>{" "}
            {employee.joined}
          </p>
        </div>
      </div>

      {/* Logout */}
      <button
  onClick={onLogout}
  className="
    w-full
    mt-2
    flex items-center justify-center gap-2
    text-sm font-semibold
    text-[#FFD6DA]
    border border-[#D14A5A]/70
    rounded-lg py-2
    shadow-[0_0_15px_rgba(209,74,90,0.25)]
    hover:bg-[#D14A5A]/30
    hover:text-white
    transition
  "
>
  Logout
</button>


    </aside>
  );
};

export default Sidebar;
