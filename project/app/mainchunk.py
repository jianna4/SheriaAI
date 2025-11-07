from langchain_community.document_loaders import PyPDFLoader
import re
import json
from typing import List, Dict

# === STEP 1: Load the PDF ===
pdf_path = r"F:\Program Files\projects\sheria_AI\Sheria_backend\project\app\EmploymentAct_2007.pdf"
loader = PyPDFLoader(pdf_path)
docs = loader.load()
print(f"✅ Loaded {len(docs)} pages from PDF.")

# === STEP 2: Combine & Clean ===
cleaned_text = "\n".join([d.page_content for d in docs])

# Remove artifacts, headers, and footers
cleaned_text = re.sub(r'\[\d+\]', '', cleaned_text)
cleaned_text = re.sub(
    r'\*\[Rev\. 2012\] CAP\. 226 Employment\*|CAP\. 226 \[Rev\. 2012\] Employment|\d+ \[Issue 1\]|'
    r'\n\s*\[Subsidiary\]|LAWS OF KENYA|CHAPTER 226|Revised Edition 2012 \[2007\]',
    '', cleaned_text
)
cleaned_text = re.sub(r'[ \t]+', ' ', cleaned_text)
cleaned_text = cleaned_text.replace('\n\n', '@@@').replace('\n', ' ').replace('@@@', '\n\n').strip()

# === STEP 3: Define Regex Patterns ===
PART_PATTERN = re.compile(r'(PART [IVXLC]+ – [A-Z].*?)(?=\n|$)')
SECTION_PATTERN = re.compile(r'(\d+\.\s+[A-Z].*?)(?=\n\d+\.|\Z)', re.DOTALL)
CLAUSE_PATTERN = re.compile(r'(\(\d+\)|\([a-z]\)|\([ivx]+\))')

# === STEP 4: Chunking ===
chunks = []
current_part = "Preamble / Introductory"

# Split document into parts
parts = re.split(r'(PART [IVXLC]+ – [A-Z].*?\n)', cleaned_text)
for i in range(0, len(parts), 2):
    if i + 1 < len(parts):
        part_title = parts[i + 1].strip()
        part_body = parts[i].strip()
    else:
        part_title = current_part
        part_body = parts[i].strip()

    if not part_body:
        continue
    current_part = part_title

    # Split by section
    sections = SECTION_PATTERN.findall(part_body)
    if not sections:
        chunks.append({
            "part": current_part,
            "section_number": "N/A",
            "section_title": "Introductory or Unnumbered Text",
            "text": part_body.strip(),
            "source_act": "Employment Act, Cap 226"
        })
        continue

    for section in sections:
        section_lines = section.strip().split('\n', 1)
        header_line = section_lines[0]
        match = re.match(r'(\d+)\.\s+(.*)', header_line)
        section_number = match.group(1) if match else "Unknown"
        section_title = match.group(2) if match else "Unknown"
        section_body = section[len(header_line):].strip()

        # Split into logical clauses
        clause_chunks = re.split(CLAUSE_PATTERN, section_body)
        buffer = ""
        for item in clause_chunks:
            if not item.strip():
                continue
            if CLAUSE_PATTERN.fullmatch(item):
                if buffer.strip():
                    chunks.append({
                        "part": current_part,
                        "section_number": section_number,
                        "section_title": section_title,
                        "text": buffer.strip(),
                        "source_act": "Employment Act, Cap 226"
                    })
                buffer = item
            else:
                buffer += " " + item.strip()

        if buffer.strip():
            chunks.append({
                "part": current_part,
                "section_number": section_number,
                "section_title": section_title,
                "text": buffer.strip(),
                "source_act": "Employment Act, Cap 226"
            })

# === STEP 5: Save Outputs ===
with open("employment_chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2, ensure_ascii=False)

with open("employment_chunks.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join([
        f"{c['part']}\nSection {c['section_number']}: {c['section_title']}\n{c['text']}"
        for c in chunks
    ]))

print(f"✅ Saved {len(chunks)} chunks to 'employment_chunks.json' and 'employment_chunks.txt'.")
