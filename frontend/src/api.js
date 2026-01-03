const API_BASE_URL =
  process.env.REACT_APP_API_BASE_URL || "https://ask2inbox.onrender.com/";

/**
 * LOGIN API
 * --------------------
 * Calls backend /login
 * Returns employeeProfile
 */
export async function login(employeeCode, email) {
  const response = await fetch(`${API_BASE_URL}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      employee_code: employeeCode,
      email: email,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Login failed");
  }

  return response.json();
}

/**
 * CHAT API
 * --------------------
 * Sends message + employee_id to agent backend
 */
export async function chat(message, employeeId) {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message: message,
      employee_id: Number(employeeId),
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Chat request failed");
  }

  return response.json();
}
