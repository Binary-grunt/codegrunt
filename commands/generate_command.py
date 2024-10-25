from exercise_file_generator import create_exercise_file
from config import LANGUAGES, set_current_exercise_path


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


def generate_command():
    lang_choice = get_language_choice()
    lang = LANGUAGES[lang_choice]
    subject = get_subject()

    if lang and subject:
        # Generate exercise file and store its path
        file_path = create_exercise_file(lang, subject)
        # Debugging output
        print(f"File generated at: {file_path}")

        if file_path:
            # Set the current exercise path
            set_current_exercise_path(file_path)
            print(f"Your current exercise is: {file_path}.")
            print("After completing it, use the 'submit' command to evaluate it.")
        else:
            print("Failed to generate the exercise file.")
    else:
        print("Failed to generate command due to invalid input.")
