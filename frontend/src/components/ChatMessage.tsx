import React, { useState } from 'react';

export interface MessageProps {
  id: string;
  role: "user" | "bot";
  content: string;
  thoughts?: string[];
}

export default function ChatMessage({ role, content, thoughts }: MessageProps) {
  const [showThoughts, setShowThoughts] = useState(false);
  const isBot = role === "bot";

  return (
    <div className={`msg-wrapper ${role}`}>
      <div className={`avatar ${role}`}>
        {isBot ? "AI" : "U"}
      </div>
      <div className="msg-content">
        {isBot && thoughts && thoughts.length > 0 && (
          <div className="thoughts-container">
            <button 
              className={`thoughts-toggle ${showThoughts ? 'open' : ''}`}
              onClick={() => setShowThoughts(!showThoughts)}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M12 2a10 10 0 100 20 10 10 0 000-20zM12 8v4l3 3" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                <span>Thought Process ({thoughts.length} steps)</span>
              </div>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M19 9l-7 7-7-7" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
            <div className={`thoughts-content ${showThoughts ? 'open' : ''}`}>
              {thoughts.map((thought, idx) => (
                <div key={idx} className="thought-step">
                  <div className="step-indicator">
                    <div className="step-dot"></div>
                    <div className="step-line"></div>
                  </div>
                  <div className="step-text">{thought}</div>
                </div>
              ))}
            </div>
          </div>
        )}
        <div className="msg-bubble glass-panel">
          {content}
        </div>
      </div>
    </div>
  );
}
