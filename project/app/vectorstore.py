from langchain_community.vectorstores import FAISS

import json
import os
from langchain.embeddings import OllamaEmbeddings


from langchain.schema import Document



with open(r"F:\Program Files\projects\sheria_AI\Sheria_backend\project\app\kenya_employment_act_chunks.json", "r", encoding="utf-8") as f:
    data = json.load(f)




# Convert to LangChain Document objects
documents = [Document(page_content=item["page_content"], metadata=item["metadata"]) for item in data]

print(f"Loaded {len(documents)} documents with metadata ready for embedding.")
print("Example metadata:", documents[0].metadata)

embeddings = OllamaEmbeddings(model="nomic-embed-text")
#now the vector db
vectorstore = FAISS.from_documents(documents, embeddings)
print("Vector store created with FAISS.")
vectorstore.save_local("faiss_index")
print("Vector store saved to 'faiss_index/'")