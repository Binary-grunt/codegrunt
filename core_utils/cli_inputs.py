from config import LANGUAGES


def display_language_options():
    print("Please select the language -")
    for key, value in LANGUAGES.items():
        print(f"{key}. {value}")


def get_language_choice():
    while True:
        display_language_options()

        lang_choice = input(
            "What's the programming language you want to learn? ")

        if lang_choice in LANGUAGES:
            return lang_choice
        else:
            print("Invalid language selection. Please enter 1, 2, or 3.")


def get_subject():
    subject = input("What's the subject you want to practice? ").strip()
    if subject:
        return subject
    else:
        print("The subject cannot be empty. Please try again.")
        return get_subject()
