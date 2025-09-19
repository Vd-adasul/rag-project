import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path
from pypdf import PdfReader

print("TECHCORP KNOWLEDGE INGESTION SYSTEM (PDF/TXT/MD)")
print("="*60)

# Connect to vector DB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("techcorp_docs")

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

doc_count = 0
total_chunks = 0

# Look at all files inside "docs" folder
for doc in Path("docs").glob("*.*"):
    if doc.suffix.lower() not in [".pdf", ".md", ".txt"]:
        continue

    print(f"Processing {doc.name}...", end="")

    # --- PDF Handling ---
    if doc.suffix.lower() == ".pdf":
        reader = PdfReader(str(doc))
        content = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                content += text + "\n"
    else:
        with open(doc, "r", encoding="utf-8") as f:
            content = f.read()

    # --- Chunk the document ---
    chunks = [content[i:i+500] for i in range(0, len(content), 400)]

    # --- Store each chunk ---
    for i, chunk in enumerate(chunks):
        doc_id = f"{doc.stem}_{i}"
        embedding = model.encode(chunk).tolist()
        collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[chunk],
            metadatas={"file": doc.name}
        )
        total_chunks += 1

    doc_count += 1
    print(f" ({len(chunks)} chunks)")

print("\nINGESTION COMPLETE!")
print(f"Documents: {doc_count}, Chunks: {total_chunks}")
