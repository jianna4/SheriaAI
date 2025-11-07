import os
os.environ["PYDANTIC_VERSION"] = "1"  # Must be set before any langchain import
#from langchain.chains import RetrievalQA
from langchain_classic.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain_ollama import OllamaEmbeddings
import json
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

# ✅ Initialize Groq Client
def get_groq_response(prompt):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant. Answer clearly and concisely based ONLY on the provided context."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

def query_vectorstore(query):
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    print("Loading vector store from 'faiss_index/'...")
    db = FAISS.load_local(
        r"F:\Program Files\projects\sheria_AI\Sheria_backend\project\app\faiss_indexmain",
        embeddings,
        allow_dangerous_deserialization=True
    )
    print("Vector store loaded.")

    # ✅ Retrieve best matching context - FIXED
    retriever = db.as_retriever(search_kwargs={"k": 1})
    docs = retriever._get_relevant_documents(query, run_manager=None)  # ✅ Add run_manager
    context = docs[0].page_content if docs else "No relevant context found."

    # ✅ Build structured prompt for Groq model
    prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer clearly using ONLY the context."

    answer = get_groq_response(prompt)
    return answer
print(query_vectorstore("what are the grounds for lawful termination of an employment contract ?"))