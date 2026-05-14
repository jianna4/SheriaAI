import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { 
  Send, 
  Bot, 
  User, 
  Briefcase, 
  Users, 
  Scale, 
  BookOpen,
  Loader2,
  Trash2,
  Sparkles,
  HelpCircle
} from 'lucide-react';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

const App = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [role, setRole] = useState('employee');
  const [backendStatus, setBackendStatus] = useState('checking');
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const textareaRef = useRef(null);

  useEffect(() => {
    const checkBackend = async () => {
      try {
        await api.get('/health');
        setBackendStatus('connected');
      } catch (error) {
        setBackendStatus('disconnected');
      }
    };
    checkBackend();
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    setMessages([
      {
        id: 'welcome',
        type: 'bot',
        content: `## Welcome to the Kenya Employment Act Assistant

I am here to help you understand your rights and obligations under the **Employment Act 2007 (Chapter 226)**.

### Current Mode: **${role === 'employee' ? 'Employee Mode' : 'Employer Mode'}**

${role === 'employee' 
  ? `**What I can help you with:**
- Leave entitlements (annual, maternity, paternity, sick leave)
- Termination and dismissal rules
- Discrimination protections
- Wage payment regulations
- Housing and medical benefits
- How to file complaints

**Try asking:**
- "How much annual leave am I entitled to?"
- "Can my employer terminate me without notice?"
- "What is the maternity leave policy?"`

  : `**What I can help you with:**
- Contract requirements (written contracts, particulars)
- Record keeping obligations
- Proper termination procedures
- Legal deductions from wages
- Health and safety requirements
- Compliance and penalties

**Try asking:**
- "What records must I keep for employees?"
- "How do I properly terminate an employee?"
- "What are the requirements for a valid contract?"`}

How can I assist you today?`,
        timestamp: new Date()
      }
    ]);
  }, []);

  useEffect(() => {
    if (messages.length > 1 && messages[0].id === 'welcome') {
      const systemMessage = {
        id: `system-${Date.now()}`,
        type: 'system',
        content: `Switched to ${role === 'employee' ? 'Employee Mode' : 'Employer Mode'}`,
        timestamp: new Date()
      };
      setMessages(prev => [prev[0], systemMessage, ...prev.slice(1)]);
    }
  }, [role]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    if (backendStatus !== 'connected') {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: `**Backend not connected**

Please make sure:
1. The backend server is running
2. Your environment variables are correct
3. The backend URL is accessible

Current backend URL: ${API_BASE_URL}

Check the browser console for more details.`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
      return;
    }

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
    setLoading(true);

    try {
      const response = await api.post('/ask', {
        query: input,
        role: role
      });

      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: response.data.answer,
        sources: response.data.sources,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error details:', error.response?.data || error.message);
      
      let errorContent = `**Sorry, I encountered an error**\n\n`;
      
      if (error.response) {
        errorContent += `Status: ${error.response.status}\n`;
        errorContent += `Details: ${error.response.data?.detail || error.message}\n\n`;
      } else if (error.request) {
        errorContent += `Cannot reach backend server\n\n`;
        errorContent += `Backend URL: ${API_BASE_URL}\n\n`;
        errorContent += `Please verify:\n`;
        errorContent += `1. The backend is deployed and running\n`;
        errorContent += `2. Your VITE_API_URL is correct\n`;
        errorContent += `3. CORS is properly configured on the backend\n`;
      } else {
        errorContent += `Error: ${error.message}\n`;
      }
      
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: errorContent,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([
      {
        id: 'welcome',
        type: 'bot',
        content: `**Chat cleared** I am back in ${role === 'employee' ? 'Employee Mode' : 'Employer Mode'}.

How can I help you today?`,
        timestamp: new Date()
      }
    ]);
  };

  const suggestedQuestions = role === 'employee' 
    ? [
        "How much annual leave am I entitled to?",
        "What are the rules for maternity leave?",
        "Can I be fired without notice?",
        "What is unfair termination?",
        "How do I report a complaint?"
      ]
    : [
        "What records must I keep for employees?",
        "How do I properly terminate an employee?",
        "What are the requirements for a written contract?",
        "What deductions can I make from wages?",
        "What are the penalties for non-compliance?"
      ];

  const adjustTextareaHeight = (e) => {
    e.target.style.height = 'auto';
    e.target.style.height = Math.min(e.target.scrollHeight, 120) + 'px';
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-container">
          <div className="header-left">
            <div className="logo">
              <Scale size={28} />
            </div>
            <div className="title-section">
              <h1>Kenya Employment Act 2007</h1>
              <p>Chapter 226 | Know Your Rights</p>
            </div>
          </div>
          
          <div className="header-right">
            <div className={`status ${backendStatus}`}>
              <span className="status-dot"></span>
              <span>{backendStatus === 'connected' ? 'Connected' : 'Disconnected'}</span>
            </div>
            <button onClick={clearChat} className="clear-button" title="Clear chat">
              <Trash2 size={18} />
            </button>
          </div>
        </div>
        
        {/* Role Buttons */}
        <div className="role-container">
          <button
            onClick={() => setRole('employee')}
            className={`role-button employee ${role === 'employee' ? 'active' : ''}`}
          >
            <Users size={18} />
            <span>Employee Mode</span>
            <span className="role-badge">Know Your Rights</span>
          </button>
          
          <button
            onClick={() => setRole('employer')}
            className={`role-button employer ${role === 'employer' ? 'active' : ''}`}
          >
            <Briefcase size={18} />
            <span>Employer Mode</span>
            <span className="role-badge">Understand Obligations</span>
          </button>
        </div>
      </header>
      
      {/* Messages */}
      <main className="messages">
        <div className="messages-container">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`message-row ${message.type}`}
            >
              {message.type === 'system' ? (
                <div className="system-message">
                  {message.content}
                </div>
              ) : (
                <div className={`message ${message.type}`}>
                  <div className="message-avatar">
                    {message.type === 'user' ? <User size={18} /> : <Bot size={18} />}
                  </div>
                  <div className="message-body">
                    <div className="message-content">
                      <ReactMarkdown
                        components={{
                          h1: ({ children }) => <h1>{children}</h1>,
                          h2: ({ children }) => <h2>{children}</h2>,
                          h3: ({ children }) => <h3>{children}</h3>,
                          p: ({ children }) => <p>{children}</p>,
                          strong: ({ children }) => <strong>{children}</strong>,
                          ul: ({ children }) => <ul>{children}</ul>,
                          li: ({ children }) => <li>{children}</li>,
                          code: ({ children }) => <code>{children}</code>,
                        }}
                      >
                        {message.content}
                      </ReactMarkdown>
                    </div>
                    
                    {message.sources && message.sources.length > 0 && (
                      <div className="message-sources">
                        <BookOpen size={12} />
                        <span>Sources: {message.sources.map(s => s.section).filter(s => s !== 'Unknown').join(', ')}</span>
                      </div>
                    )}
                    
                    <div className="message-time">
                      {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </div>
                  </div>
                </div>
              )}
            </div>
          ))}
          
          {loading && (
            <div className="message-row bot">
              <div className="message bot">
                <div className="message-avatar">
                  <Bot size={18} />
                </div>
                <div className="message-body">
                  <div className="message-content loading">
                    <Loader2 className="spinner" />
                    <span>Thinking...</span>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
      </main>
      
      {/* Suggestions */}
      <div className="suggestions">
        <div className="suggestions-scroll">
          {suggestedQuestions.map((q, idx) => (
            <button
              key={idx}
              onClick={() => setInput(q)}
              className="suggestion-button"
            >
              <HelpCircle size={14} />
              <span>{q}</span>
            </button>
          ))}
        </div>
      </div>
      
      {/* Input */}
      <footer className="input-footer">
        <div className="input-container">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => {
              setInput(e.target.value);
              adjustTextareaHeight(e);
            }}
            onKeyDown={handleKeyPress}
            placeholder="Type your question here... Press Enter to send"
            rows="1"
          />
          
          <button
            onClick={sendMessage}
            disabled={!input.trim() || loading}
            className="send-button"
          >
            <Send size={18} />
          </button>
        </div>
        
        <div className="footer-note">
          <Scale size={12} />
          <span>Powered by the Kenya Employment Act 2007 (Chapter 226)</span>
          <span className="separator">|</span>
          <span>AI-assisted legal information</span>
          <span className="separator">|</span>
          <span>Not a substitute for legal advice</span>
        </div>
      </footer>
    </div>
  );
};

export default App;