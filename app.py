import os
from flask import Flask, render_template, request, session, jsonify
from rag_logic import rag_query

app = Flask(__name__)
app.secret_key = "super-secret-key"  # for session memory

@app.route("/")
def index():
    if "history" not in session:
        session["history"] = []
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_msg = request.json["message"]

    # Retrieve history from the session
    history = session.get("history", [])

    # Get AI answer from the core RAG function
    answer = rag_query(user_msg, history)

    # Update session memory
    history.append({"user": user_msg, "ai": answer})
    session["history"] = history

    return jsonify({"answer": answer})

@app.route("/clear", methods=["POST"])
def clear():
    session["history"] = []
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    app.run(debug=True)
