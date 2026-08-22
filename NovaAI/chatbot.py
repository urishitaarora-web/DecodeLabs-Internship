"""
NovaAI Advanced Rule-Based Intelligence Engine
================================================
A modular, high-accuracy, rule-based chatbot engine featuring:
- Multi-stage text normalization, informal shortform expansion & typo handling
- Academic subject & technical abbreviation recognition
- Emoji-aware intent detection & sentiment signaling
- Confidence-weighted intent scoring & matching
- Rich categorized knowledge base across 6 core domains:
  1. 💻 Programming
  2. 🧠 Technology
  3. 📐 Mathematics
  4. 🔬 Science (Physics, Chemistry, Biology, General Science)
  5. 📖 English & Language (Grammar, Tenses, Vocabulary, Synonyms, Antonyms, Corrections, Writing)
  6. 🎯 Utilities
- Safe rule-based mathematical calculator & problem solver
- Dynamic English grammar correction, synonym/antonym finder, vocabulary definer
- Dynamic utilities (Time, Date, Day)
- Contextual categorized help system with academic & subject shortcut support
- Varied dynamic fallback & conversational responses
"""

from datetime import datetime
import difflib
import math
import random
import re
from typing import Callable, Dict, List, Optional, Set, Tuple, Union

# =============================================================================
# 1. KNOWLEDGE BASE & STATIC DATA
# =============================================================================

JOKES: List[str] = [
    "😂 Why do programmers prefer dark mode? Because light attracts bugs!",
    "😄 Why did the JavaScript developer wear glasses? Because they didn't C#!",
    "🤣 There are 10 types of people in the world: those who understand binary, and those who don't.",
    "🤖 Why was the computer cold? It left its Windows open!",
    "☕ A programmer's spouse asks: 'Could you go to the store and buy a loaf of bread? If they have eggs, buy a dozen.' The programmer returns with 12 loaves of bread.",
    "🐛 It's not a bug – it's an undocumented feature!",
    "😅 Why do Python developers get into trouble? Because they have too many tabs open!",
    "🧠 An SQL query walks into a bar, walks up to two tables and asks: 'Can I join you?'"
]

FUN_FACTS: List[str] = [
    "💡 The first computer bug was an actual real moth found trapped inside the Harvard Mark II computer in 1947!",
    "💡 The first 1GB hard drive was released by IBM in 1980 — it weighed about 550 pounds and cost $40,000.",
    "💡 Python was named after the British comedy troupe 'Monty Python', not the snake!",
    "💡 Over 90% of the world's currency exists only in digital form on computers.",
    "💡 JavaScript was created in just 10 days in May 1995 by Brendan Eich at Netscape.",
    "💡 The first domain name ever registered was 'symbolics.com' on March 15, 1985.",
    "💡 Ada Lovelace is widely considered the world's first computer programmer for her work on Charles Babbage's mechanical computer in the 1840s.",
    "💡 GitHub hosts over 100 million developers and hundreds of millions of repositories worldwide."
]

MOTIVATIONS: List[str] = [
    "🚀 'The only way to learn a new programming language is by writing programs in it.' — Dennis Ritchie",
    "🌟 Every expert was once a beginner. Consistency and curiosity will take you further than talent alone!",
    "🔥 Small daily improvements over time lead to stunning results. Keep coding, keep building!",
    "💪 Debugging is just being the detective in a crime movie where you are also the murderer. Don't give up!",
    "✨ You don't have to be great to start, but you have to start to be great. Keep pushing forward!",
    "⚡ 'First, solve the problem. Then, write the code.' — John Johnson",
    "🌈 Trust the process. Every error message is a stepping stone toward mastering your craft."
]

QUOTES: List[str] = [
    "🌟 'Programs must be written for people to read, and only incidentally for machines to execute.' — Harold Abelson",
    "💡 'Simplicity is prerequisite for reliability.' — Edsger W. Dijkstra",
    "🚀 'Talk is cheap. Show me the code.' — Linus Torvalds",
    "🔥 'Make it work, make it right, make it fast.' — Kent Beck",
    "✨ 'Stay hungry, stay foolish.' — Steve Jobs",
    "💻 'Any fool can write code that a computer can understand. Good programmers write code that humans can understand.' — Martin Fowler",
    "🎯 'The best error message is the one that never shows up.' — Thomas Fuchs"
]

FALLBACK_RESPONSES: List[str] = [
    "🤔 I'm not sure about that yet. Type **help** to explore the topics and commands I support!",
    "💡 I don't have information on that topic yet, but I can help with programming, technology, mathematics, science, English, and utilities. Type **help** to see what I can do!",
    "🤖 That topic is currently outside my knowledge base. Try asking about **Python**, **Science**, **Math**, **English Grammar**, or type **help** for a full guide.",
    "🔍 I couldn't quite match that with my rule base. Type **help** to check available commands or try rephrasing!"
]

HELP_GENERAL: str = (
    "📚 **NovaAI Knowledge & Capabilities Guide**\n\n"
    "💻 **Programming**\n"
    "• Python  • HTML  • CSS  • JavaScript\n"
    "• Flask   • Git   • GitHub • APIs\n"
    "• Databases  • Algorithms\n\n"
    "🧠 **Technology**\n"
    "• Artificial Intelligence  • Machine Learning\n"
    "• Difference between AI and ML\n"
    "• Cloud Computing  • Frontend  • Backend\n"
    "• DSA  • OOP  • Operating Systems\n\n"
    "📐 **Mathematics**\n"
    "• Arithmetic  • Percentages  • Fractions\n"
    "• Algebra  • Geometry  • Statistics\n"
    "• Trigonometry  • Unit Conversions\n\n"
    "🔬 **Science**\n"
    "• Physics  • Chemistry  • Biology  • General Science\n\n"
    "📖 **English & Language**\n"
    "• Grammar  • Tenses  • Vocabulary  • Synonyms\n"
    "• Antonyms  • Sentence Correction  • Writing Basics\n\n"
    "🎯 **Utilities**\n"
    "• Time  • Date  • Day  • Joke\n"
    "• Fun Fact  • Quote  • Motivation\n\n"
    "💡 *Try asking:*\n"
    "• \"What is Python?\"\n"
    "• \"What is Newton's first law?\"\n"
    "• \"What is an atom?\"\n"
    "• \"What is DNA?\"\n"
    "• \"What is a noun?\"\n"
    "• \"Synonym of happy\"\n"
    "• \"Solve 2x + 5 = 15\"\n\n"
    "📌 *Topic-specific help:* Type `programming help` (or `cs help`), `technology help`, `math help`, `science help` (`bio help`, `chem help`, `phy help`), `english help` (`eng help`), or `utility help`."
)

HELP_PROGRAMMING: str = (
    "💻 **Programming Help & Topics**\n\n"
    "You can ask me questions such as:\n"
    "• What is Python?\n"
    "• What is HTML / CSS?\n"
    "• What is JavaScript?\n"
    "• What is Flask?\n"
    "• What is Git / GitHub?\n"
    "• What is an API?\n"
    "• What is a database?\n"
    "• What is an algorithm?\n"
    "• What is DSA / OOP?\n\n"
    "✨ Just type the question or topic name directly!"
)

HELP_TECHNOLOGY: str = (
    "🧠 **Technology Help & Topics**\n\n"
    "You can ask me questions such as:\n"
    "• What is Artificial Intelligence (AI)?\n"
    "• What is Machine Learning (ML)?\n"
    "• Difference between AI and ML?\n"
    "• What is Cloud Computing?\n"
    "• What is Frontend / Backend Development?\n"
    "• What is an Operating System (OS)?\n"
    "• What is CPU / GPU / RAM?\n\n"
    "✨ Ask any of these topics to learn more!"
)

HELP_MATHEMATICS: str = (
    "📐 **Mathematics Help & Commands**\n\n"
    "I can help with various mathematical calculations and concepts:\n\n"
    "• **Basic Arithmetic:** `25 * 8`, `150 + 75`, `124 / 4`, `2^10`, `sqrt(144)`\n"
    "• **Percentages:** `20% of 500`, `15% off 80`\n"
    "• **Fractions & Ratios:** Simplifying & converting proportions\n"
    "• **Averages & Statistics:** `average of 10, 20, 30, 40`\n"
    "• **Basic Algebra:** Linear equations (`solve 2x + 5 = 15`)\n"
    "• **Geometry:** Area & perimeter of circle, triangle, rectangle, sphere\n"
    "• **Basic Trigonometry:** `sin(30)`, `cos(45)`, `tan(60)`\n"
    "• **Unit Conversions:** `10 km to miles`, `100 celsius to fahrenheit`, `5 kg to lbs`\n\n"
    "✨ *Try asking:*\n"
    "• \"What is 25 × 8?\"\n"
    "• \"What is 20% of 500?\"\n"
    "• \"Solve 2x + 5 = 15\"\n"
    "• \"What is the area of a circle?\"\n"
    "• \"What is the average of 10, 20 and 30?\""
)

HELP_SCIENCE: str = (
    "🔬 **Science Help & Topics**\n\n"
    "I can help with concepts across all major branches of science:\n\n"
    "• **Physics (`phy help`):** Motion, Force, Newton's Laws, Energy, Gravity, Sound, Light, Electricity, Ohm's Law\n"
    "• **Chemistry (`chem help`):** Atoms, Molecules, Elements, Compounds, Periodic Table, Chemical Bonds, Acids, Bases, pH, Chemical Reactions\n"
    "• **Biology (`bio help`):** Cell Structure, DNA, Genetics, Human Body Systems (Heart, Brain, Lungs), Photosynthesis, Ecosystems\n"
    "• **General Science:** Solar System, Water Cycle, Renewable Energy, Greenhouse Effect, Scientific Method\n\n"
    "💡 *Try asking:*\n"
    "• \"What is Newton's first law?\"\n"
    "• \"What is an atom?\"\n"
    "• \"What is DNA?\"\n"
    "• \"What is photosynthesis?\"\n"
    "• \"What is the water cycle?\"\n\n"
    "📌 *Sub-topic shortcuts:* Type `phy help`, `chem help`, or `bio help`."
)

HELP_PHYSICS: str = (
    "⚛️ **Physics Help & Topics**\n\n"
    "Ask me about physical laws, forces, and motion:\n\n"
    "• **Motion & Kinematics:** Speed, Velocity, Acceleration, Momentum\n"
    "• **Forces & Dynamics:** Force, Newton's 1st/2nd/3rd Laws, Gravity, Friction, Mass vs Weight\n"
    "• **Work & Energy:** Work, Kinetic Energy, Potential Energy, Power, Conservation of Energy\n"
    "• **Waves & Light:** Sound Waves, Light, Reflection, Refraction\n"
    "• **Electricity & Magnetism:** Current, Voltage, Resistance, Ohm's Law, Magnetic Fields\n\n"
    "✨ *Try asking:*\n"
    "• \"What is force?\"\n"
    "• \"What is Newton's first law?\"\n"
    "• \"What is Ohm's law?\"\n"
    "• \"What is kinetic energy?\""
)

HELP_CHEMISTRY: str = (
    "🧪 **Chemistry Help & Topics**\n\n"
    "Ask me about matter, reactions, and chemical structures:\n\n"
    "• **Atomic Structure:** Atoms, Molecules, Protons, Neutrons, Electrons, Atomic Number\n"
    "• **Matter & Elements:** Elements, Compounds, Mixtures, Periodic Table, States of Matter\n"
    "• **Chemical Bonds:** Ionic Bonds, Covalent Bonds\n"
    "• **Solutions & Reactions:** Acids, Bases, pH Scale, Oxidation, Reduction, Redox\n\n"
    "✨ *Try asking:*\n"
    "• \"What is an atom?\"\n"
    "• \"What is pH?\"\n"
    "• \"What is a covalent bond?\"\n"
    "• \"What is oxidation?\""
)

HELP_BIOLOGY: str = (
    "🧬 **Biology Help & Topics**\n\n"
    "Ask me about living organisms, genetics, and ecology:\n\n"
    "• **Cellular Biology:** Cell Structure, Nucleus, Organelles\n"
    "• **Genetics:** DNA, RNA, Genes, Chromosomes\n"
    "• **Human Body Systems:** Digestive, Respiratory, Circulatory, Nervous Systems, Heart, Brain\n"
    "• **Plant Biology:** Photosynthesis, Chlorophyll\n"
    "• **Ecology:** Ecosystems, Food Chains, Producers, Consumers, Decomposers, Biodiversity\n\n"
    "✨ *Try asking:*\n"
    "• \"What is a cell?\"\n"
    "• \"What is DNA?\"\n"
    "• \"What is photosynthesis?\"\n"
    "• \"What does the heart do?\""
)

HELP_ENGLISH: str = (
    "📖 **English & Language Help & Capabilities**\n\n"
    "I can help with English grammar, vocabulary, writing, and corrections:\n\n"
    "• **Grammar:** Nouns, Pronouns, Verbs, Adjectives, Adverbs, Prepositions, Conjunctions, Articles\n"
    "• **Tenses:** Present, Past, and Future Tenses (Simple, Continuous, Perfect)\n"
    "• **Voice & Speech:** Active vs Passive Voice, Direct vs Indirect Speech\n"
    "• **Vocabulary & Definitions:** `what does ephemeral mean`, `meaning of lucid`\n"
    "• **Synonyms & Antonyms:** `synonym of happy`, `opposite of difficult`\n"
    "• **Sentence Correction:** `correct: She go to school.`\n"
    "• **Writing Basics:** Paragraph writing, Formal vs Informal emails, Introductions\n\n"
    "💡 *Try asking:*\n"
    "• \"What is a noun?\"\n"
    "• \"Give me a synonym for happy\"\n"
    "• \"What's the opposite of difficult?\"\n"
    "• \"Correct: She go to school\"\n"
    "• \"How do I write a formal email?\"\n\n"
    "📌 *Sub-topic help:* Type `grammar help` or `vocabulary help`."
)

HELP_GRAMMAR: str = (
    "📝 **English Grammar Help**\n\n"
    "Ask me about parts of speech, tenses, and sentence structures:\n\n"
    "• **Parts of Speech:** Nouns, Verbs, Adjectives, Adverbs, Prepositions, Conjunctions, Articles\n"
    "• **Tenses:** Present Simple/Continuous/Perfect, Past Tenses, Future Tenses\n"
    "• **Voice:** Active Voice, Passive Voice\n"
    "• **Sentence Correction:** Type `correct: [your sentence]` to check grammar\n\n"
    "✨ *Try asking:*\n"
    "• \"What is a verb?\"\n"
    "• \"Explain present continuous tense\"\n"
    "• \"What is passive voice?\""
)

HELP_VOCABULARY: str = (
    "📚 **English Vocabulary, Synonyms & Antonyms**\n\n"
    "Here is how to use my language tools:\n\n"
    "• **Definitions:** `what does [word] mean` (e.g., `what does serendipity mean`)\n"
    "• **Synonyms:** `synonym of [word]` (e.g., `synonym of happy`, `another word for fast`)\n"
    "• **Antonyms:** `opposite of [word]` (e.g., `opposite of hot`, `antonym of difficult`)\n\n"
    "✨ *Try asking:*\n"
    "• \"Synonyms for important\"\n"
    "• \"Opposite of early\"\n"
    "• \"Meaning of resilient\""
)

HELP_UTILITIES: str = (
    "🎯 **Utilities Help & Commands**\n\n"
    "Here are handy utilities you can run anytime:\n\n"
    "• `time` / `what time is it` — Current server time\n"
    "• `date` / `what is today's date` — Today's date\n"
    "• `day` / `what day is today` — Current day of the week\n"
    "• `joke` / `tell me a joke` — Programming & tech jokes\n"
    "• `fun fact` / `tell me a fun fact` — Fascinating tech facts\n"
    "• `quote` / `give me a quote` — Inspiring tech quotes\n"
    "• `motivate me` / `motivation` — Uplifting motivational advice"
)

# =============================================================================
# 2. DICTIONARIES FOR SYNONYMS, ANTONYMS, VOCABULARY & CORRECTION
# =============================================================================

SYNONYMS_DB: Dict[str, List[str]] = {
    "happy": ["joyful", "cheerful", "glad", "delighted", "pleased", "ecstatic"],
    "sad": ["unhappy", "sorrowful", "depressed", "downhearted", "gloomy", "mournful"],
    "big": ["large", "huge", "enormous", "gigantic", "massive", "immense"],
    "small": ["tiny", "little", "miniature", "compact", "petite", "minute"],
    "smart": ["intelligent", "clever", "bright", "brilliant", "sharp", "wise"],
    "intelligent": ["smart", "clever", "brilliant", "intellectual", "astute", "sharp"],
    "fast": ["quick", "rapid", "speedy", "swift", "brisk", "fleet"],
    "slow": ["sluggish", "unhurried", "leisurely", "gradual", "delayed"],
    "important": ["significant", "crucial", "essential", "vital", "critical", "meaningful"],
    "difficult": ["hard", "challenging", "tough", "complex", "demanding", "arduous"],
    "easy": ["simple", "effortless", "straightforward", "uncomplicated", "painless"],
    "strong": ["powerful", "mighty", "robust", "sturdy", "resilient", "tough"],
    "weak": ["fragile", "frail", "feeble", "delicate", "vulnerable"],
    "beautiful": ["gorgeous", "attractive", "stunning", "pretty", "handsome", "lovely"],
    "brave": ["courageous", "fearless", "valiant", "bold", "heroic", "daring"],
    "calm": ["peaceful", "serene", "tranquil", "quiet", "composed", "relaxed"],
    "angry": ["furious", "mad", "irate", "enraged", "annoyed", "livid"],
    "bright": ["shining", "radiant", "luminous", "brilliant", "vivid", "gleaming"],
    "dark": ["dim", "shadowy", "gloomy", "murky", "obscure", "black"],
    "rich": ["wealthy", "affluent", "prosperous", "opulent", "loaded"],
    "poor": ["needy", "impoverished", "destitute", "penniless", "disadvantaged"],
    "clean": ["neat", "spotless", "tidy", "pure", "immaculate", "hygienic"],
    "dirty": ["soiled", "messy", "unclean", "grimy", "filthy", "polluted"],
    "love": ["affection", "adoration", "fondness", "devotion", "care", "warmth"],
    "hate": ["loathe", "detest", "despise", "abhor", "dislike"],
    "good": ["excellent", "fine", "superb", "great", "wonderful", "pleasant"],
    "bad": ["terrible", "awful", "poor", "inferior", "dreadful", "harmful"],
    "honest": ["truthful", "sincere", "frank", "candid", "trustworthy", "genuine"],
    "kind": ["generous", "compassionate", "benevolent", "thoughtful", "caring", "gentle"],
    "new": ["fresh", "modern", "recent", "novel", "current", "latest"],
    "old": ["ancient", "aged", "elderly", "antique", "mature", "vintage"],
    "begin": ["start", "commence", "initiate", "launch", "open"],
    "finish": ["complete", "conclude", "terminate", "end", "wrap up"],
    "help": ["assist", "aid", "support", "serve", "guide", "back"],
}

ANTONYMS_DB: Dict[str, List[str]] = {
    "happy": ["sad", "unhappy", "depressed", "miserable"],
    "sad": ["happy", "cheerful", "joyful", "glad"],
    "hot": ["cold", "chilly", "freezing", "cool"],
    "cold": ["hot", "warm", "heated"],
    "big": ["small", "tiny", "little", "miniature"],
    "small": ["big", "large", "huge", "gigantic"],
    "smart": ["foolish", "stupid", "unwise", "dumb"],
    "fast": ["slow", "sluggish", "gradual"],
    "slow": ["fast", "quick", "rapid", "speedy"],
    "difficult": ["easy", "simple", "effortless"],
    "easy": ["difficult", "hard", "complex", "challenging"],
    "hard": ["soft", "easy", "simple"],
    "soft": ["hard", "rough", "firm", "stiff"],
    "early": ["late", "delayed", "overdue"],
    "late": ["early", "punctual", "timely"],
    "strong": ["weak", "frail", "fragile", "feeble"],
    "weak": ["strong", "powerful", "robust", "mighty"],
    "rich": ["poor", "impoverished", "destitute"],
    "poor": ["rich", "wealthy", "affluent"],
    "brave": ["cowardly", "fearful", "timid"],
    "light": ["dark", "heavy"],
    "dark": ["light", "bright"],
    "good": ["bad", "evil", "poor"],
    "bad": ["good", "great", "excellent"],
    "true": ["false", "untrue", "incorrect"],
    "false": ["true", "correct", "accurate"],
    "love": ["hate", "loathing", "detestation"],
    "hate": ["love", "affection", "adoration"],
    "win": ["lose", "defeat", "fail"],
    "lose": ["win", "gain", "triumph"],
    "begin": ["end", "finish", "conclude"],
    "finish": ["start", "begin", "initiate"],
    "clean": ["dirty", "soiled", "messy"],
    "dirty": ["clean", "spotless", "neat"],
}

VOCABULARY_DB: Dict[str, str] = {
    "ephemeral": "lasting for a very short time; fleeting or transitory.",
    "ubiquitous": "present, appearing, or found everywhere simultaneously; omnipresent.",
    "pragmatic": "dealing with things sensibly and realistically based on practical rather than theoretical considerations.",
    "serendipity": "the occurrence of events by chance in a happy, beneficial, or unexpected way.",
    "eloquent": "fluent, persuasive, and expressive in speaking or writing.",
    "resilient": "able to withstand or recover quickly from difficult conditions or adversity.",
    "meticulous": "showing great attention to detail; very careful and precise.",
    "candid": "truthful and straightforward; frank and honest.",
    "nostalgia": "a sentimental longing or affection for the past.",
    "benevolent": "well meaning, kindly, and charitable.",
    "empathy": "the ability to understand and share the feelings, emotions, or perspective of another person.",
    "integrity": "the quality of being honest and having strong moral principles; uprightness.",
    "paradox": "a seemingly absurd or self-contradictory statement or proposition that when investigated proves to be well founded or true.",
    "lucid": "expressed clearly; easy to understand; or having clear and rational thinking.",
    "ambiguous": "open to more than one interpretation; having a double or unclear meaning.",
    "tenacious": "tending to keep a firm hold of something; clinging or adhering closely; persistent and determined.",
    "aesthetic": "concerned with beauty or the appreciation of beauty and artistic taste.",
    "catalyst": "a person, thing, or substance that precipitates an event or accelerates a chemical reaction without itself being consumed.",
    "emulate": "to match or surpass a person or achievement, typically by imitation; to copy with effort to equal or excel.",
    "superfluous": "unnecessary, especially through being more than enough; excessive.",
    "important": "of great significance, consequence, or value; having profound effect.",
    "algorithm": "a step-by-step procedure or set of rules to be followed in calculations or problem-solving operations.",
    "photosynthesis": "the biological process by which green plants and some organisms use sunlight to synthesize nutrients from carbon dioxide and water.",
    "gravity": "the universal force of attraction acting between all matter possessing mass or energy.",
    "democracy": "a system of government by the whole population or all the eligible members of a state, typically through elected representatives.",
}

SENTENCE_CORRECTIONS: List[Tuple[str, str, str]] = [
    (
        r"\b(she|he|it)\s+go\s+to\b",
        r"\1 goes to",
        "With third-person singular subjects ('he', 'she', 'it'), use the singular verb form 'goes' instead of 'go'."
    ),
    (
        r"\b(i)\s+has\b",
        r"I have",
        "With the first-person pronoun 'I', use 'have' instead of 'has'."
    ),
    (
        r"\b(you|we|they)\s+has\b",
        r"\1 have",
        "With plural pronouns ('you', 'we', 'they'), use 'have' instead of 'has'."
    ),
    (
        r"\b(he|she|it)\s+don't\b",
        r"\1 doesn't",
        "With third-person singular subjects ('he', 'she', 'it'), use 'doesn't' (does not) instead of 'don't'."
    ),
    (
        r"\b(he|she|it)\s+dont\b",
        r"\1 doesn't",
        "With third-person singular subjects ('he', 'she', 'it'), use 'doesn't' instead of 'dont'."
    ),
    (
        r"\b(they|we|you)\s+is\b",
        r"\1 are",
        "With plural pronouns ('they', 'we', 'you'), use 'are' instead of 'is'."
    ),
    (
        r"\b(i)\s+is\b",
        r"I am",
        "With the first-person pronoun 'I', use 'am' instead of 'is'."
    ),
    (
        r"\b(i)\s+seen\s+him\b",
        r"I saw him",
        "Use the simple past tense 'saw' rather than the past participle 'seen' without an auxiliary verb."
    ),
    (
        r"\ban\s+(university|uniform|unique|european|user)\b",
        r"a \1",
        "Words beginning with a consonant sound (like the 'y' sound in 'university' or 'uniform') take the article 'a', not 'an'."
    ),
    (
        r"\ba\s+(hour|honest|honor|heir)\b",
        r"an \1",
        "Words with a silent 'h' begin with a vowel sound and take the article 'an', not 'a'."
    ),
]

# =============================================================================
# 3. EMOJI DETECTION & NORMALIZATION
# =============================================================================

EMOJI_PATTERN = re.compile(
    r"["
    r"\U0001F600-\U0001F64F"  # Emoticons
    r"\U0001F300-\U0001F5FF"  # Misc Symbols & Pictographs
    r"\U0001F680-\U0001F6FF"  # Transport & Map
    r"\U0001F1E0-\U0001F1FF"  # Regional Flags
    r"\U00002700-\U000027BF"  # Dingbats (includes heavy black heart \u2764)
    r"\U0001F900-\U0001F9FF"  # Supplemental Symbols
    r"\U0001FA70-\U0001FAFF"  # Symbols & Pictographs Extended-A
    r"\U00002600-\U000026FF"  # Misc Symbols (sun, heart, etc.)
    r"\U0001F000-\U0001F02F"
    r"][\U0000FE00-\U0000FE0F\U0001F3FB-\U0001F3FF]?",
    flags=re.UNICODE
)


def normalize_emoji(e: str) -> str:
    """Normalizes an emoji by stripping variation selectors and skin tone modifiers."""
    if not e:
        return ""
    e = e.replace("\ufe0f", "").replace("\ufe0e", "")
    e = re.sub(r"[\U0001F3FB-\U0001F3FF]", "", e)
    return e.strip()


def extract_emojis(text: str) -> List[str]:
    """Extracts all distinct normalized emojis from raw input text."""
    if not text:
        return []
    matches = EMOJI_PATTERN.findall(text)
    cleaned_emojis = []
    for m in matches:
        norm = normalize_emoji(m)
        if norm:
            cleaned_emojis.append(norm)
    return cleaned_emojis


# Comprehensive mapping of texting shortforms, informal abbreviations & typos
SLANG_MAP: Dict[str, str] = {
    # Pronouns & Verbs
    "u": "you",
    "ur": "your",
    "r": "are",
    "y": "why",
    "wht": "what",
    "wat": "what",
    "abt": "about",
    "bcz": "because",
    "bc": "because",
    "pls": "please",
    "plz": "please",
    "plzz": "please",
    "thx": "thanks",
    "tx": "thanks",
    "thnks": "thanks",
    "thnxx": "thanks",
    "msg": "message",
    "info": "information",
    "hw": "how",
    "wbu": "what about you",
    "hbu": "how about you",
    "idk": "i do not know",
    "ikr": "i know right",
    "btw": "by the way",
    "brb": "be right back",
    "omg": "oh my god",
    "lol": "laugh",
    "lmao": "laugh",
    "rofl": "laugh",
    "tbh": "to be honest",
    "imo": "in my opinion",
    "imho": "in my humble opinion",
    "np": "no problem",
    "yw": "you are welcome",
    "asap": "as soon as possible",
    "fyi": "for your information",
    "rn": "right now",
    "ppl": "people",
    "b4": "before",
    "2day": "today",
    "tmrw": "tomorrow",
    "2moro": "tomorrow",
    "gud": "good",
    "helo": "hello",
    "helloo": "hello",
    "heyy": "hey",
    "heyyy": "hey",
    "hii": "hi",
    "hiii": "hi",
    "hiiii": "hi",
    "k": "ok",
    "im": "i am",
    "i'm": "i am",
    "tell me bout": "tell me about",
    "bout": "about",
    "machin": "machine",
    "pyhton": "python",
    "javscript": "javascript",
    "flsak": "flask",
    "algoritm": "algorithm",
    "databse": "database",
    "gthub": "github",
    "gihub": "github",
    "lets": "let us",
    "let's": "let us",
    "dont": "do not",
    "don't": "do not",
    "whats": "what is",
    "what's": "what is",
    "who's": "who is",
    "whos": "who is",
    "hows": "how is",
    "how's": "how is",
}

# Academic Subject Abbreviations (Safe token replacement)
ACADEMIC_SUBJECT_MAP: Dict[str, str] = {
    "bio": "biology",
    "phy": "physics",
    "phys": "physics",
    "chem": "chemistry",
    "math": "mathematics",
    "maths": "mathematics",
    "eng": "english",
    "cs": "computer science",
}

# Technical Abbreviations Mapping
TECH_ABBREVIATION_MAP: Dict[str, str] = {
    "dsa": "data structures and algorithms",
    "oop": "object oriented programming",
    "os": "operating system",
    "cpu": "central processing unit",
    "gpu": "graphics processing unit",
    "ram": "random access memory",
    "url": "uniform resource locator",
    "http": "hypertext transfer protocol",
    "https": "hypertext transfer protocol secure",
    "json": "javascript object notation",
    "ui": "user interface",
    "ux": "user experience",
    "dbms": "database management system",
    "sql": "structured query language",
    "db": "database",
    "ai": "artificial intelligence",
    "ml": "machine learning",
    "api": "application programming interface",
    "html": "hypertext markup language",
    "css": "cascading style sheets",
    "js": "javascript",
}

CANONICAL_VOCABULARY: List[str] = [
    "python", "javascript", "flask", "html", "css", "git", "github",
    "algorithm", "database", "api", "artificial", "intelligence", "machine",
    "learning", "cloud", "computing", "frontend", "backend", "joke", "quote",
    "motivation", "fact", "time", "date", "hello", "thanks", "help",
    "about", "developer", "version", "happy", "angry", "sad", "confused",
    "celebrate", "awesome", "great", "math", "mathematics", "algebra",
    "geometry", "percentage", "average", "arithmetic", "science", "physics",
    "chemistry", "biology", "english", "grammar", "vocabulary", "synonym",
    "antonym", "gravity", "photosynthesis", "velocity", "acceleration"
]


def normalize_repeated_chars(text: str) -> str:
    """Compress excessive repeated characters while preserving valid double letters."""
    text = re.sub(r"\bhi{2,}\b", "hi", text)
    text = re.sub(r"\bhey{2,}\b", "hey", text)
    text = re.sub(r"\bhel+o+\b", "hello", text)
    text = re.sub(r"(.)\1{2,}", r"\1", text)
    return text


def normalize_text(text: str) -> str:
    """
    Multi-stage token-safe normalization pipeline:
    1. Lowercasing & repeated character collapse
    2. Punctuation cleaning
    3. Multi-word phrase expansions (comp sci, ci/cd)
    4. Texting shortforms & informal abbreviations
    5. Academic subject abbreviation expansion
    6. Technical abbreviation expansion
    7. Lightweight fuzzy typo tolerance
    """
    if not text:
        return ""

    cleaned = text.lower().strip()
    cleaned = normalize_repeated_chars(cleaned)
    cleaned = EMOJI_PATTERN.sub(" ", cleaned)

    # Clean punctuation (preserving letters, digits, and spaces)
    cleaned = re.sub(r"[?!.,;:_~`#$|\\]+", " ", cleaned)

    # Multi-word compound abbreviations
    cleaned = re.sub(r"\bcomp\s+sci\b", "computer science", cleaned)
    cleaned = re.sub(r"\bci\s*\/\s*cd\b", "continuous integration", cleaned)
    cleaned = re.sub(r"\bui\s*\/\s*ux\b", "user interface and user experience", cleaned)

    tokens = cleaned.split()
    expanded_words = []

    for word in tokens:
        if word in SLANG_MAP:
            expanded_words.append(SLANG_MAP[word])
        elif word in ACADEMIC_SUBJECT_MAP:
            expanded_words.append(ACADEMIC_SUBJECT_MAP[word])
        elif word in TECH_ABBREVIATION_MAP:
            expanded_words.append(TECH_ABBREVIATION_MAP[word])
        else:
            if len(word) >= 4 and word not in CANONICAL_VOCABULARY:
                matches = difflib.get_close_matches(word, CANONICAL_VOCABULARY, n=1, cutoff=0.82)
                if matches:
                    expanded_words.append(matches[0])
                else:
                    expanded_words.append(word)
            else:
                expanded_words.append(word)

    return " ".join(expanded_words).strip()


# =============================================================================
# 4. DYNAMIC SOLVERS & LANGUAGE HANDLERS
# =============================================================================

def get_current_time() -> str:
    now = datetime.now()
    return now.strftime("🕒 Current Time: %I:%M:%S %p")


def get_current_date() -> str:
    now = datetime.now()
    return now.strftime("📅 Today's Date: %A, %d %B %Y")


def get_current_day() -> str:
    now = datetime.now()
    return now.strftime("📅 Today is %A.")


def solve_math_query(text: str) -> Optional[str]:
    """Safe, rule-based mathematical solver."""
    if not text:
        return None

    t = text.lower().strip()

    # 1. Percentages
    m = re.search(r"(?:what\s+is\s+)?(\d+(?:\.\d+)?)\s*%\s*(?:of|off)\s*(\d+(?:\.\d+)?)", t)
    if m:
        pct = float(m.group(1))
        val = float(m.group(2))
        res = (pct / 100.0) * val
        res_str = str(int(res)) if res.is_integer() else f"{res:.2f}".rstrip('0').rstrip('.')
        return f"📐 **Percentage Calculation:**\n**{pct:g}% of {val:g} = {res_str}**"

    # 2. Averages
    m = re.search(r"(?:average|mean)\s+(?:of\s+)?([0-9\s,\.and]+)", t)
    if m:
        raw_nums = re.findall(r"\b\d+(?:\.\d+)?\b", m.group(1))
        if raw_nums:
            nums = [float(x) for x in raw_nums]
            avg = sum(nums) / len(nums)
            avg_str = str(int(avg)) if avg.is_integer() else f"{avg:.2f}".rstrip('0').rstrip('.')
            items_str = ", ".join(f"{x:g}" for x in nums)
            return f"📐 **Average / Mean:**\nAverage of [{items_str}] = **{avg_str}** (Sum: {sum(nums):g}, Count: {len(nums)})"

    # 3. Linear Equations
    m = re.search(r"(?:solve\s+)?(\d*)\s*x\s*([\+\-])\s*(\d+(?:\.\d+)?)\s*=\s*(\d+(?:\.\d+)?)", t)
    if m:
        a_str = m.group(1)
        a = float(a_str) if a_str else 1.0
        op = m.group(2)
        b = float(m.group(3))
        c = float(m.group(4))

        rhs = (c - b) if op == '+' else (c + b)
        if a != 0:
            x_val = rhs / a
            x_str = str(int(x_val)) if x_val.is_integer() else f"{x_val:.4f}".rstrip('0').rstrip('.')
            return f"📐 **Linear Equation Solution:**\nEquation: **{m.group(0).strip()}**\n• Step 1: {a:g}x = {rhs:g}\n• **x = {x_str}**"

    # 4. Geometry Formulas
    if "area of circle" in t or "area of a circle" in t:
        return "📐 **Area of a Circle:**\n• Formula: **Area = π × r²**\n• Where **r** is the radius of the circle and **π ≈ 3.14159**."
    if "area of triangle" in t or "area of a triangle" in t:
        return "📐 **Area of a Triangle:**\n• Formula: **Area = ½ × base × height**"
    if "area of rectangle" in t or "area of a rectangle" in t:
        return "📐 **Area of a Rectangle:**\n• Formula: **Area = length × width**"
    if "circumference" in t or "perimeter of circle" in t or "perimeter of a circle" in t:
        return "📐 **Circumference of a Circle:**\n• Formula: **Circumference = 2 × π × r**"
    if "area of sphere" in t or "surface area of sphere" in t:
        return "📐 **Surface Area of a Sphere:**\n• Formula: **Area = 4 × π × r²**"

    # 5. Basic Trigonometry
    m = re.search(r"(?:what\s+is\s+)?(sin|cos|tan)\s*\(\s*(\d+(?:\.\d+)?)\s*\)", t)
    if m:
        func = m.group(1)
        deg = float(m.group(2))
        rad = math.radians(deg)
        if func == "sin":
            val = math.sin(rad)
        elif func == "cos":
            val = math.cos(rad)
        else:
            val = math.tan(rad) if (deg % 180 != 90) else float('inf')
        val_str = f"{val:.4f}".rstrip('0').rstrip('.')
        return f"📐 **Trigonometry:**\n**{func}({deg:g}°) = {val_str}**"

    # 6. Unit Conversions
    m = re.search(r"(\d+(?:\.\d+)?)\s*(km|kilometer|kilometers)\s*(?:to|in)\s*(miles?|mi)", t)
    if m:
        val = float(m.group(1))
        res = val * 0.621371
        return f"📐 **Unit Conversion:**\n**{val:g} km = {res:.2f} miles**"

    m = re.search(r"(\d+(?:\.\d+)?)\s*(miles?|mi)\s*(?:to|in)\s*(km|kilometers?)", t)
    if m:
        val = float(m.group(1))
        res = val * 1.60934
        return f"📐 **Unit Conversion:**\n**{val:g} miles = {res:.2f} km**"

    m = re.search(r"(\d+(?:\.\d+)?)\s*(?:celsius|c)\s*(?:to|in)\s*(?:fahrenheit|f)", t)
    if m:
        val = float(m.group(1))
        res = (val * 9/5) + 32
        return f"📐 **Temperature Conversion:**\n**{val:g}°C = {res:.1f}°F**"

    m = re.search(r"(\d+(?:\.\d+)?)\s*(?:kg|kilograms?)\s*(?:to|in)\s*(?:lbs?|pounds?)", t)
    if m:
        val = float(m.group(1))
        res = val * 2.20462
        return f"📐 **Weight Conversion:**\n**{val:g} kg = {res:.2f} lbs**"

    # 7. Basic Arithmetic
    clean_expr = re.sub(r"[?!]", "", t)
    clean_expr = re.sub(r"^(?:what\s+is\s+|calculate\s+|compute\s+|solve\s+)", "", clean_expr).strip()
    clean_expr = clean_expr.replace("×", "*").replace("x", "*").replace("^", "**")

    if re.match(r"^[\d\s\+\-\*\/\(\)\.\%\*\*]+$", clean_expr) and any(op in clean_expr for op in "+-*/%"):
        try:
            res = eval(clean_expr, {"__builtins__": None}, {})
            if isinstance(res, (int, float)):
                res_str = str(int(res)) if float(res).is_integer() else f"{res:.4f}".rstrip('0').rstrip('.')
                display_expr = clean_expr.replace('**', '^')
                return f"📐 **Calculation Result:**\n`{display_expr}` = **{res_str}**"
        except Exception:
            pass

    return None


def solve_synonym_query(text: str) -> Optional[str]:
    """Finds synonyms for words from the built-in dictionary."""
    t = text.lower().strip()
    m = re.search(r"(?:synonyms?\s+(?:of|for)|another\s+word\s+for|words?\s+similar\s+to)\s+([a-zA-Z]+)", t)
    if m:
        w = m.group(1).lower()
        if w in SYNONYMS_DB:
            syns = ", ".join(SYNONYMS_DB[w])
            return f"📖 **Synonyms for '{w}':**\n• {syns}"
        else:
            return f"📖 I don't have built-in synonyms for **'{w}'** yet. Try asking for common words like *happy*, *important*, *fast*, *smart*, *difficult*, or *strong*!"
    return None


def solve_antonym_query(text: str) -> Optional[str]:
    """Finds antonyms/opposites for words from the built-in dictionary."""
    t = text.lower().strip()
    m = re.search(r"(?:antonyms?\s+(?:of|for)|opposites?\s+(?:of|word\s+for|for))\s+([a-zA-Z]+)", t)
    if m:
        w = m.group(1).lower()
        if w in ANTONYMS_DB:
            ants = ", ".join(ANTONYMS_DB[w])
            return f"📖 **Antonym / Opposite of '{w}':**\n• {ants}"
        else:
            return f"📖 I don't have a built-in antonym for **'{w}'** yet. Try asking for words like *happy*, *hot*, *difficult*, *early*, *fast*, or *strong*!"
    return None


def solve_vocabulary_query(text: str) -> Optional[str]:
    """Defines vocabulary words from the curated dictionary."""
    t = text.lower().strip()
    m = re.search(r"(?:what\s+does\s+([a-zA-Z]+)\s+mean|meaning\s+of\s+([a-zA-Z]+)|define\s+([a-zA-Z]+)|definition\s+of\s+([a-zA-Z]+))", t)
    if m:
        w = next(g for g in m.groups() if g).lower()
        if w in VOCABULARY_DB:
            defn = VOCABULARY_DB[w]
            return f"📖 **Definition of '{w.capitalize()}':**\n• {defn}"
    return None


def solve_sentence_correction_query(text: str) -> Optional[str]:
    """Lightweight rule-based grammar correction for common mistakes."""
    t = text.strip()
    clean = re.sub(r"^(?:correct(?:\s+this)?(?:\s+sentence)?:\s*|check\s+(?:my\s+)?grammar:\s*)", "", t, flags=re.IGNORECASE).strip()
    clean = clean.strip('"\'')

    for pat, repl, reason in SENTENCE_CORRECTIONS:
        if re.search(pat, clean, re.IGNORECASE):
            corrected = re.sub(pat, repl, clean, count=1, flags=re.IGNORECASE)
            corrected = corrected[0].upper() + corrected[1:] if corrected else corrected
            return f"📝 **Sentence Correction:**\n\n• **Corrected:** \"{corrected}\"\n• **Original:** \"{clean}\"\n\n💡 **Reason:**\n{reason}"
    return None


# =============================================================================
# 5. INTENT DEFINITIONS & KNOWLEDGE REGISTRY
# =============================================================================

class Intent:
    def __init__(
        self,
        name: str,
        keywords: Optional[List[str]] = None,
        phrases: Optional[List[str]] = None,
        patterns: Optional[List[str]] = None,
        emojis: Optional[List[str]] = None,
        responses: Optional[Union[List[str], Callable[[], str]]] = None,
        weight: float = 1.0,
        requires_all_keywords: bool = False
    ):
        self.name = name
        self.keywords = [k.lower() for k in (keywords or [])]
        self.phrases = [p.lower() for p in (phrases or [])]
        self.patterns = [re.compile(p, re.IGNORECASE) for p in (patterns or [])]
        self.emojis = [normalize_emoji(e) for e in (emojis or [])]
        self.responses = responses or []
        self.weight = weight
        self.requires_all_keywords = requires_all_keywords

    def get_response(self) -> str:
        if callable(self.responses):
            return self.responses()
        if isinstance(self.responses, list) and self.responses:
            return random.choice(self.responses)
        return random.choice(FALLBACK_RESPONSES)


# Registry of all rule-based intents
INTENTS: List[Intent] = [
    # -----------------------------
    # Conversational & Greetings
    # -----------------------------
    Intent(
        name="GREETING",
        keywords=["hello", "hi", "hey", "howdy", "greetings", "helo", "yo", "good morning", "good afternoon", "good evening"],
        phrases=[
            "hello", "hi", "hey", "good morning", "good afternoon",
            "good evening", "hey nova", "hi nova", "hello nova", "greetings", "yo"
        ],
        emojis=["👋", "🙋", "😊", "🙂"],
        responses=[
            "👋 Hello! How can I help you today?",
            "😊 Hi there! What would you like to know?",
            "🤖 Hey! Welcome to NovaAI. How can I assist you today?",
            "👋 Greetings! Ready to explore programming, science, English, math, or utilities?"
        ],
        weight=1.0
    ),
    Intent(
        name="GOODBYE",
        keywords=["bye", "goodbye", "exit", "quit", "cya", "farewell"],
        phrases=[
            "bye", "goodbye", "see you later", "catch you later",
            "bye bye", "exit", "quit", "see you", "cya"
        ],
        emojis=["👋"],
        responses=[
            "👋 Goodbye! Have a fantastic day ahead.",
            "😊 See you later! Feel free to return anytime you have questions.",
            "🚀 Farewell! Keep learning and building amazing things.",
            "👋 Bye! Hope I was helpful today."
        ],
        weight=1.15
    ),
    Intent(
        name="HOW_ARE_YOU",
        keywords=["how", "are", "you", "doing"],
        phrases=[
            "how are you", "how are you doing", "how are u", "how is it going",
            "how do you do", "are you okay", "hows it going"
        ],
        responses=[
            "😊 I'm functioning at 100% capacity! Thank you for asking. How can I assist you?",
            "🤖 All systems operational and ready to help! What's on your mind today?",
            "✨ Doing great! Excited to explore topics with you."
        ],
        weight=1.2
    ),
    Intent(
        name="ABOUT_NOVAAI",
        keywords=["about", "who", "what", "novaai", "nova", "yourself"],
        phrases=[
            "about novaai", "about nova", "who are you", "what are you", "who are u",
            "tell me about yourself", "introduce yourself", "what is novaai",
            "what can you do", "what can u do", "about you"
        ],
        responses=[
            "🤖 **NovaAI** is an advanced rule-based intelligent chatbot built with Python, Flask, HTML, CSS, and JavaScript. I can explain programming, science, English grammar, technology, solve math problems, provide utilities, and more!",
            "✨ I am **NovaAI**, an interactive AI assistant designed to help you learn science, programming, English, mathematics, and access handy utilities without external API dependencies.",
            "🌟 I'm **NovaAI**! Built as a full-stack chatbot with an intelligent rule-based engine. Ask me about Python, physics, chemistry, biology, English grammar, or type 'help' to see my full catalog."
        ],
        weight=1.3
    ),
    Intent(
        name="BOT_NAME",
        keywords=["your", "name", "called"],
        phrases=["what is your name", "your name", "whats your name", "who are you called", "what should i call you"],
        responses=[
            "🤖 My name is **NovaAI**!",
            "✨ You can call me **NovaAI**, your friendly rule-based companion.",
            "🤖 I am **NovaAI** — built to assist and inform!"
        ],
        weight=1.2
    ),
    Intent(
        name="CREATOR",
        keywords=["who", "made", "created", "built", "developer", "author"],
        phrases=[
            "who made you", "who created you", "who built you",
            "who is your developer", "who is your creator", "who developed novaai"
        ],
        responses=[
            "👨‍💻 I was developed as an advanced Full Stack AI internship project using Python, Flask, and modern web technologies.",
            "🚀 I was crafted by a passionate software engineer as a premium rule-based AI system built on Flask.",
            "💡 My creator built me to demonstrate intelligent rule-based NLP and full-stack web application engineering."
        ],
        weight=1.3
    ),
    Intent(
        name="VERSION",
        keywords=["version", "release"],
        phrases=["what is your version", "current version", "version of novaai", "bot version"],
        responses=[
            "🚀 NovaAI Version 1.0 (Powered by Advanced Rule-Based Intelligence Engine).",
            "⚡ You are running **NovaAI v1.0** with enhanced multi-domain knowledge across Science, English, Math, Programming, and Technology."
        ],
        weight=1.2
    ),
    Intent(
        name="THANKS",
        keywords=["thanks", "thank", "appreciated", "grateful"],
        phrases=[
            "thanks", "thank you", "thx", "ty", "thanks nova",
            "thank you so much", "much appreciated", "many thanks",
            "thank u", "thnks", "thx nova"
        ],
        responses=[
            "😊 You're very welcome!",
            "🎉 Glad I could help! Let me know if you need anything else.",
            "✨ Anytime! Happy to assist.",
            "🌟 You're welcome! Feel free to ask more questions."
        ],
        weight=1.25
    ),

    # -----------------------------
    # Emoji Sentiment & Mood Intents
    # -----------------------------
    Intent(
        name="HAPPINESS",
        keywords=["happy", "glad", "joy", "cheerful", "good vibes"],
        phrases=["i am happy", "feeling good", "feeling happy", "so happy", "happy today"],
        emojis=["😊", "😄", "😁", "🙂", "😀", "😃", "🤩"],
        responses=[
            "Glad to see you're in a great mood! 😊 What can I do for you today?",
            "Your positive energy is contagious! ✨ How can I help you today?",
            "😊 Love the good vibes! What would you like to explore?"
        ],
        weight=1.05
    ),
    Intent(
        name="LAUGHTER",
        keywords=["haha", "lol", "lmao", "rofl", "hehe", "funny"],
        phrases=["that is funny", "thats funny", "made me laugh", "so funny", "haha", "lol", "lmao"],
        emojis=["😂", "🤣", "😆"],
        responses=[
            "Haha! Glad you're enjoying it! 😂",
            "Looks like I made you laugh! 😄",
            "😂 That's a great reaction! What's next on your mind?",
            "Glad I could bring a smile to your day! 🤣"
        ],
        weight=1.1
    ),
    Intent(
        name="LOVE",
        keywords=["love", "heart", "adore"],
        phrases=["love this", "love you", "send love", "much love", "i love this"],
        emojis=["❤️", "🩷", "🧡", "💛", "💚", "💙", "💜", "🤍", "🖤", "🤎", "🥰", "😍", "💖", "💗", "💓"],
        responses=[
            "Sending positive energy right back at you! ❤️",
            "Appreciate the love! 🥰 How can I assist you today?",
            "❤️ Glad to have you here! Let me know if you need help with anything."
        ],
        weight=1.05
    ),
    Intent(
        name="SADNESS",
        keywords=["sad", "unhappy", "depressed", "down", "crying", "upset"],
        phrases=["i am sad", "feeling down", "feeling sad", "i am upset", "im sad", "so sad"],
        emojis=["😢", "😭", "☹️", "🙁", "😞", "💔", "🥺", "😿"],
        responses=[
            "I'm sorry you're feeling down. I'm here if you'd like to chat or learn something new. 💙",
            "That doesn't sound great. Take it easy today — I'm right here if you need anything.",
            "Sending you positive vibes. 🌟 Let me know if you'd like to hear a joke or an inspiring quote!"
        ],
        weight=1.15
    ),
    Intent(
        name="ANGER",
        keywords=["angry", "furious", "mad", "annoyed", "frustrated"],
        phrases=["i am angry", "i am frustrated", "this is annoying", "so mad", "im angry", "im frustrated"],
        emojis=["😡", "😠", "🤬", "😤", "👿"],
        responses=[
            "I sense some frustration. Want to tell me what's going on?",
            "That sounds frustrating. How can I help resolve things for you?",
            "I understand. Take a deep breath — let me know what you're dealing with."
        ],
        weight=1.15
    ),
    Intent(
        name="CONFUSION",
        keywords=["confused", "puzzled", "lost"],
        phrases=["i am confused", "what does this mean", "im confused", "dont understand", "what mean"],
        emojis=["🤔", "😕", "❓", "🤨", "🧐"],
        responses=[
            "Thinking about something? Ask me anything about programming, science, English, math, or utilities!",
            "What's on your mind? 🤔 I'm ready to help you figure it out!",
            "Need help figuring something out? Feel free to ask or type **help** to browse topics."
        ],
        weight=1.05
    ),
    Intent(
        name="SURPRISE",
        keywords=["wow", "surprised", "shocked", "amazed"],
        phrases=["wow", "that is crazy", "thats crazy", "mind blown", "holy cow", "no way"],
        emojis=["😮", "😲", "😯", "😱", "🤯", "😳", "🙀"],
        responses=[
            "Mind-blowing, isn't it? 🤯 What else can I show you?",
            "😮 Quite a surprise! Let me know what you'd like to explore next.",
            "I know, right? Science and technology can be truly fascinating! ✨"
        ],
        weight=1.05
    ),
    Intent(
        name="AGREEMENT",
        keywords=["agree", "approved", "ok", "okay", "alright"],
        phrases=["okay", "sounds good", "all right", "got it", "i agree", "ok", "cool"],
        emojis=["👍", "👌", "✅"],
        responses=[
            "Awesome! 👍 Let me know whenever you need anything else.",
            "Glad that helps! Feel free to ask if you have more questions.",
            "Sounds like a plan! 👍"
        ],
        weight=1.05
    ),
    Intent(
        name="DISAGREEMENT",
        keywords=["disagree", "reject", "nope", "nah"],
        phrases=["i disagree", "not quite", "no way", "nope", "nah"],
        emojis=["👎", "❌", "🚫"],
        responses=[
            "Got it. Let's try another approach — what would you like to know instead?",
            "No problem at all! Feel free to rephrase or type **help** to browse available topics."
        ],
        weight=1.05
    ),
    Intent(
        name="EXCITEMENT",
        keywords=["fire", "hype", "hyped", "pumped", "energy"],
        phrases=["this is fire", "let us go", "lets go", "so hyped", "lets do this"],
        emojis=["🔥", "⚡", "🚀", "💥", "💯"],
        responses=[
            "Now that's some great energy! 🔥 Let's learn and build something awesome!",
            "Let's go! 🚀 Ready for whatever challenge you have next.",
            "Love the enthusiasm! 🔥 What's next on your mind?"
        ],
        weight=1.1
    ),
    Intent(
        name="CELEBRATION",
        keywords=["celebrate", "celebrating", "congrats", "congratulations", "win"],
        phrases=["we did it", "congratulations", "congrats", "celebration time"],
        emojis=["🎉", "🥳", "🎊", "🏆", "🥂", "🍾"],
        responses=[
            "That's definitely worth celebrating! 🎉 Congratulations!",
            "Awesome! 🥳 Great news — keep up the fantastic momentum!",
            "Woohoo! 🎉 Celebrate the win!"
        ],
        weight=1.15
    ),
    Intent(
        name="PRAISE",
        keywords=["praise", "kudos", "props"],
        phrases=["great job", "well done", "awesome job", "good job", "nice job"],
        emojis=["👏", "🙌"],
        responses=[
            "Thank you so much! 👏 I appreciate the kind words.",
            "Glad I could deliver! 🙌 Let me know if you need more help.",
            "Thank you! 👏 Happy to assist anytime."
        ],
        weight=1.15
    ),

    # -----------------------------
    # Help System Intents
    # -----------------------------
    Intent(
        name="HELP_PROGRAMMING",
        keywords=["programming", "coding", "cs", "computer science", "help"],
        phrases=[
            "programming help", "coding help", "programming topics", "help with programming",
            "cs help", "comp sci help", "computer science help"
        ],
        responses=[HELP_PROGRAMMING],
        weight=1.4
    ),
    Intent(
        name="HELP_TECHNOLOGY",
        keywords=["technology", "help", "tech"],
        phrases=["technology help", "tech help", "technology topics", "help with tech", "help with technology"],
        responses=[HELP_TECHNOLOGY],
        weight=1.4
    ),
    Intent(
        name="HELP_MATHEMATICS",
        keywords=["math", "mathematics", "maths", "calculate", "calculator", "help"],
        phrases=[
            "math help", "mathematics help", "maths help", "math commands", "math topics",
            "what math can you do", "what mathematics can you do", "help with math",
            "help with mathematics", "math capabilities", "mathematics topics"
        ],
        emojis=["📐", "🔢", "➕", "➖", "✖️", "➗"],
        responses=[HELP_MATHEMATICS],
        weight=1.45
    ),
    Intent(
        name="HELP_SCIENCE",
        keywords=["science", "help"],
        phrases=[
            "science help", "science topics", "science commands", "help with science",
            "what science can you do", "science guide", "scientific topics"
        ],
        emojis=["🔬", "🧪", "⚛️", "🧬"],
        responses=[HELP_SCIENCE],
        weight=1.45
    ),
    Intent(
        name="HELP_PHYSICS",
        keywords=["physics", "phy", "phys", "help"],
        phrases=[
            "physics help", "phy help", "phys help", "physics topics",
            "help with physics", "physics guide", "phy topics"
        ],
        emojis=["⚛️"],
        responses=[HELP_PHYSICS],
        weight=1.45
    ),
    Intent(
        name="HELP_CHEMISTRY",
        keywords=["chemistry", "chem", "help"],
        phrases=[
            "chemistry help", "chem help", "chemistry topics",
            "help with chemistry", "chemistry guide", "chem topics"
        ],
        emojis=["🧪"],
        responses=[HELP_CHEMISTRY],
        weight=1.45
    ),
    Intent(
        name="HELP_BIOLOGY",
        keywords=["biology", "bio", "help"],
        phrases=[
            "biology help", "bio help", "biology topics",
            "help with biology", "biology guide", "bio topics"
        ],
        emojis=["🧬"],
        responses=[HELP_BIOLOGY],
        weight=1.45
    ),
    Intent(
        name="HELP_ENGLISH",
        keywords=["english", "eng", "language", "help"],
        phrases=[
            "english help", "eng help", "language help", "english topics", "help with english",
            "what english can you do", "english guide", "language guide"
        ],
        emojis=["📖", "📝", "📚"],
        responses=[HELP_ENGLISH],
        weight=1.45
    ),
    Intent(
        name="HELP_GRAMMAR",
        keywords=["grammar", "tenses", "help"],
        phrases=["grammar help", "tenses help", "help with grammar", "grammar topics", "grammar guide"],
        emojis=["📝"],
        responses=[HELP_GRAMMAR],
        weight=1.45
    ),
    Intent(
        name="HELP_VOCABULARY",
        keywords=["vocabulary", "synonym", "antonym", "help"],
        phrases=["vocabulary help", "synonym help", "antonym help", "help with vocabulary", "vocabulary guide"],
        emojis=["📚"],
        responses=[HELP_VOCABULARY],
        weight=1.45
    ),
    Intent(
        name="HELP_UTILITIES",
        keywords=["utility", "utilities", "help"],
        phrases=["utility help", "utilities help", "utility commands", "help with utilities"],
        responses=[HELP_UTILITIES],
        weight=1.4
    ),
    Intent(
        name="HELP",
        keywords=["help", "commands", "menu", "features", "options"],
        phrases=["help", "show help", "help me", "what can you do", "commands", "available commands", "menu"],
        responses=[HELP_GENERAL],
        weight=1.1
    ),

    # -----------------------------
    # Utilities
    # -----------------------------
    Intent(
        name="TIME",
        keywords=["time", "clock"],
        phrases=["what time is it", "current time", "tell me the time", "time now", "what is the time", "time"],
        responses=get_current_time,
        weight=1.2
    ),
    Intent(
        name="DATE",
        keywords=["date", "today"],
        phrases=["what is today's date", "what is todays date", "current date", "today's date", "todays date", "what date is it", "date today", "date"],
        responses=get_current_date,
        weight=1.2
    ),
    Intent(
        name="DAY",
        keywords=["day", "weekday"],
        phrases=["what day is it", "what day is today", "current day", "which day is today", "day of the week", "day"],
        responses=get_current_day,
        weight=1.2
    ),
    Intent(
        name="JOKE",
        keywords=["joke", "jokes", "laugh", "funny"],
        phrases=["tell me a joke", "joke", "tell a joke", "make me laugh", "say a joke", "give me a joke", "another joke"],
        responses=JOKES,
        weight=1.2
    ),
    Intent(
        name="FUN_FACT",
        keywords=["fact", "facts", "trivia"],
        phrases=["tell me a fun fact", "fun fact", "give me a fun fact", "tell me a fact", "interesting fact", "tech fact", "random fact"],
        responses=FUN_FACTS,
        weight=1.2
    ),
    Intent(
        name="MOTIVATION",
        keywords=["motivate", "motivation", "inspire", "inspiration"],
        phrases=["motivate me", "motivation", "give me motivation", "inspire me", "need motivation", "motivational quote"],
        responses=MOTIVATIONS,
        weight=1.2
    ),
    Intent(
        name="QUOTE",
        keywords=["quote", "quotes", "saying", "wisdom"],
        phrases=["give me a quote", "quote", "tell me a quote", "inspirational quote", "tech quote", "famous quote", "share a quote"],
        responses=QUOTES,
        weight=1.2
    ),

    # -----------------------------
    # Programming Knowledge Base
    # -----------------------------
    Intent(
        name="PYTHON",
        keywords=["python"],
        phrases=[
            "what is python", "tell me about python", "python", "explain python",
            "why python", "what can python do", "python programming", "define python"
        ],
        emojis=["🐍"],
        responses=[
            "🐍 **Python** is a high-level, interpreted, general-purpose programming language known for its clean, readable syntax. It is widely used for web development, data science, artificial intelligence, automation, and scientific computing.",
            "🐍 **Python** emphasizes code readability and simplicity. With powerful libraries like NumPy, Pandas, Django, and Flask, it has become one of the world's most popular languages for everything from scripting to machine learning."
        ],
        weight=1.3
    ),
    Intent(
        name="HTML",
        keywords=["html", "hypertext markup language"],
        phrases=[
            "what is html", "tell me about html", "html", "explain html",
            "what does html do", "html5", "define html", "what is hypertext markup language"
        ],
        emojis=["🌐"],
        responses=[
            "🌐 **HTML** (HyperText Markup Language) is the foundational standard markup language for creating web pages. It defines the structure and layout of content using elements, tags, headings, paragraphs, links, and forms.",
            "🌐 **HTML** forms the structural backbone of every website on the Internet. Combined with CSS for styling and JavaScript for interactivity, it completes the core trio of web technologies."
        ],
        weight=1.3
    ),
    Intent(
        name="CSS",
        keywords=["css", "cascading style sheets"],
        phrases=[
            "what is css", "tell me about css", "css", "explain css",
            "what does css do", "css3", "define css", "what is cascading style sheets"
        ],
        emojis=["🎨"],
        responses=[
            "🎨 **CSS** (Cascading Style Sheets) is used to style and layout web pages. It controls visual design elements including colors, fonts, spacing, flexbox, grid layouts, transitions, and responsive multi-device design.",
            "🎨 **CSS** transforms raw HTML documents into beautiful, responsive, and animated user interfaces. Modern CSS features CSS variables, animations, glassmorphism effects, and container queries."
        ],
        weight=1.3
    ),
    Intent(
        name="JAVASCRIPT",
        keywords=["javascript", "js"],
        phrases=[
            "what is javascript", "tell me about javascript", "javascript", "explain javascript",
            "what is js", "tell me about js", "why javascript", "define javascript"
        ],
        emojis=["⚡"],
        responses=[
            "⚡ **JavaScript** is a versatile, high-level programming language that powers dynamic interactivity on the web. It runs on both the client side (in web browsers) and the server side (via Node.js).",
            "⚡ **JavaScript** allows developers to build rich interactive experiences, fetch asynchronous data with `fetch()`, manipulate the DOM, and power full-stack applications with frameworks like React, Vue, and Express."
        ],
        weight=1.3
    ),
    Intent(
        name="FLASK",
        keywords=["flask"],
        phrases=[
            "what is flask", "tell me about flask", "flask", "explain flask",
            "why flask", "flask framework", "python flask", "define flask"
        ],
        emojis=["🍶"],
        responses=[
            "🍶 **Flask** is a lightweight, flexible WSGI micro web framework for Python. It provides the essentials for routing, templates (Jinja2), and request handling without forcing complex boilerplate.",
            "🍶 **Flask** is designed to make getting started quick and easy, with the ability to scale up to complex applications. It powers NovaAI's backend server!"
        ],
        weight=1.3
    ),
    Intent(
        name="GIT",
        keywords=["git"],
        phrases=[
            "what is git", "tell me about git", "git", "explain git",
            "why git", "git version control", "define git"
        ],
        responses=[
            "🌲 **Git** is a distributed version control system designed to track changes in source code during software development. It enables branching, merging, and seamless collaboration among developer teams.",
            "🌲 **Git** allows developers to record snapshots of their codebase over time, rollback to previous versions when bugs occur, and manage multiple parallel features using lightweight branches."
        ],
        weight=1.3
    ),
    Intent(
        name="GITHUB",
        keywords=["github"],
        phrases=[
            "what is github", "tell me about github", "github", "explain github",
            "why github", "git vs github", "define github"
        ],
        emojis=["🐙"],
        responses=[
            "🐙 **GitHub** is a cloud-based platform built on Git that lets developers store, manage, review, and collaborate on code repositories. It includes Pull Requests, Issues, GitHub Actions for CI/CD, and project management tools.",
            "🐙 **GitHub** is the world's largest host of open-source software, enabling developers globally to share code, contribute to projects, and deploy automated pipelines."
        ],
        weight=1.3
    ),
    Intent(
        name="API",
        keywords=["api", "apis", "application programming interface"],
        phrases=[
            "what is an api", "what is api", "tell me about api", "api", "explain api",
            "how do apis work", "rest api", "define api", "what is application programming interface"
        ],
        emojis=["🔌"],
        responses=[
            "🔌 An **API** (Application Programming Interface) is a defined set of rules and protocols that allows different software applications to communicate and exchange data with one another.",
            "🔌 **APIs** act as digital bridges between systems. For instance, NovaAI's `/chat` endpoint is a REST API that receives a message in JSON format and responds with an intelligent reply!"
        ],
        weight=1.3
    ),
    Intent(
        name="DATABASE",
        keywords=["database", "databases", "sql", "nosql", "db", "dbms"],
        phrases=[
            "what is a database", "what is database", "tell me about databases", "database", "explain database",
            "what is sql", "what is nosql", "define database", "what is db", "what is dbms"
        ],
        emojis=["🗄️"],
        responses=[
            "🗄️ A **Database (DB)** is an organized collection of structured or unstructured data stored electronically in a computer system. Databases are managed by Database Management Systems (DBMS).",
            "🗄️ Databases fall broadly into **Relational (SQL)** systems (like PostgreSQL, MySQL, SQLite) using tables and schemas, and **NoSQL** systems (like MongoDB, Redis) designed for flexible documents and key-value caching."
        ],
        weight=1.3
    ),
    Intent(
        name="ALGORITHM",
        keywords=["algorithm", "algorithms"],
        phrases=[
            "what is an algorithm", "what is algorithm", "tell me about algorithms", "algorithm", "explain algorithm",
            "what are algorithms", "define algorithm"
        ],
        responses=[
            "📐 An **Algorithm** is an unambiguous, step-by-step procedure or set of computational instructions designed to perform a specific task or solve a defined problem efficiently.",
            "📐 **Algorithms** power every piece of software — from sorting lists and finding shortest paths in navigation to pattern matching and decision scoring in NovaAI's intelligence engine!"
        ],
        weight=1.3
    ),
    Intent(
        name="DSA",
        keywords=["dsa", "data structures and algorithms"],
        phrases=[
            "what is dsa", "explain dsa", "define dsa", "data structures and algorithms",
            "what is data structures and algorithms", "why dsa"
        ],
        responses=[
            "📚 **Data Structures and Algorithms (DSA):**\n\n• **Data Structures:** Ways to organize and store data efficiently in memory (e.g., Arrays, Linked Lists, Stacks, Queues, Trees, Graphs, Hash Maps).\n• **Algorithms:** Step-by-step procedures for processing and computing data (e.g., Binary Search, Merge Sort, Dijkstra's Algorithm).\n• Mastering DSA is essential for writing performant code and excelling in technical interviews!"
        ],
        weight=1.35
    ),
    Intent(
        name="OOP",
        keywords=["oop", "object oriented programming"],
        phrases=[
            "what is oop", "explain oop", "define oop", "object oriented programming",
            "what is object oriented programming", "oop concepts"
        ],
        responses=[
            "🧱 **Object-Oriented Programming (OOP):**\n\nA programming paradigm based on the concept of 'objects' containing data (attributes) and code (methods). The 4 pillars of OOP are:\n\n1. **Encapsulation:** Bundling data and methods into a single class while restricting direct access.\n2. **Abstraction:** Hiding complex implementation details and showing only necessary features.\n3. **Inheritance:** Enabling classes to inherit properties from parent classes.\n4. **Polymorphism:** Allowing methods to take on multiple forms based on context."
        ],
        weight=1.35
    ),

    # -----------------------------
    # Technology Knowledge Base
    # -----------------------------
    Intent(
        name="AI_VS_ML",
        keywords=["difference", "between", "ai", "ml", "versus", "vs"],
        phrases=[
            "difference between ai and ml", "ai vs ml", "difference between artificial intelligence and machine learning",
            "how is ai different from ml", "ai or ml", "compare ai and ml"
        ],
        responses=[
            "🧠 **AI vs. Machine Learning:**\n\n• **Artificial Intelligence (AI)** is the broad umbrella discipline focused on creating systems capable of simulating human intelligence, reasoning, and problem-solving.\n• **Machine Learning (ML)** is a specific subset of AI where algorithms automatically learn patterns from data and improve with experience rather than following explicitly hardcoded rules.\n\nIn short: *All Machine Learning is AI, but not all AI is Machine Learning!*",
        ],
        weight=1.5
    ),
    Intent(
        name="MACHINE_LEARNING",
        keywords=["machine", "learning", "ml"],
        phrases=[
            "what is machine learning", "what is ml", "tell me about machine learning", "machine learning",
            "explain machine learning", "how does machine learning work", "define machine learning"
        ],
        emojis=["🤖"],
        responses=[
            "🤖 **Machine Learning (ML)** is a field of artificial intelligence where computer systems learn from data and statistical algorithms to identify patterns and make predictions without being explicitly programmed.",
            "🤖 **Machine Learning** powers modern recommendation systems, computer vision, natural language processing, and autonomous vehicles through supervised, unsupervised, and reinforcement learning methods."
        ],
        weight=1.35
    ),
    Intent(
        name="AI",
        keywords=["artificial", "intelligence", "ai"],
        phrases=[
            "what is artificial intelligence", "what is ai", "tell me about ai", "artificial intelligence",
            "explain artificial intelligence", "ai definition", "define artificial intelligence"
        ],
        emojis=["🧠"],
        responses=[
            "🧠 **Artificial Intelligence (AI)** is a branch of computer science dedicated to creating software and systems capable of performing tasks that typically require human intelligence, such as visual perception, speech recognition, decision-making, and reasoning.",
            "🧠 **Artificial Intelligence** encompasses rule-based expert systems (like NovaAI's internal logic engine) as well as data-driven machine learning and deep neural networks."
        ],
        weight=1.3
    ),
    Intent(
        name="CLOUD_COMPUTING",
        keywords=["cloud", "computing", "aws", "azure", "gcp"],
        phrases=[
            "what is cloud computing", "what is the cloud", "tell me about cloud computing", "cloud computing",
            "explain cloud computing", "why cloud computing", "define cloud computing"
        ],
        emojis=["☁️"],
        responses=[
            "☁️ **Cloud Computing** is the on-demand delivery of IT resources and services over the Internet with pay-as-you-go pricing. It provides scalable servers, storage, databases, networking, and software without maintaining physical hardware.",
            "☁️ Popular cloud providers include **Amazon Web Services (AWS)**, **Google Cloud Platform (GCP)**, and **Microsoft Azure**, enabling instant global scalability, reliability, and automated deployment."
        ],
        weight=1.3
    ),
    Intent(
        name="FRONTEND",
        keywords=["frontend", "front-end", "ui", "client-side"],
        phrases=[
            "what is frontend", "what is front end", "what is frontend development", "tell me about frontend",
            "explain frontend", "frontend development", "define frontend"
        ],
        emojis=["🖥️"],
        responses=[
            "🖥️ **Frontend Development** involves building the client-side of web applications — everything that users see, interact with, and experience directly in their browsers using HTML, CSS, JavaScript, and UI frameworks.",
            "🖥️ Frontend developers focus on user experience (UX), accessibility, responsive cross-device layouts, animations, and fluid state management using technologies like React, Vue, and modern CSS."
        ],
        weight=1.3
    ),
    Intent(
        name="BACKEND",
        keywords=["backend", "back-end", "server-side"],
        phrases=[
            "what is backend", "what is back end", "what is backend development", "tell me about backend",
            "explain backend", "backend development", "define backend"
        ],
        emojis=["⚙️"],
        responses=[
            "⚙️ **Backend Development** refers to the server-side architecture of an application. It handles business logic, database queries, authentication, security, server management, and API design.",
            "⚙️ Backend systems are typically written in languages like Python (Flask/Django), JavaScript (Node.js/Express), Java, Go, or Ruby, ensuring data is securely processed and delivered to the frontend."
        ],
        weight=1.3
    ),
    Intent(
        name="OPERATING_SYSTEM",
        keywords=["operating system", "os", "windows", "linux", "macos"],
        phrases=[
            "what is an operating system", "what is operating system", "what is an os", "what is os",
            "explain operating system", "operating systems", "define operating system"
        ],
        responses=[
            "💻 **Operating System (OS):**\n\nAn **Operating System** is system software that manages computer hardware, software resources, memory allocation, and provides common services for computer programs (e.g., Linux, Windows, macOS, Android, iOS)."
        ],
        weight=1.35
    ),
    Intent(
        name="HARDWARE_COMPONENTS",
        keywords=["cpu", "gpu", "ram", "processor", "hardware", "central processing unit", "graphics processing unit", "random access memory"],
        phrases=[
            "what is cpu", "what is gpu", "what is ram", "explain cpu", "explain gpu", "explain ram",
            "what is central processing unit", "what is graphics processing unit", "what is random access memory",
            "difference between cpu and gpu", "what is a processor"
        ],
        responses=[
            "🖥️ **Core Computer Hardware:**\n\n• **CPU (Central Processing Unit):** The primary processor/'brain' of a computer executing general instructions.\n• **GPU (Graphics Processing Unit):** Highly parallel processor optimized for rendering graphics and training machine learning models.\n• **RAM (Random Access Memory):** High-speed volatile memory holding data currently in active use."
        ],
        weight=1.35
    ),

    # -----------------------------
    # 🔬 Science — Physics
    # -----------------------------
    Intent(
        name="PHYSICS_GENERAL",
        keywords=["physics", "phy", "phys"],
        phrases=[
            "what is physics", "what is phy", "tell me about physics", "tell me about phy",
            "explain physics", "define physics", "why study physics"
        ],
        emojis=["⚛️"],
        responses=[
            "⚛️ **Physics** is the fundamental branch of science that studies matter, energy, motion, force, space, and time. It explores how the universe behaves from subatomic particles to cosmic galaxies!"
        ],
        weight=1.3
    ),
    Intent(
        name="PHYSICS_FORCE",
        keywords=["force", "newton", "newtons"],
        phrases=[
            "what is force", "define force", "explain force", "tell me about force",
            "what is newton's first law", "what is newtons first law", "newtons first law",
            "what is newton's second law", "what is newtons second law", "newtons second law",
            "what is newton's third law", "what is newtons third law", "newtons third law",
            "newton's laws of motion", "newtons laws of motion", "newton's laws", "newtons laws"
        ],
        emojis=["⚛️"],
        responses=[
            "⚛️ **Force & Newton's Laws of Motion:**\n\n• **Force (F):** A push or pull upon an object resulting from its interaction with another object (Formula: `F = m × a`, measured in Newtons `N`).\n• **1st Law (Inertia):** An object remains at rest or in uniform motion unless acted on by an external net force.\n• **2nd Law (F=ma):** Acceleration is directly proportional to net force and inversely proportional to mass.\n• **3rd Law (Action-Reaction):** For every action, there is an equal and opposite reaction."
        ],
        weight=1.35
    ),
    Intent(
        name="PHYSICS_MOTION_VELOCITY",
        keywords=["velocity", "speed", "acceleration", "displacement", "momentum"],
        phrases=[
            "what is velocity", "define velocity", "explain velocity",
            "what is acceleration", "define acceleration", "explain acceleration",
            "speed vs velocity", "difference between speed and velocity",
            "what is momentum", "define momentum", "what is displacement"
        ],
        responses=[
            "⚛️ **Kinematics & Motion:**\n\n• **Speed:** A scalar quantity measuring how fast an object moves (`distance / time`).\n• **Velocity:** A vector quantity measuring speed in a specific direction (`displacement / time`).\n• **Acceleration:** The rate of change of velocity over time (`a = Δv / t`, in `m/s²`).\n• **Momentum:** The quantity of motion of a moving body (`p = mass × velocity`)."
        ],
        weight=1.3
    ),
    Intent(
        name="PHYSICS_GRAVITY",
        keywords=["gravity", "gravitation", "gravitational"],
        phrases=[
            "what is gravity", "define gravity", "explain gravity", "tell me about gravity",
            "what does gravity mean", "how does gravity work", "law of gravitation"
        ],
        emojis=["🌍"],
        responses=[
            "🌍 **Gravity** is a fundamental universal force of attraction that pulls objects with mass or energy toward one another. On Earth, gravity accelerates falling objects at approximately `9.8 m/s²` (`g`), giving objects weight and keeping our atmosphere and ocean tides in balance!"
        ],
        weight=1.3
    ),
    Intent(
        name="PHYSICS_ENERGY_WORK",
        keywords=["energy", "kinetic", "potential", "work", "power"],
        phrases=[
            "what is kinetic energy", "what is potential energy", "what is energy",
            "define kinetic energy", "define potential energy", "explain kinetic energy",
            "what is work in physics", "what is power in physics", "conservation of energy"
        ],
        emojis=["⚡"],
        responses=[
            "⚡ **Work, Energy & Power:**\n\n• **Kinetic Energy (KE):** Energy of motion (`KE = ½mv²`).\n• **Potential Energy (PE):** Stored energy due to position or height (`PE = mgh`).\n• **Work:** Energy transferred when a force moves an object (`Work = Force × distance`, measured in Joules `J`).\n• **Power:** Rate at which work is done (`Power = Work / time`, measured in Watts `W`).\n• **Law of Conservation of Energy:** Energy cannot be created or destroyed, only transformed from one form to another."
        ],
        weight=1.3
    ),
    Intent(
        name="PHYSICS_ELECTRICITY_OHM",
        keywords=["electricity", "current", "voltage", "resistance", "ohm", "ohms"],
        phrases=[
            "what is ohm's law", "what is ohms law", "explain ohms law", "define ohms law",
            "what is electricity", "what is electric current", "what is voltage",
            "what is resistance", "explain electricity"
        ],
        emojis=["⚡", "🔌"],
        responses=[
            "⚡ **Electricity & Ohm's Law:**\n\n• **Ohm's Law:** Voltage across a conductor is directly proportional to current through it (`V = I × R`).\n• **Voltage (V):** Electrical potential difference that pushes charge (measured in Volts `V`).\n• **Current (I):** The flow rate of electric charge/electrons (measured in Amperes `A`).\n• **Resistance (R):** Opposition to the flow of electric current (measured in Ohms `Ω`)."
        ],
        weight=1.35
    ),
    Intent(
        name="PHYSICS_LIGHT_OPTICS",
        keywords=["light", "refraction", "reflection", "optics"],
        phrases=[
            "what is refraction", "define refraction", "explain refraction",
            "what is reflection", "define reflection", "reflection vs refraction",
            "what is light", "speed of light"
        ],
        emojis=["💡"],
        responses=[
            "💡 **Light & Optics:**\n\n• **Reflection:** The bouncing back of light waves when they strike a reflective surface (Law: Angle of Incidence = Angle of Reflection).\n• **Refraction:** The bending of light as it passes from one medium into another of different optical density due to a change in wave speed (e.g., light bending in water or glass lenses).\n• **Speed of Light:** `c ≈ 300,000 km/s` (or `3 × 10⁸ m/s`) in a vacuum."
        ],
        weight=1.3
    ),
    Intent(
        name="PHYSICS_SOUND_WAVES",
        keywords=["sound", "waves", "frequency", "wavelength"],
        phrases=[
            "what is sound", "what are waves", "what is frequency", "what is wavelength",
            "speed of sound", "how does sound travel", "define frequency"
        ],
        emojis=["🔊"],
        responses=[
            "🔊 **Waves & Sound:**\n\n• **Sound Waves:** Longitudinal mechanical waves created by vibrating particles, traveling through solids, liquids, and gases (cannot travel in a vacuum).\n• **Frequency (f):** Number of complete wave cycles per second (measured in Hertz `Hz`). Determines pitch.\n• **Wavelength (λ):** The physical distance between two consecutive wave crests or compressions.\n• **Wave Equation:** `Wave Speed (v) = Frequency (f) × Wavelength (λ)`."
        ],
        weight=1.3
    ),

    # -----------------------------
    # 🔬 Science — Chemistry
    # -----------------------------
    Intent(
        name="CHEMISTRY_GENERAL",
        keywords=["chemistry", "chem"],
        phrases=[
            "what is chemistry", "what is chem", "tell me about chemistry", "tell me about chem",
            "explain chemistry", "define chemistry", "why study chemistry"
        ],
        emojis=["🧪"],
        responses=[
            "🧪 **Chemistry** is the branch of natural science that studies the composition, structure, properties, and transformations of matter at atomic and molecular levels."
        ],
        weight=1.3
    ),
    Intent(
        name="CHEMISTRY_ATOM_MOLECULE",
        keywords=["atom", "molecule", "proton", "neutron", "electron"],
        phrases=[
            "what is an atom", "define atom", "explain atom", "tell me about atoms",
            "what is a molecule", "define molecule", "explain molecule",
            "what are protons", "what are electrons", "what are neutrons",
            "atomic number", "structure of an atom"
        ],
        emojis=["⚛️"],
        responses=[
            "⚛️ **Atoms & Molecules:**\n\n• **Atom:** The fundamental building block of all chemical matter. Consists of a central nucleus (protons + neutrons) surrounded by orbiting electrons.\n• **Proton (+1):** Positively charged subatomic particle. Number of protons = Atomic Number.\n• **Neutron (0):** Neutral subatomic particle located in the nucleus.\n• **Electron (-1):** Negatively charged particle in electron shells.\n• **Molecule:** A group of two or more atoms held together by chemical bonds (e.g., `H₂O`, `O₂`)."
        ],
        weight=1.35
    ),
    Intent(
        name="CHEMISTRY_ELEMENT_COMPOUND",
        keywords=["element", "compound", "mixture", "periodic"],
        phrases=[
            "what is an element", "define element", "explain element",
            "what is a compound", "define compound", "explain compound",
            "what is a mixture", "what is the periodic table", "periodic table",
            "element vs compound", "difference between element and compound"
        ],
        emojis=["🧪"],
        responses=[
            "🧪 **Elements, Compounds & Mixtures:**\n\n• **Element:** A pure substance composed of only one type of atom (e.g., Hydrogen `H`, Gold `Au`, Oxygen `O`). All 118 known elements are arranged in the **Periodic Table**.\n• **Compound:** A substance formed when two or more distinct elements chemically combine in fixed proportions (e.g., Water `H₂O`, Table Salt `NaCl`).\n• **Mixture:** Physical combination of substances without chemical bonding (e.g., air, saltwater)."
        ],
        weight=1.35
    ),
    Intent(
        name="CHEMISTRY_BONDS",
        keywords=["bonds", "ionic", "covalent"],
        phrases=[
            "what is a covalent bond", "what is an ionic bond", "chemical bonds",
            "covalent bond", "ionic bond", "difference between ionic and covalent bonds",
            "define covalent bond", "define ionic bond"
        ],
        responses=[
            "🧪 **Chemical Bonds:**\n\n• **Ionic Bond:** Formed when electrons are transferred from a metal to a non-metal, creating oppositely charged ions that attract (e.g., `Na⁺` + `Cl⁻` → `NaCl`).\n• **Covalent Bond:** Formed when two non-metal atoms share one or more pairs of valence electrons to achieve stable outer shells (e.g., `H₂O`, `CH₄`).\n• **Metallic Bond:** Electrostatic attraction between positive metal ions and a sea of delocalized electrons."
        ],
        weight=1.35
    ),
    Intent(
        name="CHEMISTRY_ACIDS_BASES_PH",
        keywords=["acid", "acids", "base", "bases", "ph"],
        phrases=[
            "what is an acid", "what is a base", "what is ph", "define ph",
            "explain ph scale", "acids and bases", "what is neutralization",
            "define acid", "define base"
        ],
        responses=[
            "🧪 **Acids, Bases & pH Scale:**\n\n• **Acid:** A substance that releases Hydrogen ions (`H⁺`) in aqueous solution (pH < 7, tastes sour, turns litmus red, e.g., Lemon juice, `HCl`).\n• **Base (Alkali):** A substance that releases Hydroxide ions (`OH⁻`) in aqueous solution (pH > 7, feels slippery, turns litmus blue, e.g., Soap, `NaOH`).\n• **pH Scale:** Measures acidity/alkalinity from 0 to 14 (7 is Neutral, such as pure water).\n• **Neutralization:** Acid + Base → Salt + Water (`HCl + NaOH → NaCl + H₂O`)."
        ],
        weight=1.35
    ),
    Intent(
        name="CHEMISTRY_REACTIONS_OXIDATION",
        keywords=["oxidation", "reduction", "redox", "reactions"],
        phrases=[
            "what is oxidation", "what is reduction", "what is a redox reaction",
            "chemical reactions", "types of chemical reactions", "define oxidation", "define reduction"
        ],
        responses=[
            "🧪 **Chemical Reactions & Redox:**\n\n• **Oxidation:** The loss of electrons (or gain of oxygen) by a molecule, atom, or ion.\n• **Reduction:** The gain of electrons (or loss of oxygen) by a substance.\n• **Redox Reaction:** A chemical reaction where reduction and oxidation take place simultaneously (Mnemonic: **OIL RIG** — *Oxidation Is Loss, Reduction Is Gain* of electrons!)."
        ],
        weight=1.3
    ),

    # -----------------------------
    # 🔬 Science — Biology
    # -----------------------------
    Intent(
        name="BIOLOGY_GENERAL",
        keywords=["biology", "bio"],
        phrases=[
            "what is biology", "what is bio", "tell me about biology", "tell me about bio",
            "explain biology", "define biology", "why study biology"
        ],
        emojis=["🧬"],
        responses=[
            "🧬 **Biology** is the natural science that studies life and living organisms, including their physical structure, chemical processes, molecular interactions, cellular mechanics, physiological adaptations, and evolution!"
        ],
        weight=1.3
    ),
    Intent(
        name="BIOLOGY_CELL",
        keywords=["cell", "cells", "organelles", "nucleus"],
        phrases=[
            "what is a cell", "define cell", "explain cell", "cell biology",
            "plant cell vs animal cell", "what is the nucleus of a cell",
            "parts of a cell", "structure of a cell"
        ],
        emojis=["🧬"],
        responses=[
            "🧬 **Cell Biology:**\n\n• **Cell:** The basic structural and functional unit of all living organisms (often called the building blocks of life).\n• **Nucleus:** The control center of the cell holding genetic material (DNA).\n• **Mitochondria:** The 'powerhouse of the cell' that produces cellular energy (ATP) via respiration.\n• **Plant vs. Animal Cells:** Plant cells possess a rigid cellulose cell wall, large central vacuole, and chloroplasts for photosynthesis; animal cells do not."
        ],
        weight=1.3
    ),
    Intent(
        name="BIOLOGY_DNA_GENETICS",
        keywords=["dna", "rna", "gene", "genes", "chromosomes", "genetics"],
        phrases=[
            "what is dna", "define dna", "explain dna", "what is rna",
            "what are genes", "what are chromosomes", "tell me about dna",
            "structure of dna", "what is heredity"
        ],
        emojis=["🧬"],
        responses=[
            "🧬 **DNA & Genetics:**\n\n• **DNA (Deoxyribonucleic Acid):** The hereditary molecule that carries genetic instructions for the development, functioning, and reproduction of all living organisms. Structured as a double helix of four base pairs: Adenine (A), Thymine (T), Cytosine (C), and Guanine (G).\n• **Genes:** Specific segments of DNA that code for distinct functional proteins and traits.\n• **Chromosomes:** Tightly coiled thread-like structures of DNA located inside the cell nucleus (humans have 23 pairs / 46 chromosomes)."
        ],
        weight=1.35
    ),
    Intent(
        name="BIOLOGY_PHOTOSYNTHESIS",
        keywords=["photosynthesis", "chlorophyll"],
        phrases=[
            "what is photosynthesis", "define photosynthesis", "explain photosynthesis",
            "how does photosynthesis work", "photosynthesis formula", "what is chlorophyll"
        ],
        emojis=["🌱"],
        responses=[
            "🌱 **Photosynthesis:**\n\nThe biological process by which green plants, algae, and some bacteria convert sunlight, carbon dioxide, and water into glucose (food) and oxygen.\n\n• **Formula:** `6CO₂ + 6H₂O + Sunlight → C₆H₁₂O₆ (Glucose) + 6O₂`\n• **Chlorophyll:** The green pigment located in plant chloroplasts that captures light energy."
        ],
        weight=1.35
    ),
    Intent(
        name="BIOLOGY_HUMAN_BODY",
        keywords=["heart", "brain", "lungs", "digestive", "circulatory", "respiratory", "nervous"],
        phrases=[
            "what does the heart do", "what is the circulatory system", "what is the digestive system",
            "what is the respiratory system", "what is the nervous system", "what does the brain do",
            "human body systems", "what do lungs do"
        ],
        emojis=["🫀", "🧠", "🫁"],
        responses=[
            "🫀 **Human Body & Organ Systems:**\n\n• **Circulatory System (Heart & Blood):** Pumps oxygenated blood, nutrients, and hormones throughout the body via arteries, veins, and capillaries.\n• **Respiratory System (Lungs):** Facilitates gas exchange — taking in Oxygen (`O₂`) and expelling Carbon Dioxide (`CO₂`).\n• **Nervous System (Brain & Nerves):** Sends electrical impulses and coordinates sensory perception, voluntary motion, and cognition.\n• **Digestive System:** Breaks down nutrients from food for cellular absorption and energy."
        ],
        weight=1.35
    ),
    Intent(
        name="BIOLOGY_ECOSYSTEM",
        keywords=["ecosystem", "ecosystems", "biodiversity", "producers", "consumers", "decomposers"],
        phrases=[
            "what is an ecosystem", "define ecosystem", "explain ecosystem",
            "what is a food chain", "producers and consumers", "what are decomposers",
            "what is biodiversity", "tell me about ecosystems"
        ],
        emojis=["🌿"],
        responses=[
            "🌿 **Ecology & Ecosystems:**\n\n• **Ecosystem:** A geographic community where living organisms (biotic factors like plants and animals) interact with each other and their non-living environment (abiotic factors like water, rocks, and climate).\n• **Food Chain:** Energy flow hierarchy from **Producers** (plants) → **Primary Consumers** (herbivores) → **Secondary Consumers** (carnivores) → **Decomposers** (fungi/bacteria that recycle organic matter).\n• **Biodiversity:** The variety of life across species and ecosystems on Earth."
        ],
        weight=1.3
    ),

    # -----------------------------
    # 🔬 Science — General Science
    # -----------------------------
    Intent(
        name="SCIENCE_SOLAR_SYSTEM",
        keywords=["planets", "solar", "sun", "moon", "earth"],
        phrases=[
            "how many planets are there", "what is the solar system", "solar system",
            "planets in order", "tell me about the planets", "planets in the solar system",
            "sun and moon", "what is the sun", "what is the moon"
        ],
        emojis=["🪐", "☀️", "🌕"],
        responses=[
            "🪐 **The Solar System:**\n\nOur Solar System consists of our central star (the **Sun**), 8 official planets, dwarf planets (like Pluto), moons, asteroids, and comets.\n\n• **8 Planets in Order from the Sun:**\n1. Mercury  2. Venus  3. Earth  4. Mars (Terrestrial rocky planets)\n5. Jupiter  6. Saturn  7. Uranus  8. Neptune (Gas & ice giants)"
        ],
        weight=1.35
    ),
    Intent(
        name="SCIENCE_WATER_CYCLE",
        keywords=["water", "cycle", "atmosphere"],
        phrases=[
            "what is the water cycle", "explain the water cycle", "water cycle steps",
            "water cycle", "how does the water cycle work", "what is evaporation"
        ],
        emojis=["💧"],
        responses=[
            "💧 **The Water Cycle (Hydrologic Cycle):**\n\nThe continuous global circulation of water between Earth's surface and atmosphere:\n\n1. **Evaporation & Transpiration:** Sun heats liquid water into water vapor rising into the air.\n2. **Condensation:** Water vapor cools and condenses into clouds.\n3. **Precipitation:** Clouds release moisture as rain, snow, sleet, or hail.\n4. **Collection & Runoff:** Water gathers into rivers, lakes, and oceans, repeating the cycle!"
        ],
        weight=1.35
    ),
    Intent(
        name="SCIENCE_RENEWABLE_ENERGY",
        keywords=["renewable", "greenhouse", "pollution", "solar", "wind"],
        phrases=[
            "what is renewable energy", "renewable energy", "what is the greenhouse effect",
            "greenhouse effect", "solar energy", "wind energy", "types of renewable energy",
            "climate change vs global warming"
        ],
        emojis=["🌱", "☀️", "💨"],
        responses=[
            "🌱 **Renewable Energy & Climate:**\n\n• **Renewable Energy:** Clean energy collected from naturally replenishing resources that produce zero direct greenhouse emissions (e.g., Solar, Wind, Hydroelectric, Geothermal).\n• **Greenhouse Effect:** Natural warming process where greenhouse gases (like `CO₂`, `CH₄`, and water vapor) trap heat in Earth's atmosphere. Excessive emissions intensify global temperatures and drive climate change."
        ],
        weight=1.35
    ),
    Intent(
        name="SCIENCE_SCIENTIFIC_METHOD",
        keywords=["scientific", "method", "hypothesis"],
        phrases=[
            "what is the scientific method", "scientific method", "steps of the scientific method",
            "what is a hypothesis", "explain scientific method"
        ],
        emojis=["🔬"],
        responses=[
            "🔬 **The Scientific Method:**\n\nA systematic, empirical process used by scientists to explore observations and answer questions:\n\n1. **Observation:** Identify a phenomenon or question.\n2. **Research:** Gather background knowledge.\n3. **Hypothesis:** Formulate a testable prediction.\n4. **Experiment:** Test the hypothesis under controlled conditions.\n5. **Data Analysis:** Analyze data and metrics.\n6. **Conclusion:** Accept, refine, or reject the hypothesis and publish findings!"
        ],
        weight=1.35
    ),

    # -----------------------------
    # 📖 English & Language — Grammar & Writing
    # -----------------------------
    Intent(
        name="ENGLISH_GENERAL",
        keywords=["english", "eng", "language"],
        phrases=[
            "what is english", "tell me about english", "explain english",
            "why study english", "what is the english language"
        ],
        emojis=["📖"],
        responses=[
            "📖 **English** is a West Germanic language that has become the primary global lingua franca for international communication, science, technology, aviation, business, and web development!"
        ],
        weight=1.3
    ),
    Intent(
        name="ENGLISH_NOUN",
        keywords=["noun", "nouns"],
        phrases=[
            "what is a noun", "define noun", "explain nouns", "types of nouns",
            "what are nouns", "examples of nouns", "tell me about nouns"
        ],
        responses=[
            "📖 **Nouns:**\n\nA **Noun** is a part of speech that names a person, place, thing, animal, or idea.\n\n• **Common Noun:** General names (e.g., *city, book, teacher*).\n• **Proper Noun:** Specific capitalized names (e.g., *Paris, NovaAI, William*).\n• **Abstract Noun:** Intangible concepts and feelings (e.g., *courage, freedom, happiness*).\n• **Collective Noun:** Groups (e.g., *team, flock, herd*)."
        ],
        weight=1.35
    ),
    Intent(
        name="ENGLISH_VERB",
        keywords=["verb", "verbs"],
        phrases=[
            "what is a verb", "define verb", "explain verbs", "what are verbs",
            "types of verbs", "examples of verbs", "helping verbs"
        ],
        responses=[
            "📖 **Verbs:**\n\nA **Verb** is a word that expresses an action, occurrence, or state of being (often called the engine of a sentence).\n\n• **Action Verbs:** Physical or mental actions (e.g., *run, write, think, code*).\n• **Linking / State Verbs:** Connect subjects to descriptions (e.g., *is, seem, become*).\n• **Helping / Auxiliary Verbs:** Support main verbs to form tenses (e.g., *have, has, will, can, should*)."
        ],
        weight=1.35
    ),
    Intent(
        name="ENGLISH_ADJECTIVE",
        keywords=["adjective", "adjectives"],
        phrases=[
            "what is an adjective", "define adjective", "explain adjectives",
            "what are adjectives", "examples of adjectives", "degrees of adjectives"
        ],
        responses=[
            "📖 **Adjectives:**\n\nAn **Adjective** is a word that describes, qualifies, or modifies a noun or pronoun by providing details on quantity, quality, size, color, or origin.\n\n• **Examples:** *bright screen, fast runner, delicious apple*.\n• **Degrees of Comparison:**\n  1. Positive: *smart*\n  2. Comparative: *smarter*\n  3. Superlative: *smartest*"
        ],
        weight=1.35
    ),
    Intent(
        name="ENGLISH_ADVERB",
        keywords=["adverb", "adverbs"],
        phrases=[
            "what is an adverb", "define adverb", "explain adverbs",
            "what are adverbs", "examples of adverbs"
        ],
        responses=[
            "📖 **Adverbs:**\n\nAn **Adverb** modifies a verb, an adjective, or another adverb. It explains *how, when, where, why, or to what extent* an action occurs (often ending in `-ly`).\n\n• **Manner (How):** *He typed **quickly**.*\n• **Time (When):** *We will meet **tomorrow**.*\n• **Degree (How much):** *The code is **extremely** clean.*"
        ],
        weight=1.35
    ),
    Intent(
        name="ENGLISH_PREPOSITION_CONJUNCTION",
        keywords=["preposition", "prepositions", "conjunction", "conjunctions"],
        phrases=[
            "what are prepositions", "what is a preposition", "define preposition",
            "what are conjunctions", "what is a conjunction", "define conjunction"
        ],
        responses=[
            "📖 **Prepositions & Conjunctions:**\n\n• **Prepositions:** Words showing spatial, temporal, or logical relationships between nouns and other sentence elements (e.g., *in, on, at, under, through, between*).\n• **Conjunctions:** Words that connect words, phrases, or clauses (e.g., Coordinating **FANBOYS**: *For, And, Nor, But, Or, Yet, So*; Subordinating: *because, although, since*)."
        ],
        weight=1.35
    ),
    Intent(
        name="ENGLISH_VOICE",
        keywords=["voice", "active", "passive"],
        phrases=[
            "what is active voice", "what is passive voice", "active vs passive voice",
            "difference between active and passive voice", "active and passive voice"
        ],
        responses=[
            "📖 **Active vs. Passive Voice:**\n\n• **Active Voice:** The subject performs the action (Direct & clear).\n  *Example:* \"Ada wrote the Python program.\"\n• **Passive Voice:** The subject receives the action (Used when the actor is unknown or less important).\n  *Example:* \"The Python program was written by Ada.\""
        ],
        weight=1.35
    ),
    Intent(
        name="ENGLISH_TENSES",
        keywords=["tense", "tenses", "present", "past", "future"],
        phrases=[
            "what are tenses", "what are the types of tenses", "explain tenses",
            "what is present tense", "what is past tense", "what is future tense",
            "what is present continuous", "what is past perfect", "what is future perfect"
        ],
        responses=[
            "📖 **English Tenses Overview:**\n\nEnglish has 3 primary timeframes divided into 4 aspects (12 total tenses):\n\n• **Present Tenses:**\n  - Simple Present: *I code.*\n  - Present Continuous: *I am coding.*\n  - Present Perfect: *I have coded.*\n  - Present Perfect Continuous: *I have been coding.*\n\n• **Past Tenses:**\n  - Simple Past: *I coded.*\n  - Past Continuous: *I was coding.*\n  - Past Perfect: *I had coded.*\n\n• **Future Tenses:**\n  - Simple Future: *I will code.*\n  - Future Continuous: *I will be coding.*\n  - Future Perfect: *I will have coded.*"
        ],
        weight=1.35
    ),
    Intent(
        name="ENGLISH_WRITING",
        keywords=["email", "formal", "informal", "paragraph", "writing"],
        phrases=[
            "how do i write a formal email", "formal vs informal english",
            "what is a paragraph", "how should i write an introduction",
            "how to write a good paragraph", "formal email writing"
        ],
        responses=[
            "📝 **Writing Basics & Formal Communication:**\n\n• **Formal Email Structure:**\n  1. Clear, concise Subject Line\n  2. Professional Salutation (*Dear [Name],* or *Dear Hiring Team,*)\n  3. Purpose statement in opening sentence\n  4. Focused body paragraph(s) with bullet points where useful\n  5. Actionable closing (*I look forward to hearing from you.*)\n  6. Professional sign-off (*Sincerely,* or *Best regards, [Your Name]*)\n\n• **Formal vs Informal:** Formal English avoids slang and contractions (*do not* instead of *don't*), maintaining an objective, respectful tone."
        ],
        weight=1.35
    ),
]


# =============================================================================
# 6. INTENT CLASSIFICATION & CONFIDENCE SCORING ENGINE
# =============================================================================

CONFIDENCE_THRESHOLD: float = 0.35


def score_intent(
    normalized_msg: str,
    tokens: List[str],
    extracted_emojis: List[str],
    intent: Intent
) -> float:
    """Calculates confidence score for a message matching an intent."""
    score = 0.0
    text_matched = False

    # 1. Exact phrase match
    for phrase in intent.phrases:
        if normalized_msg == phrase:
            score = max(score, 1.0 * intent.weight)
            text_matched = True
        elif re.search(r"\b" + re.escape(phrase) + r"\b", normalized_msg):
            ratio = len(phrase) / max(len(normalized_msg), 1)
            score = max(score, (0.70 + (0.30 * ratio)) * intent.weight)
            text_matched = True

    # 2. Regex pattern match
    for pattern in intent.patterns:
        match = pattern.search(normalized_msg)
        if match:
            score = max(score, 0.90 * intent.weight)
            text_matched = True

    # 3. Keyword matching & density
    if intent.keywords:
        matching_keywords = []
        for k in intent.keywords:
            if " " in k:
                if re.search(r"\b" + re.escape(k) + r"\b", normalized_msg):
                    matching_keywords.append(k)
            else:
                if k in tokens:
                    matching_keywords.append(k)

        num_matched = len(matching_keywords)
        total_keywords = len(intent.keywords)

        if intent.requires_all_keywords:
            if num_matched == total_keywords:
                score = max(score, 0.85 * intent.weight)
                text_matched = True
        else:
            if num_matched > 0:
                density = num_matched / max(len(tokens), 1)
                coverage = num_matched / total_keywords
                keyword_score = (0.40 * coverage + 0.40 * density + (0.10 * num_matched)) * intent.weight
                score = max(score, keyword_score)
                text_matched = True

    # 4. Emoji matching & sentiment
    if intent.emojis and extracted_emojis:
        matched_emojis = [e for e in extracted_emojis if e in intent.emojis]
        if matched_emojis:
            if not tokens:
                count_bonus = min(len(matched_emojis) * 0.05, 0.10)
                emoji_score = (0.90 + count_bonus) * intent.weight
                score = max(score, emoji_score)
            else:
                if text_matched:
                    score += 0.15
                else:
                    emoji_score = 0.45 * intent.weight
                    score = max(score, emoji_score)

    return score


def detect_intent(message: str) -> Tuple[Optional[Intent], float]:
    """Detects best-matching intent for a message."""
    if not message:
        return None, 0.0

    extracted_emojis = extract_emojis(message)
    normalized_msg = normalize_text(message)

    if not normalized_msg and not extracted_emojis:
        return None, 0.0

    tokens = normalized_msg.split()

    best_intent: Optional[Intent] = None
    best_score: float = 0.0

    for intent in INTENTS:
        score = score_intent(normalized_msg, tokens, extracted_emojis, intent)
        if score > best_score:
            best_score = score
            best_intent = intent

    return best_intent, best_score


# =============================================================================
# 7. MAIN CHATBOT RESPONSE ENTRY POINT
# =============================================================================

def get_response(message: str) -> str:
    """Main interface for NovaAI rule-based engine."""
    if not message or not message.strip():
        return "Please type a message to start chatting!"

    raw_msg = message.strip()

    # 1. Test mathematical calculations & formulas
    math_result = solve_math_query(raw_msg)
    if math_result:
        return math_result

    # 2. Test language & vocabulary dynamic handlers
    synonym_result = solve_synonym_query(raw_msg)
    if synonym_result:
        return synonym_result

    antonym_result = solve_antonym_query(raw_msg)
    if antonym_result:
        return antonym_result

    vocab_result = solve_vocabulary_query(raw_msg)
    if vocab_result:
        return vocab_result

    correction_result = solve_sentence_correction_query(raw_msg)
    if correction_result:
        return correction_result

    # 3. Detect intent from rule-based intent registry
    best_intent, confidence = detect_intent(raw_msg)

    if best_intent and confidence >= CONFIDENCE_THRESHOLD:
        return best_intent.get_response()

    # 4. Fallback response
    return random.choice(FALLBACK_RESPONSES)