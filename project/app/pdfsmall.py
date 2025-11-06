from langchain_community.document_loaders import PyPDFLoader

#from langchain.text_splitter import RecursiveCharacterTextSplitter
#from langchain.schema import Document
import re #this is for regex operations to search for text that matches a pattern
import json

pdf_path = r"F:\Program Files\projects\sheria_AI\Sheria_backend\project\app\Labour Relations Act (1).pdf"
loader = PyPDFLoader(pdf_path)

docs = loader.load()
print(f"Loaded {len(docs)} documents from PDF.")


#coz it goes page by page,add this
full_text = ""
for page in docs:
    full_text += page.page_content + "\n"

#Split at newlines that are followed by a section-like pattern
chunks = re.split(r'\n(?=\s*\d+[A-Z]?\.\s)', full_text)

# Remove empty or whitespace-only chunks
chunks = [chunk.strip() for chunk in chunks if chunk.strip()]



documents = []  # this will hold all your chunks with metadata

for chunk in chunks:
    # Try to read the section number and title from the start of the chunk
    match = re.search(r'(\d+[A-Z]?)\.\s*(.*)', chunk)
    
    if match:
        section_num = match.group(1)      # e.g., "5" or "10A"
        section_title = match.group(2)[:100]  # first 100 characters of the title
    else:
        section_num = "Preamble"
        section_title = "Introductory"

    # Create a LangChain Document with metadata
    documents.append({
        "page_content":chunk,
        "metadata":{
            "source": "Employment Act 2007 (Kenya)",
            "section_number": section_num,
            "section_title": section_title,
            "jurisdiction": "Kenya",
            "effective_date": "2022-12-31"
        }
    })


# Save to a JSON file
with open("kenya_employment_act_chunks.json", "w", encoding="utf-8") as f:
    json.dump(documents, f, indent=2, ensure_ascii=False)


with open("kenya_employment_act_chunks.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(
        [f"{doc['metadata']['section_number']}. {doc['metadata']['section_title']}\n{doc['page_content']}"
         for doc in documents]
    ))
print(f"Saved {len(documents)} chunks to 'kenya_employment_act_chunks.json' and 'kenya_employment_act_chunks.txt'.")