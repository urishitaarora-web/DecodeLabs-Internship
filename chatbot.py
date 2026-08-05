"""
NovaAI Rule-Based Chatbot Engine
"""

from datetime import datetime
import random

# -----------------------------
# Static Responses
# -----------------------------

JOKES = [
    "😂 Why do programmers prefer dark mode? Because light attracts bugs!",
    "😄 Why did the computer get cold? It forgot to close Windows.",
    "🤣 I told my AI a joke... it generated another one."
]

QUOTES = [
    "🌟 Believe in yourself.",
    "🚀 Success comes from consistency.",
    "💡 Every expert was once a beginner.",
    "🔥 Keep learning. Keep growing."
]

HELP_TEXT = """
Available Commands

👋 Greetings
Time
Date
Day
Help
Joke
Quote
About
Who made you
Version
Python
HTML
CSS
JavaScript
AI
Machine Learning
Flask
Bye
Exit
"""

# -----------------------------
# Response Function
# -----------------------------

def get_response(message: str):

    msg = message.lower().strip()

    if not msg:
        return "Please type something."

    # Greetings

    if msg in ["hi", "hello", "hey", "good morning", "good evening", "good afternoon"]:
        return random.choice([
            "👋 Hello!",
            "😊 Hi there!",
            "🤖 Welcome! I'm NovaAI."
        ])

    # How are you

    elif "how are you" in msg:
        return "😊 I'm functioning perfectly! Thanks for asking."

    # Name

    elif "your name" in msg:
        return "🤖 My name is NovaAI."

    # About

    elif "about" in msg:
        return (
            "NovaAI is a rule-based chatbot built using Python, Flask, "
            "HTML, CSS and JavaScript."
        )

    # Developer

    elif "who made you" in msg:
        return "👨‍💻 I was developed as a Full Stack AI project."

    # Version

    elif "version" in msg:
        return "NovaAI Version 1.0"

    # Help

    elif "help" == msg:
        return HELP_TEXT

    # Time

    elif "time" in msg:
        return datetime.now().strftime("🕒 Current Time : %I:%M:%S %p")

    # Date

    elif "date" in msg:
        return datetime.now().strftime("📅 %d %B %Y")

    # Day

    elif "day" in msg:
        return datetime.now().strftime("%A")

    # Joke

    elif "joke" in msg:
        return random.choice(JOKES)

    # Quote

    elif "quote" in msg or "motivate" in msg:
        return random.choice(QUOTES)

    # Technologies

    elif "python" in msg:
        return "🐍 Python is a powerful programming language."

    elif "html" in msg:
        return "🌐 HTML structures web pages."

    elif "css" in msg:
        return "🎨 CSS styles web pages."

    elif "javascript" in msg:
        return "⚡ JavaScript makes web pages interactive."

    elif "flask" in msg:
        return "🍶 Flask is a lightweight Python web framework."

    elif "machine learning" in msg:
        return "🤖 Machine Learning enables computers to learn from data."

    elif msg == "ai":
        return "Artificial Intelligence enables machines to mimic human intelligence."

    # Goodbye

    elif msg in ["bye", "exit", "quit"]:
        return "👋 Goodbye! Have a wonderful day."

    # Default

    else:
        return (
            "🤔 I don't know about that yet.\n"
            "Type 'help' to see my available commands."
        )