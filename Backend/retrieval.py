"""
Step 3: Load Chroma, create RAG chain with LangChain
Works with both FastAPI and interactive chat
"""

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from typing import Dict, Any, List
from dotenv import load_dotenv
import os

load_dotenv()

class EmploymentQASystem:
    def __init__(self, persist_directory: str = "./chroma_db", k_retrieval: int = 5):
        self.persist_directory = persist_directory
        self.k_retrieval = k_retrieval
        
        # Initialize embeddings with OpenRouter
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-ada-002",
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        )
        
        # Initialize LLM with OpenRouter
        self.llm = ChatOpenAI(
            model="openai/gpt-3.5-turbo",  # Note: openai/ prefix for OpenRouter
            temperature=0.2,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        )
        
        # Load Chroma store
        print(f"📚 Loading Chroma store from: {persist_directory}")
        self.vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embeddings
        )
        print(f"✅ Chroma store loaded with {self.vector_store._collection.count()} vectors")
    
    def format_docs(self, docs):
        """Format retrieved documents for context"""
        return "\n\n---\n\n".join([
            f"[Section {d.metadata.get('section_number', 'Unknown')} - Page {d.metadata.get('page', 'Unknown')}]\n{d.page_content}"
            for d in docs
        ])
    
    def create_rag_chain(self, role: str = "employee"):
        """Create a RAG chain for question answering"""
        
        # Role-specific system prompts
        role_prompts = {
            "employee": """You are a helpful legal assistant for Kenyan workers. 
Your job is to explain employment rights clearly in simple language.

Guidelines:
- Be empathetic and practical
- Cite specific sections of the Employment Act 2007
- If unsure, suggest consulting a labour officer
- Focus on: employee protections, leave entitlements, unfair dismissal, discrimination

Context from the Employment Act 2007:
{context}

Question: {question}

Answer clearly and helpfully:""",
            
            "employer": """You are a legal compliance assistant for Kenyan employers.
Your job is to explain employer obligations clearly and professionally.

Guidelines:
- Be precise and cite specific sections
- Highlight compliance requirements and potential penalties
- Focus on: contracts, records, deductions, termination procedures, health and safety

Context from the Employment Act 2007:
{context}

Question: {question}

Answer professionally and accurately:"""
        }
        
        # Create prompt template
        prompt = ChatPromptTemplate.from_template(role_prompts[role])
        
        # Create RAG chain
        chain = (
            {"context": self.vector_store.as_retriever(search_kwargs={"k": self.k_retrieval}) | self.format_docs,
             "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        return chain
    
    def answer_question(self, question: str, role: str = "employee") -> Dict[str, Any]:
        """Answer a question using RAG - Used by both API and interactive chat"""
        
        print(f"\n💬 Question ({role}): {question}")
        
        # Create chain for this role
        chain = self.create_rag_chain(role)
        
        # Get answer
        answer = chain.invoke(question)
        
        # Get sources for transparency
        retriever = self.vector_store.as_retriever(search_kwargs={"k": self.k_retrieval})
        source_docs = retriever.invoke(question)
        
        return {
            "question": question,
            "answer": answer,
            "sources": [
                {
                    "section": doc.metadata.get("section_number", "Unknown"),
                    "page": str(doc.metadata.get("page", "Unknown")),
                    "preview": doc.page_content[:100] + "..."
                }
                for doc in source_docs[:3]
            ]
        }
    
    def interactive_chat(self):
        """Run interactive chat session"""
        print("\n" + "="*60)
        print("🤖 KENYA EMPLOYMENT ACT - RAG CHATBOT")
        print("="*60)
        print("\nCommands:")
        print("  /employee - Switch to employee mode (know your rights)")
        print("  /employer - Switch to employer mode (understand obligations)")
        print("  /sources  - Show sources for last answer")
        print("  /quit     - Exit chatbot")
        print("-" * 60)
        
        current_role = "employee"
        last_sources = []
        
        while True:
            user_input = input(f"\n[{current_role.upper()}] You: ").strip()
            
            if user_input.lower() == '/quit':
                print("\n👋 Goodbye!")
                break
            elif user_input.lower() == '/employee':
                current_role = "employee"
                print("✅ Switched to EMPLOYEE mode")
                continue
            elif user_input.lower() == '/employer':
                current_role = "employer"
                print("✅ Switched to EMPLOYER mode")
                continue
            elif user_input.lower() == '/sources':
                if last_sources:
                    print("\n📚 Last answer sources:")
                    for source in last_sources:
                        if source['section'] != 'Unknown':
                            print(f"  • Section {source['section']} (Page {source['page']})")
                else:
                    print("No sources yet. Ask a question first.")
                continue
            
            if not user_input:
                continue
            
            # Get answer
            result = self.answer_question(user_input, current_role)
            last_sources = result['sources']
            
            print(f"\n🤖 Assistant: {result['answer']}")
            
            # Show sources
            valid_sources = [s for s in result['sources'] if s['section'] != 'Unknown']
            if valid_sources:
                sections = [f"Section {s['section']}" for s in valid_sources]
                print(f"\n📚 Sources: {', '.join(sections)}")
if __name__ == "__main__":
    qa_system = EmploymentQASystem()
    qa_system.interactive_chat()