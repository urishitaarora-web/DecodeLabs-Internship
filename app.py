"""
NovaAI Flask Server
"""

from flask import Flask, render_template, request, jsonify

from chatbot import get_response

app = Flask(__name__)

# -----------------------------
# Home
# -----------------------------

@app.route("/")
def home():
    return render_template("index.html")

# -----------------------------
# Chat API
# -----------------------------

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"reply": "Invalid request."}), 400

    message = data.get("message", "").strip()

    if not message:
        return jsonify({"reply": "Please type a message."})

    reply = get_response(message)

    return jsonify({"reply": reply})

# -----------------------------
# Health Check
# -----------------------------

@app.route("/health")
def health():
    return jsonify({
        "status": "online",
        "bot": "NovaAI"
    })
# -----------------------------
# 404 Error Page
# -----------------------------
@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "404.html"
    ),404
# -----------------------------
# Run
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)

