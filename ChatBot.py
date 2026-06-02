import re
import random
import datetime

RULES = {
    # Greetings
    r"\b(hello|hi|hey|howdy|hola)\b": [
        "Hi there! How can I help you today?",
        "Hello! Great to see you. What's on your mind?",
        "Hey! I'm here and ready to chat.",
    ],

    # How are you
    r"\bhow are you\b|\bhow r u\b|\bhow do you do\b": [
        "I'm doing great, thanks for asking! How about you?",
        "Running smoothly! What can I do for you?",
        "All good on my end! How are you doing?",
    ],

    # User feeling good
    r"\bi('m| am) (good|fine|great|awesome|well|happy)\b": [
        "That's wonderful to hear! How can I assist you?",
        "Glad to know that! What would you like to talk about?",
    ],

    # User feeling bad
    r"\bi('m| am) (sad|bad|not good|not well|upset|tired|stressed)\b": [
        "I'm sorry to hear that. I hope things get better for you soon!",
        "That's tough. Remember, every hard day makes you stronger. ",
    ],

    # Name
    r"\bwhat('s| is) your name\b|\bwho are you\b": [
        "I'm Chat Bot — a Friend-based chatbot built for an friendly chat",
        "My name is Chat Bot. Nice to meet you!",
    ],

    # What can you do
    r"\bwhat can you do\b|\byour (features|abilities|skills)\b": [
        "I can chat with you, answer basic questions, tell the time/date, do simple math, and more!",
    ],

    # Time
    r"\bwhat (time|is the time)\b|\bcurrent time\b": [
        lambda: f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}.",
    ],

    # Date
    r"\bwhat (date|day|is today)\b|\btoday('s date)?\b": [
        lambda: f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}.",
    ],

    # Math — addition
    r"what is (\d+)\s*\+\s*(\d+)": [
        lambda m: f"{m.group(1)} + {m.group(2)} = {int(m.group(1)) + int(m.group(2))}",
    ],

    # Math — subtraction
    r"what is (\d+)\s*\-\s*(\d+)": [
        lambda m: f"{m.group(1)} - {m.group(2)} = {int(m.group(1)) - int(m.group(2))}",
    ],

    # Math — multiplication
    r"what is (\d+)\s*[\*x]\s*(\d+)": [
        lambda m: f"{m.group(1)} × {m.group(2)} = {int(m.group(1)) * int(m.group(2))}",
    ],

    # Age
    r"\bhow old are you\b|\byour age\b": [
        "I'm ageless — just lines of Python code! ",
        "I was born the day this script was written. Quite young!",
    ],

    # Creator
    r"\bwho (made|created|built|programmed) you\b": [
        "I was created by an AI enthusiast as part of a B.Tech internship project!",
    ],

    # Weather (simulated)
    r"\bweather\b": [
        "I don't have live weather access, but I recommend checking weather.com!",
    ],

    # Jokes
    r"\btell me a joke\b|\bjoke\b": [
        "Why do programmers prefer dark mode? Because light attracts bugs! ",
        "Why did the AI go to school? To improve its learning rate! ",
        "What's a computer's favorite snack? Microchips! ",
    ],

    # Help
    r"\bhelp\b|\bcommands\b|\bwhat can i (ask|say)\b": [
        (
            "You can ask me:\n"
            "  • hello / hi / hey\n"
            "  • how are you\n"
            "  • what is your name\n"
            "  • what time / date is it\n"
            "  • what is 5 + 3\n"
            "  • tell me a joke\n"
            "  • bye / goodbye\n"
            "  • Type 'quit' to exit"
        ),
    ],

    # Goodbye
    r"\b(bye|goodbye|see you|take care|cya|exit|quit)\b": [
        "Goodbye! Have a wonderful day! ",
        "See you later! Take care! ",
        "Bye! It was great chatting with you!",
    ],

    # Thank you
    r"\b(thanks|thank you|thx|ty)\b": [
        "You're welcome! ",
        "Happy to help! Anything else?",
        "Anytime! That's what I'm here for.",
    ],
}

# Fallback responses when no rule matches
FALLBACKS = [
    "Hmm, I'm not sure about that. Try asking something else or type 'help'.",
    "I didn't quite get that. Could you rephrase? Or type 'help' for options.",
    "That's outside my current knowledge. Try 'help' to see what I can do!",
]

EXIT_TRIGGERS = {"bye", "goodbye", "see you", "take care", "cya", "exit", "quit"}

def preprocess(text: str) -> str:
    """Lowercase and strip whitespace for uniform matching."""
    return text.lower().strip()


def get_response(user_input: str) -> tuple[str, bool]:
    """
    Match user input against rules using regex.
    Returns (response_text, should_exit).
    """
    cleaned = preprocess(user_input)

    for pattern, responses in RULES.items():
        match = re.search(pattern, cleaned)
        if match:
            chosen = random.choice(responses)

            if callable(chosen):
                try:
                    import inspect
                    sig = inspect.signature(chosen)
                    response = chosen(match) if sig.parameters else chosen()
                except Exception:
                    response = chosen()
            else:
                response = chosen

            should_exit = any(trigger in cleaned for trigger in EXIT_TRIGGERS)
            return response, should_exit

    return random.choice(FALLBACKS), False


def display_banner():
    """Print welcome """
    print(" Friendly Chatbot: ")
    print(" # Type 'help' to see available commands")
    print(" # Type 'quit' or 'bye' to exit")


def chat_loop():
    """Main conversation loop"""
    display_banner()

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nBot: Goodbye! See you next time! ")
            break

        if not user_input:
            print("Bot: Please type something! (or 'help' for options)")
            continue

        response, should_exit = get_response(user_input)
        print(f"Bot: {response}")

        if should_exit:
            break

    print("   Session ended. Thanks for chatting!")

if __name__ == "__main__":
    chat_loop()
