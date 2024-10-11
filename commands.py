from files_generated import create_file
from openai_helpers import analyze_code


def generate_command():
    print("Please select the language -\n"
          "1. PHP\n"
          "2. JavaScript\n"
          "3. Python\n")

    lang_choice = input(
        "What's the programming language you want to learn? ")

    if lang_choice in ['1', '2', '3']:
        subject = input("What's the subject you want to practice? ")

        languages = {
            '1': 'PHP',
            '2': 'JavaScript',
            '3': 'Python',
        }
        lang = languages[lang_choice]
        if lang and subject:
            create_file(lang, subject)
        else:
            print("The language or subject is invalid.")
    else:
        print("Invalid language selection. Please enter 1, 2, or 3.")


def read_code_file(file_path):
    try:
        with open(file_path, 'r') as file:
            code = file.read()
        result = analyze_code(code)
        score = 0
        # TODO: Add logic for a score player for 100 points per section
        if "True" in result:
            score += 10
            print(f'Good answer, your score are now  : {score} / 100.')
        else:
            print(f"Wrong answer, you score is : {score} / 100.")
            # HACK: Delete the next print
        print(f'Count number = {score}, and result is now: {result}')
    except FileNotFoundError:
        print(f"Error: The file '{
            file_path}' was not found. Please check the file path and try again.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
