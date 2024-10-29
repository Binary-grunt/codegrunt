from config.language_options import LANGUAGES


class CLIInputs:

    def __init__(self):
        self.language_choice = None
        self.subject = None

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
            return CLIInputs.get_subject()

    def start_session(self):
        print("Starting a new session...")
        self.get_language_choice()
        self.get_subject()
        print(f"Session ready! Language: {
              LANGUAGES[self.language_choice]}, Subject: {self.subject}")
