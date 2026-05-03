"""
Main entry point - orchestrates everything with LangChain
"""

import os
import sys
from pathlib import Path

# Import our modules
from chunk_pdf_to_json import PDFChunker
from embed_and_store import ChromaStore
from retrieval_qa import EmploymentQASystem

def check_prerequisites():
    """Check if all required files and variables exist"""
    
    # Check for .env file
    if not os.path.exists(".env"):
        print("\n❌ .env file not found!")
        print("Please create .env file with:")
        print("OPENAI_API_KEY=your_key_here\n")
        return False
    
    # Check for PDF
    if not os.path.exists("EmploymentAct_2007.pdf"):
        print("\n❌ EmploymentAct_2007.pdf not found!")
        print("Please place the PDF in the current directory\n")
        return False
    
    return True

def run_full_pipeline(force_fresh: bool = False):
    """
    Run the complete RAG pipeline
    
    Args:
        force_fresh: If True, reprocess everything from scratch
    """
    
    print("\n" + "="*60)
    print("🇰🇪 KENYA EMPLOYMENT ACT RAG SYSTEM")
    print("="*60)
    
    # File paths
    json_path = "employment_chunks.json"
    chroma_dir = "./chroma_db"
    
    # Step 1: Chunk PDF to JSON
    if force_fresh or not os.path.exists(json_path):
        chunker = PDFChunker(pdf_path="EmploymentAct_2007.pdf")
        json_path = chunker.run()
    else:
        print(f"\n⏭️  Using existing chunks: {json_path}")
    
    # Step 2: Embed and store in Chroma
    if force_fresh or not os.path.exists(chroma_dir):
        embedder = ChromaStore(chunks_json_path=json_path, persist_directory=chroma_dir)
        embedder.run()
    else:
        print(f"\n⏭️  Using existing Chroma DB: {chroma_dir}")
    
    # Step 3: Start interactive Q&A
    print("\n" + "="*60)
    print("STEP 3: Starting Interactive Q&A")
    print("="*60)
    
    qa_system = EmploymentQASystem(persist_directory=chroma_dir)
    qa_system.interactive_chat()

def quick_test():
    """Quick test without interactive mode"""
    
    print("\n" + "="*60)
    print("🧪 QUICK TEST MODE")
    print("="*60)
    
    # Check if we have existing data
    if not os.path.exists("./chroma_db"):
        print("No existing Chroma DB found. Running full pipeline...")
        run_full_pipeline(force_fresh=True)
        return
    
    # Test QA
    qa_system = EmploymentQASystem()
    
    test_questions = [
        ("How much annual leave am I entitled to?", "employee"),
        ("What are the rules for terminating an employee?", "employer"),
        ("Can I be fired for joining a trade union?", "employee"),
    ]
    
    for question, role in test_questions:
        print(f"\n{'='*50}")
        result = qa_system.answer_question(question, role)
        print(f"\nQ: {question}")
        print(f"A: {result['answer'][:300]}...")
        print(f"Sources: {[s['section'] for s in result['sources']]}")

if __name__ == "__main__":
    # Check prerequisites
    if not check_prerequisites():
        sys.exit(1)
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            quick_test()
        elif sys.argv[1] == --fresh":
            run_full_pipeline(force_fresh=True)
        else:
            print("Usage:")
            print("  python main.py           # Run interactive mode (reuse existing)")
            print("  python main.py --test    # Run quick test")
            print("  python main.py --fresh   # Reprocess everything from scratch")
    else:
        # Default: Run interactive with reuse
        run_full_pipeline(force_fresh=False)