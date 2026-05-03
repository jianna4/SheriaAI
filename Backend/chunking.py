"""
Step 1: Load PDF with LangChain, chunk intelligently, save to JSON
Uses ONLY LangChain imports
"""

import json
from typing import List
from dataclasses import dataclass, asdict
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

@dataclass
class Chunk:
    """Represents a single chunk for storage"""
    text: str
    metadata: dict
    chunk_id: str

class PDFChunker:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.chunks = []
        
    def load_pdf(self) -> List[Document]:
        """Load PDF using LangChain's PyMuPDFLoader"""
        print(f"📄 Loading PDF: {self.pdf_path}")
        loader = PyMuPDFLoader(self.pdf_path)
        documents = loader.load()
        print(f"✅ Loaded {len(documents)} pages")
        return documents
    
    def chunk_documents(self, documents: List[Document]) -> List[Chunk]:
        """Chunk documents using LangChain's text splitter"""
        
        # Use recursive character splitter for clean boundaries
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=[
                "\n\n",           # Double newline (paragraphs)
                "\n",             # Single newline
                "(?<=\. )",       # Sentences
                " ",              # Words
                ""                # Characters
            ],
            length_function=len,
        )
        
        # Split documents
        split_docs = text_splitter.split_documents(documents)
        
        # Convert to our Chunk format with better metadata
        chunks = []
        for i, doc in enumerate(split_docs):
            # Extract section number if possible (look for patterns like "5.")
            section_match = None
            lines = doc.page_content.split('\n')
            for line in lines[:3]:  # Check first 3 lines
                import re
                match = re.match(r'^\s*(\d+)\.', line)
                if match:
                    section_match = match.group(1)
                    break
            
            chunk = Chunk(
                text=doc.page_content,
                metadata={
                    "source": self.pdf_path,
                    "page": doc.metadata.get("page", 0),
                    "section_number": section_match or "unknown",
                    "chunk_index": i,
                    "total_chunks": len(split_docs)
                },
                chunk_id=f"chunk_{i}_{section_match or 'unknown'}"
            )
            chunks.append(chunk)
        
        print(f"✅ Created {len(chunks)} chunks")
        print(f"   Average chunk size: {sum(len(c.text) for c in chunks) // len(chunks)} chars")
        return chunks
    
    def save_to_json(self, chunks: List[Chunk], output_path: str = "employment_chunks.json"):
        """Save chunks to JSON file"""
        # Convert to serializable format
        chunks_dict = [asdict(chunk) for chunk in chunks]
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(chunks_dict, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Saved {len(chunks)} chunks to {output_path}")
        return output_path
    
    def run(self, output_path: str = "employment_chunks.json"):
        """Run the complete chunking pipeline"""
        print("\n" + "="*60)
        print("STEP 1: Loading PDF and Creating Chunks")
        print("="*60)
        
        # Load PDF
        documents = self.load_pdf()
        
        # Create chunks
        chunks = self.chunk_documents(documents)
        
        # Save to JSON
        json_path = self.save_to_json(chunks, output_path)
        
        # Print sample
        if chunks:
            print("\n📝 Sample chunk:")
            print(f"  ID: {chunks[0].chunk_id}")
            print(f"  Metadata: {chunks[0].metadata}")
            print(f"  Text preview: {chunks[0].text[:200]}...")
        
        return json_path

if __name__ == "__main__":
    # Test the chunker
    chunker = PDFChunker(pdf_path=r"F:\projects\sheria_AI\Sheria_backend\Backend\EmploymentAct_2007.pdf")
    chunker.run()