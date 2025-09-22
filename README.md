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
```
### 2. Create a virtual environment
```bash
python -m venv venv
# Activate
venv\Scripts\activate      # Windows
# OR
source venv/bin/activate   # Mac/Linux
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Add your Gemini API key
Copy the example environment file and add your API key:

```bash
cp .env.example .env
Then open .env and add:

text
GEMINI_API_KEY=your_api_key_here
```
### 5. Add your documents
Put your PDF files inside the docs/ folder.

### 6. Initialize the vector database
Run these scripts to process your PDFs and set up FAISS:

```bash
python ingest_documents.py
python init_vectordb.py
```
### 7. Run the RAG chatbot
```bash
python app.py
Open your browser and go to http://localhost:5000.
```
### ✅ Project Structure
```text
rag-project/
│
├─ app.py                # Flask web app
├─ rag_pipeline.py       # Main RAG logic
├─ ingest_documents.py   # Script to load PDFs
├─ init_vectordb.py      # Script to create FAISS DB
├─ docs/                 # PDF documents
├─ templates/            # HTML templates (chat UI)
├─ static/               # CSS, JS, images
├─ chroma_db/            # Local vector DB (auto-generated, ignored in Git)
├─ venv/                 # Virtual environment (ignored in Git)
├─ .env                  # API key (ignored in Git)
├─ .env.example          # Example API key file
├─ requirements.txt      # Python dependencies
└─ README.md             # Project documentation
⚠️ Notes
chroma_db/ should not be pushed to GitHub; it can be rebuilt locally.

.env should never be committed; use .env.example for sharing instructions.

Conversation history is stored in Flask sessions.
```
### 📦 Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit - RAG Chatbot"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/rag-project.git
git push -u origin main
Your friends can now clone the repo, add their Gemini API key, and run the chatbot locally.
```
### 🎨 UI Improvements
You can improve templates/chat.html with Bootstrap or TailwindCSS for a cleaner look.

Memory is already handled via Flask sessions to maintain conversation history.

### 🛠 Dependencies
Flask

google-generativeai

langchain

faiss-cpu

pypdf

python-dotenv
