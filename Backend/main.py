"""
FastAPI Backend for Kenya Employment Act RAG System
This is the main API that the React frontend will connect to
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the RAG system
from retrieval import EmploymentQASystem

# Initialize FastAPI
app = FastAPI(
    title="Kenya Employment Act RAG API",
    description="AI-powered assistant for Kenya Employment Act 2007",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)



# CORS middleware - Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # Local development
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        # Production (Render)
        "https://sheriaai.onrender.com",
        "https://www.sheriaai.onrender.com",
        # Allow all Render subdomains (for preview deployments)
        "https://*.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept"],
)
# Global variable for QA system
qa_system = None

# Request/Response Models
class QuestionRequest(BaseModel):
    query: str
    role: str = "employee"

class SourceResponse(BaseModel):
    section: str
    page: Optional[str] = None
    preview: str

class AnswerResponse(BaseModel):
    question: str
    answer: str
    sources: List[SourceResponse]

class HealthResponse(BaseModel):
    status: str
    qa_system_ready: bool
    chroma_db_exists: bool

# Startup Event
@app.on_event("startup")
async def startup_event():
    """Initialize the QA system when the API starts"""
    global qa_system
    print("\n" + "="*60)
    print("🚀 Starting Kenya Employment Act RAG API")
    print("="*60)
    
    # Check if Chroma DB exists
    chroma_path = "./chroma_db"
    if not os.path.exists(chroma_path):
        print("⚠️ Chroma database not found at ./chroma_db")
        print("Please run: python embedding.py first")
        qa_system = None
    else:
        try:
            print("📚 Loading Chroma database...")
            qa_system = EmploymentQASystem(persist_directory=chroma_path, k_retrieval=5)
            print("✅ QA System ready!")
        except Exception as e:
            print(f"❌ Error loading QA system: {e}")
            qa_system = None
    
    print("="*60 + "\n")

# Health Check Endpoints
@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - API health check"""
    chroma_exists = os.path.exists("./chroma_db")
    return HealthResponse(
        status="healthy",
        qa_system_ready=qa_system is not None,
        chroma_db_exists=chroma_exists
    )

@app.get("/health")
async def health_check():
    """Detailed health check for monitoring"""
    chroma_exists = os.path.exists("./chroma_db")
    return {
        "status": "ok",
        "qa_system_loaded": qa_system is not None,
        "chroma_db_exists": chroma_exists,
        "chroma_db_path": "./chroma_db",
        "api_version": "1.0.0"
    }

# Main Question Answering Endpoint
@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask a question about the Kenya Employment Act 2007
    
    - **query**: Your question about employment law
    - **role**: Either "employee" or "employer" (changes response style)
    
    Returns an answer with cited sources from the Act
    """
    
    # Validate input
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    if request.role not in ["employee", "employer"]:
        raise HTTPException(status_code=400, detail="Role must be 'employee' or 'employer'")
    
    # Check if QA system is ready
    if qa_system is None:
        raise HTTPException(
            status_code=503,
            detail="QA system not initialized. Please ensure Chroma DB exists and run embedding.py first."
        )
    
    try:
        # Get answer from QA system
        print(f"📝 Processing question: {request.query[:50]}...")
        result = qa_system.answer_question(request.query, request.role)
        
        # Return formatted response
        return AnswerResponse(
            question=result["question"],
            answer=result["answer"],
            sources=[
                SourceResponse(
                    section=source.get("section", "Unknown"),
                    page=source.get("page"),
                    preview=source.get("preview", "")
                )
                for source in result["sources"]
            ]
        )
    
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Stats Endpoint
@app.get("/stats")
async def get_stats():
    """Get statistics about the vector store"""
    if qa_system is None:
        raise HTTPException(status_code=503, detail="QA system not initialized")
    
    try:
        count = qa_system.vector_store._collection.count()
        return {
            "vector_count": count,
            "persist_directory": "./chroma_db",
            "model": "text-embedding-ada-002 via OpenRouter",
            "k_retrieval": qa_system.k_retrieval
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Info Endpoint
@app.get("/info")
async def get_info():
    """Get information about available sections"""
    return {
        "act_name": "Kenya Employment Act 2007 (Chapter 226)",
        "commencement_date": "2nd June, 2008",
        "parts": [
            "Part I - Preliminary",
            "Part II - General Principles", 
            "Part III - Employment Relationship",
            "Part IV - Protection of Wages",
            "Part V - Rights and Duties in Employment",
            "Part VI - Termination and Dismissal",
            "Part VII - Protection of Children",
            "Part VIII - Insolvency of Employer",
            "Part IX - Employment Records",
            "Part X - Employment Management",
            "Part XI - Foreign Contracts of Service",
            "Part XII - Disputes Settlement Procedure",
            "Part XIII - Miscellaneous Provisions"
        ],
        "subsidiary_rules": [
            "Employment (Children) Rules, 1977",
            "Employment Service Rules, 1977",
            "Employment (Medical Treatment) Rules, 1977",
            "Employment Of Juveniles At Sea (Medical Examination) Rules, 1977",
            "Employment (Sanitation) Rules, 1977",
            "Employment (Foreign Contracts of Service) Rules, 1977"
        ]
    }

# Simple HTML test interface
@app.get("/test")
async def test_interface():
    """Simple HTML test interface"""
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Kenya Employment Act API Test</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            h1 { color: #4CAF50; }
            select, input, button { padding: 10px; margin: 5px; border-radius: 5px; }
            select, input { border: 1px solid #ccc; }
            button { background: #4CAF50; color: white; border: none; cursor: pointer; }
            button:hover { background: #45a049; }
            #response { margin-top: 20px; padding: 15px; background: #f5f5f5; border-radius: 5px; white-space: pre-wrap; }
            .sources { color: #666; font-size: 0.9em; margin-top: 10px; }
        </style>
    </head>
    <body>
        <h1>🇰🇪 Kenya Employment Act API Test</h1>
        <div>
            <select id="role">
                <option value="employee">👥 Employee Mode (Know Your Rights)</option>
                <option value="employer">💼 Employer Mode (Understand Obligations)</option>
            </select>
            <br>
            <input type="text" id="question" placeholder="Ask a question about employment law..." size="60">
            <br>
            <button onclick="ask()">Ask Question</button>
            <button onclick="clearResponse()">Clear</button>
        </div>
        <div id="response"></div>
        
        <script>
            async function ask() {
                const role = document.getElementById('role').value;
                const query = document.getElementById('question').value;
                const responseDiv = document.getElementById('response');
                
                if (!query) {
                    responseDiv.innerHTML = 'Please enter a question.';
                    return;
                }
                
                responseDiv.innerHTML = '🤔 Thinking...';
                
                try {
                    const response = await fetch('/ask', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ query, role })
                    });
                    const data = await response.json();
                    
                    responseDiv.innerHTML = `
                        <strong>📝 Answer:</strong><br>
                        ${data.answer}
                        <div class="sources">
                            <strong>📚 Sources:</strong><br>
                            ${data.sources.map(s => `• Section ${s.section}`).join('<br>')}
                        </div>
                    `;
                } catch (error) {
                    responseDiv.innerHTML = `❌ Error: ${error.message}`;
                }
            }
            
            function clearResponse() {
                document.getElementById('response').innerHTML = '';
                document.getElementById('question').value = '';
            }
            
            // Allow Enter key to submit
            document.getElementById('question').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    ask();
                }
            });
        </script>
    </body>
    </html>
    """)

# Run the server
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    
    print("\n" + "="*60)
    print("🇰🇪 Kenya Employment Act RAG API")
    print("="*60)
    print(f"📡 Server: http://localhost:{port}")
    print(f"📚 API Docs: http://localhost:{port}/docs")
    print(f"🧪 Test UI: http://localhost:{port}/test")
    print("="*60 + "\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )