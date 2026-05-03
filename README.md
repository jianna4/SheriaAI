# 🇰🇪 Kenya Employment Act 2007 - AI Legal Assistant

<div align="center">

![Kenya Employment Act](https://img.shields.io/badge/Kenya-Employment%20Act%202007-red)
![RAG](https://img.shields.io/badge/RAG-Powered-green)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/Python-3.11-yellow)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-teal)

**Empowering Kenyan Workers & Employers with AI-Powered Legal Understanding**

[🌟 Features](#-features) • [🚀 Quick Start](#-quick-start) • [📖 About](#-about-the-kenya-employment-act) • [🛠️ Tech Stack](#️-tech-stack) • [📱 Coming Soon](#-coming-soon)

</div>

---

## 📋 Overview

The **Kenya Employment Act AI Assistant** is an intelligent, RAG (Retrieval-Augmented Generation) powered chatbot that helps Kenyans understand their rights and obligations under the **Employment Act 2007 (Chapter 226 of the Laws of Kenya)**.

Whether you're an **employee** wanting to know your rights or an **employer** needing to understand your legal obligations, this assistant provides accurate, context-aware answers with direct citations from the actual law.

### 🎯 Purpose

In Kenya, many workers and small business owners struggle to understand complex legal language. This tool bridges that gap by:
- **Simplifying** legal jargon into clear, practical advice
- **Providing** specific section citations for verification
- **Offering** role-specific guidance (employee vs employer perspectives)
- **Making** legal information accessible 24/7, completely free

---

## ✨ Features

### 🤖 Dual-Mode Assistant

| Mode | Focus | Key Topics |
|------|-------|------------|
| **👥 Employee Mode** | Know Your Rights | Leave entitlements, termination protections, discrimination, wage payment, complaint filing |
| **💼 Employer Mode** | Understand Obligations | Written contracts, record keeping, proper termination procedures, legal deductions, compliance |

### 📚 Powered by the Actual Law

- **203 intelligent chunks** from the complete Employment Act 2007
- **Section-by-section** analysis and retrieval
- **Direct citations** with page numbers for verification
- **Up-to-date** with Revised Edition 2012

### 💬 Interactive Features

- 💡 **Suggested questions** to help you get started
- 🌙 **Dark mode** for comfortable reading
- 📱 **Mobile-responsive** design
- 🔗 **Source attribution** for every answer
- ✨ **Real-time streaming** responses

### 🔒 Privacy First

- No conversation history stored
- No personal data collected
- Direct API calls only for query processing

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- OpenRouter API key (or OpenAI API key)
- Git

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/jianna4/SheriaAI.git
cd kenya-employment-act-rag/Backend

# Create virtual environment
python -m venv venv
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
echo "OPENAI_API_KEY=your-key-here" > .env
echo "OPENAI_BASE_URL=https://openrouter.ai/api/v1" >> .env

# Create vector database (first time only)
python embedding.py

# Run the API server
uvicorn main:app --reload --port 8000
```

### Frontend Setup

```bash
# Open a new terminal
cd ../Frontend

# Install dependencies
npm install

# Set up environment variables
echo "VITE_API_URL=http://localhost:8000" > .env

# Run development server
npm run dev
```

Visit http://localhost:5173 to start using the assistant!

---

## 📖 About the Kenya Employment Act

### Historical Context

| Aspect | Details |
|--------|--------|
| Act No. | Chapter 226 |
| Date of Assent | 22nd October, 2007 |
| Date of Commencement | 2nd June, 2008 |
| Revised Edition | 2012 |
| Purpose | To declare and define fundamental rights of employees, provide basic conditions of employment, regulate child employment |

### Key Parts of the Act

The Employment Act 2007 is organized into 13 main parts:

<details>
<summary><strong>Click to view all parts</strong></summary>

Part	Title	Key Sections
I	Preliminary	Short title, interpretation, application
II	General Principles	Forced labour prohibition, discrimination, sexual harassment
III	Employment Relationship	Contracts, employment particulars, disciplinary rules
IV	Protection of Wages	Payment rules, deductions, itemized pay statements
V	Rights & Duties	Leave entitlements, housing, water, food, medical attention
VI	Termination & Dismissal	Notice periods, redundancy, unfair termination, remedies
VII	Protection of Children	Child labour prohibition, medical examination, penalties
VIII	Insolvency of Employer	Employee protection when employer becomes insolvent
IX	Employment Records	Record keeping requirements, false entries penalties
X	Employment Management	Vacancy notifications, employee registers
XI	Foreign Contracts	Contracts for work outside Kenya
XII	Dispute Settlement	Complaint procedures, jurisdiction
XIII	Miscellaneous	Rules, repeals, transitional provisions

</details>

### Important Statistics

📄 203 chunks processed for accurate retrieval  
📖 71 pages of legal content analyzed  
⚖️ 93 sections covered  
📜 6 subsidiary rules included  

---

## 🛠️ Tech Stack

### Backend Technology

| Technology | Purpose |
|-----------|--------|
| FastAPI | High-performance API framework |
| LangChain | RAG orchestration & document processing |
| ChromaDB | Vector database for semantic search |
| OpenRouter | LLM API (GPT-3.5-turbo via open-source proxy) |
| PyMuPDF | PDF text extraction |
| Uvicorn | ASGI server |

### Frontend Technology

| Technology | Purpose |
|-----------|--------|
| React 18 | UI framework |
| Vite | Build tool & dev server |
| TailwindCSS | Styling |
| Axios | API client |
| ReactMarkdown | Markdown rendering |
| Lucide React | Icons |

### Deployment

| Platform | Component | URL |
|---------|----------|-----|
| Render | Backend API | kenya-employment-api.onrender.com |
| Vercel | Frontend App | [Your Vercel URL] |

---

## 📱 Coming Soon

### WhatsApp Integration

Planned features:

📲 Send a message to a WhatsApp number, get instant legal answers  
🔗 Share sections via WhatsApp with friends and family  
🗣️ Voice messages support (send voice note, get text response)  
📞 USSD fallback for feature phones  
🇰🇪 Sheng & Swahili language support  

How it will work:

Kenyan User → Sends "Maternity leave rules?" to WhatsApp Bot  
↓  
Bot queries RAG system  
↓  
User receives: "According to Section 29 of the Employment Act 2007, you are entitled to 3 months maternity leave with full pay..."

Target launch: Q3 2025  

### Other Planned Improvements

Swahili language support (Kamusi ya Sheria)  
Voice input for illiterate users  
PDF report generation of conversations  
Employer compliance checklist generator  
Labour officer directory integration  
Case law database connection  
Salary calculator with statutory deductions  
Contract template generator  

---

## 🏗️ Architecture

User (Browser/WhatsApp)
↓
Frontend (React + Vite on Vercel)
↓
Backend (FastAPI on Render)
↓
RAG Pipeline → Retriever → Context → LLM

---

## 📊 Project Structure

kenya-employment-act-rag/
├── Backend/
│   ├── main.py
│   ├── retrieval.py
│   ├── embedding.py
│   ├── chunking.py
│   ├── requirements.txt
│   ├── runtime.txt
│   ├── build.sh
│   ├── employment_chunks.json
│   ├── EmploymentAct_2007.pdf
│   └── chroma_db/
├── Frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── .env
│   ├── vite.config.js
│   ├── package.json
│   └── vercel.json
└── README.md

---

## 🔧 Environment Variables

### Backend (.env)

OPENAI_API_KEY=your-key-here  
OPENAI_BASE_URL=https://openrouter.ai/api/v1  
PORT=8000  

### Frontend (.env)

VITE_API_URL=http://localhost:8000  

---

## 🧪 Testing

curl /health  
curl /ask  
curl /info  

---

## 🤝 Contributing

git checkout -b feature/amazing-feature  
git commit -m 'Add amazing feature'  
git push origin feature/amazing-feature  

---

## ⚠️ Disclaimer

Important: This AI assistant provides information based on the Kenya Employment Act 2007 but is not a substitute for professional legal advice.

---

## 📄 License

MIT License

---

## 📞 Contact & Support

Report Bug → GitHub Issues  
Feature Request → GitHub Discussions  
WhatsApp Beta → Coming soon!  
Email → mainajoan555@gmail.com

---

## 🙏 Acknowledgments

National Council for Law Reporting (Kenya Law)  
OpenRouter  
LangChain  
Render & Vercel
