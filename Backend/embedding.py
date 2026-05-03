"""
Step 2: Load JSON chunks, embed with LangChain + OpenAI, store in Chroma
Modified for deployment - creates chroma_db during build
"""

import json
import os
from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

class ChromaStore:
    def __init__(self, chunks_json_path: str = "employment_chunks.json", persist_directory: str = "./chroma_db"):
        self.chunks_json_path = chunks_json_path
        self.persist_directory = persist_directory
        
        # Initialize OpenAI embeddings
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
        
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        print(f"🔑 Using API key: {api_key[:10]}...")
        print(f"🌐 Using base URL: {base_url}")
        
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-ada-002",
            openai_api_key=api_key,
            base_url=base_url
        )
    
    def load_chunks_from_json(self) -> List[Document]:
        """Load chunks from JSON file and convert to LangChain Documents"""
        print(f"📂 Loading chunks from: {self.chunks_json_path}")
        
        if not os.path.exists(self.chunks_json_path):
            raise FileNotFoundError(f"Chunks file not found: {self.chunks_json_path}")
        
        with open(self.chunks_json_path, 'r', encoding='utf-8') as f:
            chunks_data = json.load(f)
        
        documents = []
        for chunk in chunks_data:
            doc = Document(
                page_content=chunk['text'],
                metadata=chunk['metadata']
            )
            documents.append(doc)
        
        print(f"✅ Loaded {len(documents)} chunks")
        return documents
    
    def create_vector_store(self, documents: List[Document]):
        """Create Chroma vector store from documents"""
        print(f"🔧 Creating Chroma vector store at: {self.persist_directory}")
        
        os.makedirs(self.persist_directory, exist_ok=True)
        
        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        
        print(f"✅ Stored {len(documents)} embeddings in Chroma")
        return vector_store
    
    def run(self):
        """Run the embedding pipeline"""
        print("\n" + "="*60)
        print("STEP 2: Embedding Chunks and Storing in Chroma")
        print("="*60)
        
        documents = self.load_chunks_from_json()
        vector_store = self.create_vector_store(documents)
        
        # Test retrieval
        print("\n🔍 Testing retrieval...")
        test_query = "What are the maternity leave rules?"
        results = vector_store.similarity_search(test_query, k=3)
        
        print(f"\n✅ Test successful! Retrieved {len(results)} relevant chunks")
        
        return vector_store

if __name__ == "__main__":
    store = ChromaStore()
    store.run()