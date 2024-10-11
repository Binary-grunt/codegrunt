from openai_helpers import generated_exercice
import os


def create_file(lang: str, subject: str) -> str:

    lang_dictionnaries = {
        "javascript": ("js", "JavaScript"),
        "python": ("py", "Python"),
        "php": ("php", "PHP"),
    }

    lang = lang.lower()

    if lang in lang_dictionnaries:
        extension, language_name = lang_dictionnaries[lang]
        try:
            exercice = generated_exercice(subject, language_name)
            write_file(subject, extension, exercice)

            print(f"{language_name} files generated.")
        except Exception as e:
            print(f"An error occurred while generating the file: {e}")
    else:
        print("Invalid language. Please select a language avaiable")


def write_file(subject: str, extension: str, generated_text: str) -> str:
    num = 0
    while True:
        file_name = f"{subject}_{num}.{extension}"
        if not os.path.exists(file_name):
            break
        num += 1
    with open(file_name, "w") as generated_file:
        generated_file.write(generated_text)
    print(f"File '{file_name}' generated successfully.")
