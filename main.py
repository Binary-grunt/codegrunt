from openai_helpers import generated_exercice, analyze_code


def write_file_ai(subject: str, eof: str, generated_text: str) -> str:
    file_name = f"{subject}.{eof}"
    with open(file_name, "w") as generated_file:
        generated_file.write(generated_text)
    print(f"File '{file_name}' generated successfully.")


def read_code_file(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    result = analyze_code(code)
    count = 0
    for keyword in result:
        if keyword == "True":
            count += 1
            print(count)
    print(f'Count number = {count}, and reslt is now : {result}')


def create_file(lang: str, subject: str) -> str:
    lang = lang.lower()
    match lang:
        case "javascript":
            write_file_ai(subject, "js", generated_exercice(
                subject, "JavaScript"))
            print("Javascript files generated.")
        case "php":
            write_file_ai(subject, "php", generated_exercice(subject, "PHP"))
            print("PHP files generated.")
        case "python":
            write_file_ai(subject, "py", generated_exercice(subject, "Python"))
            print("Python files generated.")
        case _:
            print("Select correct language. Try again")


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

        lang = languages[lang_choice]  # Get the correct language name
        if lang and subject:
            create_file(lang, subject)
        else:
            print("The language or subject is invalid.")
    else:
        print("Invalid language selection. Please enter 1, 2, or 3.")


if __name__ == '__main__':
    while True:

        print("Hello, Welcome to Codegrunt. It's generator of exercice."
              "You will have 3 commands\n"
              "generate - For generate exercice\n"
              "evaluate - For correct the provided path exercice\n"
              )

        choice_command = input("Select your commands")

        if choice_command == "generate":
            generate_command()
        elif choice_command == "evaluate":
            # Evaluate the files
            analyze = input("Write the name of the file to evaluate")
            read_code_file(analyze)
