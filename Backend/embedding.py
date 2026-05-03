"""
Step 2: Load JSON chunks, embed with LangChain + OpenAI, store in Chroma
Uses ONLY LangChain imports
"""

import json
from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document
from dotenv import load_dotenv
import os

load_dotenv()

class ChromaStore:
    def __init__(self, chunks_json_path: str, persist_directory: str = "./chroma_db"):
        self.chunks_json_path = chunks_json_path
        self.persist_directory = persist_directory
        
        # Initialize OpenAI embeddings
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-ada-002",
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
    
    def load_chunks_from_json(self) -> List[Document]:
        """Load chunks from JSON file and convert to LangChain Documents"""
        print(f"📂 Loading chunks from: {self.chunks_json_path}")
        
        with open(self.chunks_json_path, 'r', encoding='utf-8') as f:
            chunks_data = json.load(f)
        
        # Convert to LangChain Document objects
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
        
        # Create and persist Chroma store
        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        
        # Persist to disk
        vector_store.persist()
        
        print(f"✅ Stored {len(documents)} embeddings in Chroma")
        return vector_store
    
    def run(self):
        """Run the embedding pipeline"""
        print("\n" + "="*60)
        print("STEP 2: Embedding Chunks and Storing in Chroma")
        print("="*60)
        
        # Load chunks
        documents = self.load_chunks_from_json()
        
        # Create vector store
        vector_store = self.create_vector_store(documents)
        
        # Test retrieval
        print("\n🔍 Testing retrieval...")
        test_query = "What are the maternity leave rules?"
        results = vector_store.similarity_search(test_query, k=3)
        
        print(f"\n✅ Test successful! Retrieved {len(results)} relevant chunks:")
        for i, result in enumerate(results[:2], 1):
            print(f"\n  Result {i}:")
            print(f"    Page: {result.metadata.get('page', 'N/A')}")
            print(f"    Section: {result.metadata.get('section_number', 'N/A')}")
            print(f"    Preview: {result.page_content[:150]}...")
        
        return vector_store

if __name__ == "__main__":
    store = ChromaStore(chunks_json_path="employment_chunks.json")
    store.run()