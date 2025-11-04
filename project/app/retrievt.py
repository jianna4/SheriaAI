import os
import json
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama


# ---------------------------
# 📁 PATH CONFIGURATION
# ---------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_DIR = os.path.join(BASE_DIR, "memory")
MEMORY_PATH = os.path.join(MEMORY_DIR, "longterm_memory.json")

# FAISS index path
FAISS_INDEX_PATH = os.path.join(BASE_DIR, "faiss_index")


# ---------------------------
# 🧠 MEMORY HELPERS
# ---------------------------
def ensure_memory_file():
    """Ensure that the memory folder and file exist."""
    if not os.path.exists(MEMORY_DIR):
        os.makedirs(MEMORY_DIR)

    if not os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, "w", encoding="utf-8") as f:
            json.dump([], f)  # start with an empty list


def save_memory(query: str, answer: str):
    """Append a new interaction (query + answer) to memory file."""
    ensure_memory_file()

    with open(MEMORY_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    data.append({"query": query, "answer": answer})

    with open(MEMORY_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_memory_context(limit: int = 3):
    """Load the last few stored interactions to give the model context."""
    ensure_memory_file()

    with open(MEMORY_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    recent = data[-limit:] if data else []
    # Join them into a context string
    context = "\n".join(
        [f"User: {item['query']}\nAI: {item['answer']}" for item in recent]
    )
    return context


# ---------------------------
# 🧩 MAIN RETRIEVAL FUNCTION
# ---------------------------
def quey_vectorstore(query: str):
    """Query the FAISS vector store, get answer, and store to memory."""

    print("🔹 Loading embeddings and FAISS index...")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    db = FAISS.load_local(
        FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True
    )

    llm = Ollama(model="llama3.1:8b")
    retriever = db.as_retriever(search_kwargs={"k": 2})

    # 🧠 Include previous chat context
    memory_context = load_memory_context(limit=3)
    full_query = f"{memory_context}\nUser: {query}" if memory_context else query

    # Build the QA chain
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")

    print("🔍 Getting answer from model...")
    result = qa.invoke(full_query)

    # The result may be a dict depending on the version of LangChain
    answer = result.get("result") if isinstance(result, dict) else str(result)

    # 💾 Save to long-term memory
    save_memory(query, answer)

    print("✅ Memory updated successfully.")
    return answer
