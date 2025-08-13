import React, { useState } from "react";
import axios from "axios";

function App() {
  const [messages, setMessages] = useState([{ sender: "agent", text: "Hi! Ask me a question about the database." 
    }]);
  const [input, setInput] = useState("");

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await axios.post("http://localhost:8000/query", { user_input: input }, { responseType: "blob" });

      const blob = new Blob([response.data], {
        type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = "query_result.xlsx";
      link.click();

      setMessages((prev) => [
        ...prev,
        { sender: "agent", text: "Your query has been processed. The file has been downloaded." },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { sender: "agent", text: "I couldn't process your request. Please try again." },
      ]);
    }

    setInput("");
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100vh", backgroundColor: "#181818", color: "#FFF" }}>
      <div style={{ flex: 1, padding: "20px", overflowY: "auto" }}>
        {messages.map((msg, index) => (
          <div key={index} style={{ display: "flex", justifyContent: msg.sender === "agent" ? "flex-start" : "flex-end" }}>
            <div style={{ maxWidth: "60%", padding: "10px", borderRadius: "10px", backgroundColor: msg.sender === "agent" ? "#252525" : "#00ADB5", color: msg.sender === "agent" ? "#FFF" : "#000" }}>
              {msg.text}
            </div>
          </div>
        ))}
      </div>
      <div style={{ padding: "10px", backgroundColor: "#1F1F1F" }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your question..."
          style={{ flex: 1, padding: "10px", borderRadius: "20px", border: "1px solid #444", backgroundColor: "#252525", color: "#FFF", marginRight: "10px" }}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
      </div>
    </div>
  );
}

export default App;
