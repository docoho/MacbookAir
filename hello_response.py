#!/usr/bin/env python3
"""
A robust script that responds to various forms of "hello" input.
Features:
- Case insensitive input matching
- Multiple hello variations
- Exit commands
- Input validation
- Error handling
"""

import sys
import re
from typing import Optional


def normalize_input(user_input: str) -> str:
    """Normalize user input by stripping whitespace and converting to lowercase."""
    if user_input is None:
        return ""
    return user_input.strip().lower()


def is_hello_command(input_text: str) -> bool:
    """Check if input matches various hello patterns."""
    hello_patterns = [
        # English greetings
        r'^hello$',
        r'^hi$',
        r'^hey$',
        r'^hello there$',
        r'^hi there$',
        r'^hey there$',
        r'^howdy$',
        r'^yo$',
        r'^sup$',
        r'^what\'?s up$',
        r'^whats up$',
        r'^wassup$',
        r'^good morning$',
        r'^good afternoon$',
        r'^good evening$',
        r'^good day$',
        r'^greetings$',
        r'^salutations$',
        r'^welcome$',
        r'^how are you$',
        r'^how do you do$',
        r'^pleased to meet you$',
        r'^nice to meet you$',

        # Spanish greetings
        r'^hola$',
        r'^buenos dias$',
        r'^buenas tardes$',
        r'^buenas noches$',

        # French greetings
        r'^bonjour$',
        r'^salut$',
        r'^bonsoir$',

        # German greetings
        r'^hallo$',
        r'^guten tag$',
        r'^guten morgen$',

        # Italian greetings
        r'^ciao$',
        r'^buongiorno$',
        r'^buonasera$',

        # Portuguese greetings
        r'^oi$',
        r'^ola$',
        r'^bom dia$',

        # Asian greetings
        r'^namaste$',
        r'^konnichiwa$',
        r'^ni hao$',
        r'^annyeong$',
        r'^sawadee$',

        # Other languages
        r'^shalom$',
        r'^salam$',
        r'^jambo$',
        r'^aloha$',
        r'^ahoy$',
        r'^privyet$',
        r'^zdravo$'
    ]

    normalized = normalize_input(input_text)

    for pattern in hello_patterns:
        if re.match(pattern, normalized, re.IGNORECASE):
            return True

    return False


def is_exit_command(input_text: str) -> bool:
    """Check if user wants to exit."""
    exit_commands = ['exit', 'quit', 'q', 'bye', 'goodbye', 'stop', 'end']
    normalized = normalize_input(input_text)
    return normalized in exit_commands


def is_help_command(input_text: str) -> bool:
    """Check if user wants help."""
    help_commands = ['help', '?', 'commands', 'info', 'usage']
    normalized = normalize_input(input_text)
    return normalized in help_commands


def show_help() -> None:
    """Display help information."""
    print("\n" + "="*50)
    print("HELLO RESPONSE SCRIPT - HELP")
    print("="*50)
    print("\nThis script responds to various greeting forms.")
    print("\nCommands:")
    print("  English:   hello, hi, hey, howdy, yo, sup, what's up,")
    print("             good morning/afternoon/evening/day, greetings,")
    print("             how are you, nice to meet you, welcome")
    print("  Spanish:   hola, buenos dias, buenas tardes, buenas noches")
    print("  French:    bonjour, salut, bonsoir")
    print("  German:    hallo, guten tag, guten morgen")
    print("  Italian:   ciao, buongiorno, buonasera")
    print("  Portuguese: oi, ola, bom dia")
    print("  Japanese:  konnichiwa")
    print("  Chinese:   ni hao")
    print("  Korean:    annyeong")
    print("  Thai:      sawadee")
    print("  Hindi:     namaste")
    print("  Hebrew:    shalom")
    print("  Arabic:    salam")
    print("  Swahili:   jambo")
    print("  Hawaiian:  aloha")
    print("  Russian:   privyet")
    print("  Serbian:   zdravo")
    print("\n  Help:      help, ?, commands, info, usage")
    print("  Exit:      exit, quit, q, bye, goodbye, stop, end")
    print("\nThe script is case-insensitive and handles extra spaces.")
    print("="*50 + "\n")


def show_greeting(input_text: str) -> None:
    """Display appropriate greeting response."""
    normalized = normalize_input(input_text)

    responses = {
        # English greetings
        'hello': "Hello! Welcome!",
        'hi': "Hi there! Nice to see you!",
        'hey': "Hey! How's it going?",
        'hello there': "Hello there! General Kenobi... 😉",
        'hi there': "Hi there! Wonderful to see you!",
        'hey there': "Hey there! What's happening?",
        'howdy': "Howdy, partner! 🤠",
        'yo': "Yo! What's good?",
        'sup': "Sup! How's everything?",
        "what's up": "Not much, you? What's up with you?",
        'whats up': "Not much, you? What's up with you?",
        'wassup': "Wassup! Everything cool?",
        'good morning': "Good morning! Rise and shine!",
        'good afternoon': "Good afternoon! Hope you're having a great day!",
        'good evening': "Good evening! How was your day?",
        'good day': "Good day! Wishing you the best!",
        'greetings': "Greetings and salutations!",
        'salutations': "Salutations! A pleasure to meet you!",
        'welcome': "Welcome! So glad you're here!",
        'how are you': "I'm doing great, thanks for asking! How are you?",
        'how do you do': "How do you do? Pleased to make your acquaintance!",
        'pleased to meet you': "Pleased to meet you too! The pleasure is mine!",
        'nice to meet you': "Nice to meet you as well! Great to connect!",

        # Spanish greetings
        'hola': "¡Hola! ¡Bienvenido!",
        'buenos dias': "¡Buenos días! ¡Que tengas un excelente día!",
        'buenas tardes': "¡Buenas tardes! ¿Cómo estás?",
        'buenas noches': "¡Buenas noches! Que descanses bien.",

        # French greetings
        'bonjour': "Bonjour! Comment allez-vous?",
        'salut': "Salut! Ça va?",
        'bonsoir': "Bonsoir! Bonne soirée!",

        # German greetings
        'hallo': "Hallo! Wie geht's?",
        'guten tag': "Guten Tag! Wie geht es Ihnen?",
        'guten morgen': "Guten Morgen! Schönen Tag noch!",

        # Italian greetings
        'ciao': "Ciao! Piacere di conoscerti!",
        'buongiorno': "Buongiorno! Come stai?",
        'buonasera': "Buonasera! Bella serata!",

        # Portuguese greetings
        'oi': "Oi! Tudo bem?",
        'ola': "Olá! Como vai?",
        'bom dia': "Bom dia! Tenha um ótimo dia!",

        # Asian greetings
        'namaste': "Namaste! 🙏",
        'konnichiwa': "こんにちは (Konnichiwa)! Welcome!",
        'ni hao': "你好 (Nǐ hǎo)! Hello!",
        'annyeong': "안녕 (Annyeong)! Hello!",
        'sawadee': "สวัสดี (Sawadee)! Welcome!",

        # Other languages
        'shalom': "Shalom! שלום Peace be with you!",
        'salam': "As-salamu alaykum! السلام عليكم Peace!",
        'jambo': "Jambo! Habari gani?",
        'aloha': "Aloha! 🌺 Welcome to paradise!",
        'ahoy': "Ahoy there, matey! ⚓",
        'privyet': "Привет (Privyet)! Как дела?",
        'zdravo': "Zdravo! Kako si?"
    }

    # Find matching response
    response = responses.get(normalized, "Hello! Great to see you!")
    print(f"\n🌟 {response} 🌟\n")


def get_user_input() -> Optional[str]:
    """Safely get user input."""
    try:
        return input("Enter something (or 'help' for commands): ")
    except (EOFError, KeyboardInterrupt):
        print("\n\nGoodbye!")
        return None
    except Exception as e:
        print(f"\nError reading input: {e}")
        return None


def main():
    """Main program loop."""
    print("\n" + "="*50)
    print("🚀 HELLO RESPONSE SCRIPT - ENHANCED VERSION 🚀")
    print("="*50)
    print("\nType 'hello' (or variations) to get a response!")
    print("Type 'help' for available commands or 'exit' to quit.\n")

    try:
        while True:
            user_input = get_user_input()

            if user_input is None:
                break

            if not user_input.strip():
                print("Please enter something. Type 'help' for commands.\n")
                continue

            if is_exit_command(user_input):
                print("\nThank you for using the Hello Response Script! 👋")
                print("Goodbye!\n")
                break

            if is_help_command(user_input):
                show_help()
                continue

            if is_hello_command(user_input):
                show_greeting(user_input)
            else:
                print(f"\nYou entered: '{user_input}'")
                print(
                    "Try typing 'hello' or similar greetings! Type 'help' for more options.\n")

    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Goodbye! 👋")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


# hello
# hey
