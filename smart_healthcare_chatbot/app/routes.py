from flask import Flask, render_template, request, session, jsonify
from app.chatbot import start_session, handle_user_message

app = Flask(__name__)
app.secret_key = 'replace_with_a_secure_key'

@app.route("/", methods=["GET"])
def home():
    start_session(session)
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_text = request.form.get("message", "")
    reply = handle_user_message(session, user_text)
    return jsonify({"response": reply})

@app.route("/reset", methods=["POST"])
def reset():
    start_session(session)
    return ('', 204)
