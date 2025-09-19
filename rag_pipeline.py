import os
import chromadb
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Load DB + model
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("techcorp_docs")
model = SentenceTransformer('all-MiniLM-L6-v2')

def rag_query(question: str) -> str:
    # 1. RETRIEVAL
    query_embedding = model.encode(question).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=3)
    context = "\n\n".join(results["documents"][0])

    # 2. AUGMENTATION
    prompt = f"""You are student's AI assistant.
Answer the question using the documents below.
If unsure, say you don’t know.

Documents:
{context}

Question: {question}
Answer:"""

    # 3. GENERATION
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
    return response.text

if __name__ == "__main__":
    q = input("Ask a question: ")
    print("\nAI Answer:\n", rag_query(q))
