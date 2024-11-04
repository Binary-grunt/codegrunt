from config.language_options import LANGUAGES
import os


class Inputs:

    def __init__(self):
        self.language_choice = None
        self.subject = "" 

    def display_language_options(self):
        print("Please select the language -")
        for key, value in LANGUAGES.items():
            print(f"{key}. {value}")

    def get_language_choice(self):
        while True:
            self.display_language_options()
            lang_choice = input(
                "What's the programming language you want to learn? ")
            if lang_choice in LANGUAGES:
                self.language_choice = lang_choice
                return lang_choice
            else:
                print("Invalid language selection. Please enter 1, 2, or 3.")

    def get_subject(self):
        subject = input("What's the subject you want to practice? ").strip()
        if subject:
            self.subject = subject
            return subject
        else:
            print("The subject cannot be empty. Please try again.")
            return self.get_subject()

    def get_or_prompt_api_key(self) -> str:
        # Get API key from environment or prompt user if not found.
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            api_key = input("Enter your OpenAI API key: ").strip()
            if api_key:
                # Stock in environment for session use
                os.environ["OPENAI_API_KEY"] = api_key
                print(f"API key set for this session. Use:\n\nexport OPENAI_API_KEY={
                      api_key}\n\nin your terminal to set it permanently.")
            else:
                print("API key cannot be empty. Please try again.")
                return self.get_or_prompt_api_key()
        return api_key

    def start_session(self) -> None:
        print("Starting a new session...")
        self.get_language_choice()
        self.get_subject()
        if self.language_choice in LANGUAGES:
            print(f"Session ready! Language: {LANGUAGES[self.language_choice]}, Subject: {self.subject}")
        else:
            print("Invalid language choice.")
