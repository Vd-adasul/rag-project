import os
import chromadb
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

# --- Load vector DB + model ---
# These are global so they are only loaded once when the module is imported.
try:
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection("techcorp_docs")
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    # Print an error message if the vector database or model fails to load.
    print(f"Error loading vector DB or sentence transformer: {e}")
    # Re-raise the exception to stop the application from starting.
    raise

# --- Configure Gemini ---
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    llm = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    raise

def rag_query(question: str, history: list):
    """
    Performs a RAG query using the provided question and conversation history.

    Args:
        question (str): The current user's question.
        history (list): A list of dictionaries representing the conversation history.
                        Each dictionary has keys 'user' and 'ai'.

    Returns:
        str: The generated response from the LLM.
    """
    # Check if the collection is available before querying
    if not collection:
        return "The document collection is not available. Please ensure the database is set up correctly."

    try:
        # Encode question to get the embedding
        query_embedding = embedder.encode(question).tolist()

        # Query the ChromaDB collection for relevant documents
        results = collection.query(query_embeddings=[query_embedding], n_results=3)
        context = "\n\n".join(results["documents"][0])

        # Build conversation context from history
        history_text = "\n".join([f"User: {h['user']}\nAI: {h['ai']}" for h in history])

        # Construct the final prompt for the LLM
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
        
        # Generate content using the LLM
        response = llm.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"An error occurred during the RAG query: {e}")
        return "An error occurred while generating the response."
