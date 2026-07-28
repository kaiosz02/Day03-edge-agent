"use client";
import React, { useState, useRef, useEffect } from 'react';
import ChatMessage, { MessageProps } from '../components/ChatMessage';

interface ChatSession {
  id: string;
  title: string;
  messages: MessageProps[];
}

export default function ChatApp() {
  const [sessions, setSessions] = useState<ChatSession[]>([
    {
      id: "session-1",
      title: "Tư vấn khoá học",
      messages: [
        {
          id: "1",
          role: "bot",
          content: "Xin chào! Tôi là trợ lý AI (ReAct Agent). Tôi có thể tư vấn các khoá học IELTS/TOEIC cho bạn.",
        }
      ]
    }
  ]);
  const [activeSessionId, setActiveSessionId] = useState<string>("session-1");
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const activeSession = sessions.find(s => s.id === activeSessionId) || sessions[0];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [activeSession.messages, isTyping]);

  const handleNewChat = () => {
    const newSession: ChatSession = {
      id: `session-${Date.now()}`,
      title: "Hội thoại mới",
      messages: [
        {
          id: "1",
          role: "bot",
          content: "Xin chào! Bạn cần tư vấn điều gì hôm nay?",
        }
      ]
    };
    setSessions([newSession, ...sessions]);
    setActiveSessionId(newSession.id);
  };

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isTyping) return;

    const userQuery = input.trim();
    const userMsg: MessageProps = {
      id: Date.now().toString(),
      role: "user",
      content: userQuery,
    };

    setSessions(prev => prev.map(s => {
      if (s.id === activeSessionId) {
        const newTitle = s.title === "Hội thoại mới" ? userQuery.slice(0, 25) + "..." : s.title;
        return { ...s, title: newTitle, messages: [...s.messages, userMsg] };
      }
      return s;
    }));
    setInput("");
    setIsTyping(true);

    try {
      const history = activeSession.messages.filter(m => m.id !== "1").map(m => ({
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
      
      setSessions(prev => prev.map(s => 
        s.id === activeSessionId ? { ...s, messages: [...s.messages, botMsg] } : s
      ));
    } catch (error) {
      console.error(error);
      const errorMsg: MessageProps = {
        id: (Date.now() + 1).toString(),
        role: "bot",
        content: "Xin lỗi, không thể kết nối tới máy chủ AI lúc này."
      };
      setSessions(prev => prev.map(s => 
        s.id === activeSessionId ? { ...s, messages: [...s.messages, errorMsg] } : s
      ));
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="app-container">
      {/* Sidebar for Chat History */}
      <aside className="sidebar glass-panel">
        <button className="new-chat-btn" onClick={handleNewChat}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
          Hội thoại mới
        </button>
        <div className="sessions-list">
          {sessions.map(session => (
            <div 
              key={session.id} 
              className={`session-item ${session.id === activeSessionId ? 'active' : ''}`}
              onClick={() => setActiveSessionId(session.id)}
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
              </svg>
              <span className="session-title">{session.title}</span>
            </div>
          ))}
        </div>
      </aside>

      {/* Main Chat Area */}
      <main className="main-chat">
        <header className="app-header glass-panel">
          <h1>AI Assistant</h1>
          <div className="status-indicator">
            <span className="status-dot"></span>
            Online
          </div>
        </header>

        <div className="chat-container">
          <div className="messages-area">
            {activeSession.messages.map(msg => (
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
        </div>

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
      </main>
    </div>
  );
}
