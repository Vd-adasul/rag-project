import os
from flask import Flask, render_template, request, session, jsonify
import chromadb
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

app = Flask(__name__)
app.secret_key = "super-secret-key"  # for session memory

# --- Load vector DB + model ---
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("techcorp_docs")
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# --- Configure Gemini ---
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
llm = genai.GenerativeModel("gemini-1.5-flash")

def rag_query(question: str, history: list):
    # Encode question
    query_embedding = embedder.encode(question).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=3)
    context = "\n\n".join(results["documents"][0])

    # Build conversation context
    history_text = "\n".join([f"User: {h['user']}\nAI: {h['ai']}" for h in history])

    prompt = f"""
You are TechCorp's helpful AI assistant.
Use the provided documents for accurate answers.
If unsure, say you don’t know.

Conversation so far:
{history_text}

Relevant Documents:
{context}

Current Question: {question}
Answer:"""

    response = llm.generate_content(prompt)
    return response.text

@app.route("/")
def index():
    if "history" not in session:
        session["history"] = []
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_msg = request.json["message"]

    # Retrieve history
    history = session.get("history", [])

    # Get AI answer
    answer = rag_query(user_msg, history)

    # Update session memory
    history.append({"user": user_msg, "ai": answer})
    session["history"] = history

    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
