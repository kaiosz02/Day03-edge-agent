"use client";
import React, { useState, useRef, useEffect } from 'react';
import ChatMessage, { MessageProps } from '../components/ChatMessage';

export default function ChatApp() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<MessageProps[]>([
    {
      id: "1",
      role: "bot",
      content: "Xin chào! Tôi là trợ lý AI (ReAct Agent). Tôi có thể tư vấn các khoá học IELTS/TOEIC cho bạn.",
    }
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userQuery = input.trim();
    const userMsg: MessageProps = {
      id: Date.now().toString(),
      role: "user",
      content: userQuery,
    };

    setMessages(prev => [...prev, userMsg]);
    setInput("");
    setIsTyping(true);

    try {
      // Build history excluding the "typing" mock or the first static welcome message if needed.
      // But passing all user and bot messages is fine.
      const history = messages.filter(m => m.id !== "1").map(m => ({
        role: m.role,
        content: m.content
      }));

      const response = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: userQuery, history })
      });
      
      const data = await response.json();
      
      const botMsg: MessageProps = {
        id: (Date.now() + 1).toString(),
        role: "bot",
        content: data.answer || "Lỗi khi lấy câu trả lời.",
        thoughts: data.thoughts || []
      };
      
      setMessages(prev => [...prev, botMsg]);
    } catch (error) {
      console.error(error);
      const errorMsg: MessageProps = {
        id: (Date.now() + 1).toString(),
        role: "bot",
        content: "Xin lỗi, không thể kết nối tới máy chủ AI lúc này."
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header glass-panel">
        <h1>AI Assistant</h1>
        <div className="status-indicator">
          <span className="status-dot"></span>
          Online
        </div>
      </header>

      <main className="chat-container">
        <div className="messages-area">
          {messages.map(msg => (
            <ChatMessage key={msg.id} {...msg} />
          ))}
          {isTyping && (
            <div className="typing-indicator glass-panel">
              <span className="dot"></span>
              <span className="dot"></span>
              <span className="dot"></span>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </main>

      <footer className="app-footer">
        <form onSubmit={handleSend} className="input-form glass-panel">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Nhập câu hỏi..."
            className="chat-input"
          />
          <button type="submit" className="send-btn" disabled={!input.trim() || isTyping}>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        </form>
      </footer>
    </div>
  );
}
