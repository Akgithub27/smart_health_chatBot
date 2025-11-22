"""
Flask routes
"""
from flask import Flask, render_template, request, session, jsonify
from app.chatbot import start_session, handle_user_message

app = Flask(__name__)
app.secret_key = 'your-secret-key-for-local-development'

@app.route("/", methods=["GET"])
def home():
    """Render home page and initialize session"""
    start_session(session)
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """Handle chat messages"""
    user_text = request.form.get("message", "").strip()
    
    if not user_text:
        return jsonify({"response": "Please enter a message."})
    
    # Ensure session is initialized
    if 'stage' not in session:
        start_session(session)
    
    # Process message
    reply = handle_user_message(session, user_text)
    return jsonify({"response": reply})

@app.route("/reset", methods=["POST"])
def reset():
    """Reset chat session"""
    start_session(session)
    return ('', 204)