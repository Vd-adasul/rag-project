# 📚 RAG Chatbot (Flask + Google Gemini)

This is a **Retrieval-Augmented Generation (RAG) chatbot** built with:

- **Flask** → Web UI  
- **Google Gemini API** → Answers questions using generative AI  
- **FAISS** → Local vector database  
- **LangChain** → RAG pipeline  
- **PDF Loader** → Load your documents into the vector DB  

The chatbot can answer questions from your PDF documents and remembers conversation history.

---

## 🚀 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/rag-project.git
cd rag-project

### 2. Create a virtual environment
python -m venv venv
# Activate
venv\Scripts\activate      # Windows
# OR
source venv/bin/activate   # Mac/Linux

### 3.Install dependencies
cp .env.example .env
