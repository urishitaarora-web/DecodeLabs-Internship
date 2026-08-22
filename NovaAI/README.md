# 🤖 NovaAI — Advanced Rule-Based AI Chatbot

<p align="center">
  <img src="static/images/nova-avatar.png" alt="NovaAI Logo" width="140"/>
</p>

<p align="center">
  <strong>A full-stack, modular, rule-based intelligent chatbot built with Python, Flask, and modern web technologies. Features multi-domain knowledge (Programming, Science, Mathematics, English & Language, Technology, Utilities), emoji sentiment detection, shortform and abbreviation recognition, voice interaction, and a responsive glassmorphism UI with a collapsible sidebar.</strong>
</p>

<p align="center">
  <a href="https://nova-ai-um96.onrender.com/"><img src="https://img.shields.io/badge/Live%20Demo-Render-46E3B7?style=for-the-badge&logo=render" alt="Live Demo on Render"/></a>
  <img src="https://img.shields.io/badge/Python-3.12%2B-blue?style=for-the-badge&logo=python" alt="Python 3.12+"/>
  <img src="https://img.shields.io/badge/Flask-3.1-black?style=for-the-badge&logo=flask" alt="Flask 3.1"/>
  <img src="https://img.shields.io/badge/Architecture-Rule--Based%20NLP-orange?style=for-the-badge" alt="Rule-Based NLP"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License"/>
</p>

---

## 🌐 Live Demo

🚀 **Experience NovaAI Live:** [https://nova-ai-um96.onrender.com/](https://nova-ai-um96.onrender.com/)

---

## 📖 Overview

**NovaAI** is an advanced conversational and educational chatbot that operates entirely on a custom, high-accuracy **Rule-Based Intelligence Engine**. Unlike chatbots that depend on external Large Language Models (LLMs) or paid cloud APIs, NovaAI achieves responsive and intelligent interaction through deterministic, lightweight computational linguistics:

- 🚫 **Zero External LLM APIs:** No OpenAI, ChatGPT, Google Gemini, Anthropic, or paid cloud APIs.
- ⚡ **Local & Deterministic:** Powered 100% by Python standard library algorithms and Flask.
- 🎯 **Confidence-Weighted Matching:** Multi-signal intent scoring (exact phrases, keywords, regex patterns, and emojis).
- 🧩 **Multi-Stage Text Normalization:** Robust informal shortform expansion, academic subject mapping, and lightweight typo tolerance.
- 🔒 **Privacy-First:** User data and chat histories remain strictly client-side via LocalStorage.

---

## ✨ Features

### 🧠 1. Chatbot Intelligence & NLP Pipeline
- **Intent-Based Architecture:** Modular knowledge registry supporting 40+ categorized intents and sub-intents.
- **Multi-Stage Normalization:** Token-safe normalization covering texting shortforms, slang, and technical abbreviations.
- **Academic Subject Mapping:** Automatic resolution of shortcuts (`bio`, `chem`, `phy`, `math`, `eng`, `cs`).
- **Technical Abbreviation Recognition:** Recognizes `AI`, `ML`, `API`, `HTML`, `CSS`, `JS`, `DSA`, `OOP`, `OS`, `CPU`, `GPU`, `RAM`, `DB`, `DBMS`, `SQL`.
- **Fuzzy Typo Tolerance:** Lightweight matching for common spelling errors (`pyhton`, `flsak`, `javscript`, `machin learning`, `algoritm`).
- **Emoji-Aware Sentiment Engine:** Understands standalone emojis, repeated emojis (`😂😂`, `🔥🔥`), and text + emoji combinations (`wht is ai 🤔`, `thx ❤️`).
- **Dynamic Solvers:** Built-in rule-based mathematical calculator, grammar error corrector, synonym/antonym finder, and vocabulary definer.
- **Varied Dynamic Responses:** Multiple natural response variations per intent to prevent repetitive conversations.
- **Graceful Fallback Handling:** Helpful fallback responses with contextual command recommendations.

### 📚 2. Multi-Domain Knowledge Base
- **💻 Programming:** Python, HTML, CSS, JavaScript, Flask, Git, GitHub, APIs, Databases, Algorithms, DSA, OOP.
- **🧠 Technology:** Artificial Intelligence, Machine Learning, AI vs. ML, Cloud Computing, Frontend, Backend, Operating Systems, Computer Hardware (CPU, GPU, RAM).
- **📐 Mathematics:** Arithmetic, Percentages, Fractions, Averages/Mean, Linear Equations (`solve 2x + 5 = 15`), Geometry formulas, Trigonometry, Unit Conversions.
- **🔬 Science:**
  - *Physics:* Force, Newton's 1st/2nd/3rd Laws, Speed & Velocity, Acceleration, Momentum, Work, Energy, Gravity, Sound, Light (Reflection & Refraction), Electricity, Ohm's Law.
  - *Chemistry:* Atoms, Molecules, Elements, Compounds, Mixtures, Periodic Table, Chemical Bonds (Ionic & Covalent), Acids, Bases, pH Scale, Oxidation, Reduction, Redox.
  - *Biology:* Cell Biology, DNA, RNA, Genetics, Photosynthesis, Human Body Systems (Circulatory, Respiratory, Nervous, Digestive), Ecosystems, Food Chains.
  - *General Science:* Solar System & Planets, Water Cycle, Renewable Energy, Greenhouse Effect, Scientific Method.
- **📖 English & Language:**
  - *Grammar:* Nouns, Verbs, Adjectives, Adverbs, Prepositions, Conjunctions, Active vs. Passive Voice.
  - *Tenses:* All 12 tenses (Present, Past, Future — Simple, Continuous, Perfect).
  - *Vocabulary:* Word definitions (`what does ephemeral mean`).
  - *Synonyms & Antonyms:* Direct lookups (`synonym of happy`, `opposite of difficult`).
  - *Sentence Correction:* Grammar mistake detection (`correct: She go to school.` ➔ `"She goes to school"`).
  - *Writing Basics:* Formal email writing structure, paragraph development, formal vs. informal tone.
- **🎯 Utilities:** Real-time clock (`time`), dynamic date (`date`), day of the week (`day`), programming jokes (`joke`), tech facts (`fun fact`), motivational advice (`motivate me`), inspirational quotes (`quote`).

### 🎨 3. Modern User Interface
- **Glassmorphism Aesthetic:** Frosted glass styling with layered backdrop filters and harmonious typography.
- **Responsive Layout:** Adaptive desktop, tablet, and mobile interface with fluid viewport scaling (`100dvh`).
- **Collapsible Sidebar:** Desktop and mobile sidebar containing conversation controls:
  - 📥 **Download Chat:** Export chat history as a formatted `.txt` transcript (*exclusive to sidebar*).
  - 🗑️ **Clear Chat:** Reset conversation history (*exclusive to sidebar*).
- **Voice Capabilities:**
  - 🎤 Speech-to-Text voice recognition via Web Speech API.
  - 🔊 Text-to-Speech bot response vocalization.
  - 🔈 Speaker ON/OFF toggle.
- **Interactive Controls:**
  - 😀 Modal Emoji Picker.
  - 📋 One-click message copying.
  - 🌓 Persistent Dark / Light Mode theme switcher.
  - 💬 Typing indicator animation and message timestamps.
  - 🛡️ Custom branded 404 Error page.

---

## 💬 Natural Language Understanding & Examples

NovaAI seamlessly handles variations, shortforms, abbreviations, and emojis:

| User Query | Detected Topic / Intent | Result |
| :--- | :--- | :--- |
| `who r u` | Conversational Intro | Introduces NovaAI and core capabilities |
| `wht is pyhton` | Programming | Explains Python's syntax, use cases, and ecosystem |
| `plz explain js` | Programming | Explains JavaScript for client and server |
| `wht is ai 🤔` | Technology | Explains Artificial Intelligence (prioritizes topic over confusion emoji) |
| `what is dsa` | Technology | Explains Data Structures and Algorithms |
| `what is oop` | Programming | Explains 4 pillars of Object-Oriented Programming |
| `bio help` | Academic Help | Displays Biology topics and guide |
| `wht is bio` | Science | Explains Biology as the study of life |
| `what is dna` | Science | Explains DNA structure, base pairs, and genes |
| `what is Newton's first law` | Science (Physics) | Explains Law of Inertia and force |
| `what is an atom` | Science (Chemistry) | Explains atomic structure (protons, neutrons, electrons) |
| `what is 20% of 500` | Mathematics | Computes `20% of 500 = 100` |
| `solve 2x + 5 = 15` | Mathematics | Solves linear equation step-by-step (`x = 5`) |
| `synonym of happy` | English & Language | Returns joyful, cheerful, glad, delighted, pleased |
| `opposite of difficult` | English & Language | Returns easy, simple, effortless |
| `correct: She go to school.` | English & Language | Corrects to `"She goes to school."` with grammatical explanation |
| `thx ❤️` | Conversational Sentiment | Returns polite acknowledgement (prioritizes thanks over heart emoji) |
| `bye 👋` | Conversational Farewell | Returns friendly goodbye response |

---

## 🔤 Supported Academic Subject Shortcuts

| Shortcut | Maps To | Dedicated Help Command |
| :--- | :--- | :--- |
| `bio` | Biology | `bio help` |
| `phy` / `phys` | Physics | `phy help` |
| `chem` | Chemistry | `chem help` |
| `math` / `maths` | Mathematics | `math help` / `maths help` |
| `eng` | English & Language | `eng help` |
| `cs` / `comp sci` | Computer Science | `cs help` |

---

## 🏗️ Architecture

```text
User Message (Web Interface / Voice Input)
                  ↓
          HTTP POST /chat
                  ↓
       [Text Normalization Pipeline]
    • Lowercasing & Character De-duplication
    • Emoji Extraction & Sentiment Classification
    • Texting Shortform Expansion (u -> you, wht -> what)
    • Academic Subject Resolution (bio -> biology, phy -> physics)
    • Technical Abbreviation Mapping (dsa -> data structures & algorithms)
    • Lightweight Fuzzy Typo Tolerance (pyhton -> python)
                  ↓
       [Rule-Based Evaluation Engine]
    • Direct Math Expression & Formula Solvers
    • Dynamic Grammar, Synonym & Vocabulary Handlers
    • Multi-Signal Confidence Scoring (Phrases, Keywords, Regex, Emojis)
                  ↓
       [Knowledge Base Lookup & Response Selection]
    • Programming • Technology • Mathematics
    • Science (Physics, Chemistry, Biology, General Science)
    • English & Language • Utilities • Fallbacks
                  ↓
          JSON Reply Payload
                  ↓
Client UI Rendering (HTML/CSS/JS + TTS Audio + LocalStorage)
```

---

## 🛠️ Tech Stack

| Domain | Technologies |
| :--- | :--- |
| **Backend** | Python 3.12+, Flask 3.1, Gunicorn |
| **NLP Engine** | Pure Python Standard Library (`re`, `difflib`, `math`, `datetime`, `random`) |
| **Frontend** | HTML5, CSS3 (Modern Flexbox, CSS Grid, Glassmorphism, CSS Variables), Vanilla JavaScript (ES6+) |
| **Browser APIs** | Web Speech API (`SpeechRecognition`, `SpeechSynthesis`), Web Storage API (`localStorage`) |
| **Deployment** | Render Web Services |
| **Version Control** | Git & GitHub |

---

## 🔌 API Documentation

NovaAI exposes a clean, lightweight REST API endpoint:

### Endpoint: `POST /chat`

#### Request:
- **Headers:** `Content-Type: application/json`
- **Body:**
```json
{
  "message": "wht is bio 🤔"
}
```

#### Response:
- **Status:** `200 OK`
- **Body:**
```json
{
  "reply": "🧬 **Biology** is the natural science that studies life and living organisms, including their physical structure, chemical processes, molecular interactions, cellular mechanics, physiological adaptations, and evolution!"
}
```

---

## 📂 Project Structure

```text
NovaAI/
├── app.py                     # Flask application routes (/ and /chat) & server configuration
├── chatbot.py                 # Core rule-based intelligence engine, knowledge base & solvers
├── config.py                  # Environment & server settings
├── requirements.txt           # Production Python dependencies (Flask, Gunicorn)
├── architecture.md            # Architectural specification document
├── design.md                  # UI/UX design and styling documentation
├── README.md                  # Project documentation
│
├── templates/
│   ├── index.html             # Main responsive glassmorphism UI with collapsible sidebar
│   └── 404.html               # Custom error page
│
└── static/
    ├── css/
    │   ├── base.css           # Global reset, typography, and background
    │   ├── layout.css         # Glassmorphism container, header, footer & sidebar layouts
    │   ├── chat.css           # Chat bubbles, avatars, message formatting, timestamps
    │   ├── buttons.css        # Action buttons, icons, and interactive hover states
    │   ├── emoji.css          # Emoji picker grid modal
    │   ├── theme.css          # Dark and light mode color variables
    │   ├── responsive.css     # Mobile and tablet breakpoints
    │   ├── animations.css     # Aurora background, typing indicators, pulse effects
    │   └── style.css          # Master stylesheet imports
    │
    ├── js/
    │   ├── app.js             # Main frontend orchestrator & event listeners
    │   ├── chat.js            # Message sending, receiving, bubble rendering & copy logic
    │   ├── storage.js         # LocalStorage persistence for chat history & theme
    │   ├── theme.js           # Theme switching and preference management
    │   ├── voice.js           # Speech-to-Text input handling
    │   ├── speech.js          # Text-to-Speech vocalization & speaker toggle
    │   ├── emoji.js           # Emoji picker modal & insertion
    │   ├── download.js        # Chat export as formatted text file
    │   └── clock.js           # Header real-time clock
    │
    └── images/
        ├── favicon.ico        # Browser favicon
        └── nova-avatar.png    # NovaAI bot avatar graphic
```

---

## ⚙️ Installation & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/urishitaarora-web/DecodeLabs-Internship.git
```

### 2. Navigate to the NovaAI Directory
```bash
cd DecodeLabs-Internship/NovaAI
```

### 3. Create & Activate a Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Start the Application
```bash
python app.py
```

### 6. Open in Browser
Open your browser and navigate to:
```text
http://127.0.0.1:5000
```

---

## ☁️ Render Deployment

NovaAI is configured for instant deployment on [Render](https://render.com/):

1. **Service Type:** Web Service
2. **Environment:** Python 3
3. **Build Command:** `pip install -r requirements.txt`
4. **Start Command:** `gunicorn app:app` (or `python app.py`)
5. **Root Directory:** `NovaAI`

---

## 🧪 Testing & Verification

NovaAI includes automated verification test scripts. Key test cases include:

- **Conversational Shortforms:** `hello`, `who r u`, `hw r u`, `gud morning`, `thx nova`
- **Programming Queries:** `wht is pyhton`, `plz explain js`, `tell me abt html`, `wht is css`
- **Technology Queries:** `wht is ai`, `explain ml`, `what is api`, `what is db`, `what is dsa`, `what is oop`
- **Mathematics Calculations:** `25 + 35`, `20% of 500`, `solve 2x + 5 = 15`, `area of a circle`, `math help`
- **Science Knowledge:** `what is gravity`, `wht is bio`, `bio help`, `chem help`, `phy help`, `what is dna`, `what is an atom`
- **English & Language:** `wht is a noun`, `plz explain tenses`, `synonym of happy`, `opposite of difficult`, `correct: She go to school.`
- **Emojis & Combinations:** `😊`, `😂😂`, `❤️`, `wht is ai 🤔`, `plz explain bio 🧬`, `tell me abt python 👍`, `bye 👋`

---

## 🎯 Design Philosophy

- **Deterministic & Safe:** Every answer is grounded in curated rule sets, eliminating hallucinations and unpredictable model outputs.
- **Resource Efficient:** Near-instant sub-millisecond response times with minimal CPU and memory footprints.
- **Maintainable & Modular:** Organized into discrete domain intents and language solvers, allowing new subjects to be added seamlessly.
- **User-Centric UI:** Clean desktop layout, collapsible sidebar, accessible typography, and smooth glassmorphism animations.

---

## 🔮 Future Improvements

- 📈 Expanding vocabulary dictionary and synonyms database.
- 📐 Additional geometric formulas and multi-step word problem solvers.
- 🧪 Extended organic chemistry and advanced physics kinematics topics.
- 🌍 Multi-language greeting and translation support.

---

## 👩‍💻 Author

**Urishita Arora**  
- GitHub: [@urishitaarora-web](https://github.com/urishitaarora-web)

---

## 📜 License

This project is licensed under the **MIT License**.
