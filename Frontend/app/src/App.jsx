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
  Sun,
  Moon,
  Sparkles,
  MessageCircle,
  HelpCircle
} from 'lucide-react';

const App = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [role, setRole] = useState('employee');
  const [darkMode, setDarkMode] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Apply dark mode to HTML element
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  // Auto-scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Welcome message
  useEffect(() => {
    setMessages([
      {
        id: 'welcome',
        type: 'bot',
        content: `## 🇰🇪 Welcome to the Kenya Employment Act Assistant!

I'm here to help you understand your rights and obligations under the **Employment Act 2007 (Chapter 226)**.

### Current Mode: **${role === 'employee' ? 'Employee Mode 👥' : 'Employer Mode 💼'}**

${role === 'employee' 
  ? `### 🔹 What I can help you with:
- **Leave entitlements** (annual, maternity, paternity, sick leave)
- **Termination & dismissal** rules
- **Discrimination** protections
- **Wage payment** regulations
- **Housing & medical** benefits
- How to **file complaints**

### 💡 Try asking:
- "How much annual leave am I entitled to?"
- "Can my employer terminate me without notice?"
- "What is the maternity leave policy?"`

  : `### 🔹 What I can help you with:
- **Contract requirements** (written contracts, particulars)
- **Record keeping** obligations
- **Proper termination** procedures
- **Legal deductions** from wages
- **Health & safety** requirements
- **Compliance & penalties**

### 💡 Try asking:
- "What records must I keep for employees?"
- "How do I properly terminate an employee?"
- "What are the requirements for a valid contract?"`

}

How can I assist you today?`,
        timestamp: new Date()
      }
    ]);
  }, []);

  // Update when role changes (add system message)
  useEffect(() => {
    if (messages.length > 0 && messages[0].id === 'welcome') {
      const systemMessage = {
        id: `system-${Date.now()}`,
        type: 'system',
        content: `🔄 Switched to **${role === 'employee' ? 'Employee Mode' : 'Employer Mode'}**`,
        timestamp: new Date()
      };
      setMessages(prev => [prev[0], systemMessage, ...prev.slice(1)]);
    }
  }, [role]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post('/api/ask', {
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
      console.error('Error:', error);
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: `❌ **Sorry, I encountered an error**

Please make sure:
1. The backend server is running on port 8000
2. Your OpenAI API key is set in the backend

Error details: ${error.message}`,
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
        content: `🇰🇪 **Chat cleared!** I'm back in ${role === 'employee' ? 'Employee Mode' : 'Employer Mode'}.

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

  return (
    <div className="min-h-screen bg-gradient-kenya">
      {/* Header */}
      <header className="sticky top-0 z-10 bg-white/95 dark:bg-gray-900/95 backdrop-blur-md border-b border-gray-200 dark:border-gray-700 shadow-sm">
        <div className="max-w-5xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-gradient-to-br from-green-600 to-red-600 p-2.5 rounded-xl shadow-lg">
                <Scale className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold bg-gradient-to-r from-green-700 to-red-700 dark:from-green-400 dark:to-red-400 bg-clip-text text-transparent">
                  Kenya Employment Act 2007
                </h1>
                <p className="text-xs text-gray-500 dark:text-gray-400 flex items-center gap-1">
                  <Sparkles className="w-3 h-3" />
                  Know Your Rights • Fahamu Haki Zako
                </p>
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <button
                onClick={() => setDarkMode(!darkMode)}
                className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                aria-label="Toggle dark mode"
              >
                {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
              </button>
              
              <button
                onClick={clearChat}
                className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                aria-label="Clear chat"
              >
                <Trash2 className="w-5 h-5" />
              </button>
            </div>
          </div>
          
          {/* Role Switcher */}
          <div className="flex gap-2 mt-4">
            <button
              onClick={() => setRole('employee')}
              className={`flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl font-medium transition-all ${
                role === 'employee'
                  ? 'bg-green-600 text-white shadow-lg shadow-green-200 dark:shadow-none'
                  : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700'
              }`}
            >
              <Users className="w-4 h-4" />
              <span>Employee Mode</span>
              <span className="text-xs opacity-80">Know Your Rights</span>
            </button>
            
            <button
              onClick={() => setRole('employer')}
              className={`flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl font-medium transition-all ${
                role === 'employer'
                  ? 'bg-red-600 text-white shadow-lg shadow-red-200 dark:shadow-none'
                  : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700'
              }`}
            >
              <Briefcase className="w-4 h-4" />
              <span>Employer Mode</span>
              <span className="text-xs opacity-80">Understand Obligations</span>
            </button>
          </div>
        </div>
      </header>
      
      {/* Messages Area */}
      <main className="max-w-5xl mx-auto px-4 py-6">
        <div className="space-y-4 pb-36">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`animate-slide-up ${
                message.type === 'user' 
                  ? 'flex justify-end' 
                  : message.type === 'system'
                  ? 'flex justify-center'
                  : 'flex justify-start'
              }`}
            >
              {message.type === 'system' ? (
                <div className="px-4 py-2 bg-gray-100 dark:bg-gray-800 rounded-full text-sm text-gray-600 dark:text-gray-400">
                  {message.content}
                </div>
              ) : (
                <div className={`flex max-w-[85%] gap-3 ${
                  message.type === 'user' ? 'flex-row-reverse' : 'flex-row'
                }`}>
                  {/* Avatar */}
                  <div className={`flex-shrink-0 w-9 h-9 rounded-full flex items-center justify-center ${
                    message.type === 'user' 
                      ? 'bg-gradient-to-br from-green-500 to-green-600' 
                      : 'bg-gradient-to-br from-red-500 to-red-600'
                  }`}>
                    {message.type === 'user' 
                      ? <User className="w-4 h-4 text-white" />
                      : <Bot className="w-4 h-4 text-white" />
                    }
                  </div>
                  
                  {/* Message Content */}
                  <div className={`rounded-2xl px-5 py-3 ${
                    message.type === 'user'
                      ? 'bg-gradient-to-br from-green-600 to-green-700 text-white'
                      : 'bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200 shadow-md border border-gray-100 dark:border-gray-700'
                  }`}>
                    <div className="prose prose-sm dark:prose-invert max-w-none">
                      <ReactMarkdown
                        components={{
                          h1: ({ children }) => <h1 className="text-lg font-bold mb-2">{children}</h1>,
                          h2: ({ children }) => <h2 className="text-md font-semibold mb-2 mt-3 first:mt-0">{children}</h2>,
                          h3: ({ children }) => <h3 className="text-sm font-semibold mb-1 mt-2">{children}</h3>,
                          p: ({ children }) => <p className="mb-2 leading-relaxed">{children}</p>,
                          strong: ({ children }) => <strong className="font-bold text-green-600 dark:text-green-400">{children}</strong>,
                          ul: ({ children }) => <ul className="list-disc ml-4 mb-2 space-y-1">{children}</ul>,
                          li: ({ children }) => <li className="text-sm">{children}</li>,
                          code: ({ children }) => <code className="bg-gray-100 dark:bg-gray-700 px-1 py-0.5 rounded text-sm">{children}</code>,
                        }}
                      >
                        {message.content}
                      </ReactMarkdown>
                    </div>
                    
                    {/* Sources */}
                    {message.sources && message.sources.length > 0 && (
                      <div className="mt-3 pt-2 border-t border-gray-200 dark:border-gray-700">
                        <p className="text-xs text-gray-500 dark:text-gray-400 flex items-center gap-1">
                          <BookOpen className="w-3 h-3" />
                          Sources: {message.sources.map(s => s.section).filter(s => s !== 'Unknown').join(', ')}
                        </p>
                      </div>
                    )}
                    
                    <p className="text-xs text-gray-400 dark:text-gray-500 mt-2">
                      {message.timestamp.toLocaleTimeString()}
                    </p>
                  </div>
                </div>
              )}
            </div>
          ))}
          
          {loading && (
            <div className="flex justify-start animate-slide-up">
              <div className="flex gap-3">
                <div className="w-9 h-9 rounded-full bg-gradient-to-br from-red-500 to-red-600 flex items-center justify-center">
                  <Bot className="w-4 h-4 text-white" />
                </div>
                <div className="bg-white dark:bg-gray-800 rounded-2xl px-5 py-3 shadow-md">
                  <Loader2 className="w-5 h-5 animate-spin text-green-600" />
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
      </main>
      
      {/* Suggested Questions */}
      <div className="fixed bottom-28 left-0 right-0 max-w-5xl mx-auto px-4 z-10">
        <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-thin">
          {suggestedQuestions.map((q, idx) => (
            <button
              key={idx}
              onClick={() => setInput(q)}
              className="flex-shrink-0 px-4 py-2 text-sm bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-full hover:border-green-500 dark:hover:border-green-500 hover:bg-green-50 dark:hover:bg-green-900/20 transition-all shadow-sm hover:shadow-md"
            >
              <HelpCircle className="w-3 h-3 inline mr-1" />
              {q}
            </button>
          ))}
        </div>
      </div>
      
      {/* Input Area */}
      <footer className="fixed bottom-0 left-0 right-0 bg-white/95 dark:bg-gray-900/95 backdrop-blur-md border-t border-gray-200 dark:border-gray-700 shadow-lg">
        <div className="max-w-5xl mx-auto px-4 py-4">
          <div className="flex gap-3 items-end">
            <div className="flex-1 relative">
              <textarea
                ref={inputRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type your question here... Press Enter to send"
                className="w-full px-4 py-3 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none text-gray-800 dark:text-gray-200"
                rows="1"
                style={{ minHeight: '48px', maxHeight: '120px' }}
                onInput={(e) => {
                  e.target.style.height = 'auto';
                  e.target.style.height = Math.min(e.target.scrollHeight, 120) + 'px';
                }}
              />
            </div>
            
            <button
              onClick={sendMessage}
              disabled={!input.trim() || loading}
              className="p-3 bg-gradient-to-r from-green-600 to-green-700 text-white rounded-xl hover:from-green-700 hover:to-green-800 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
          
          <p className="text-xs text-center text-gray-500 dark:text-gray-400 mt-3 flex items-center justify-center gap-1">
            <Scale className="w-3 h-3" />
            Powered by the Kenya Employment Act 2007 (Chapter 226)
            <span className="mx-1">•</span>
            AI-assisted legal information
            <span className="mx-1">•</span>
            Not a substitute for legal advice
          </p>
        </div>
      </footer>
    </div>
  );
};

export default App;