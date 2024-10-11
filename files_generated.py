from openai_helpers import generated_exercice, write_file_ai


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
            write_file_ai(subject, extension, exercice)

            print(f"{language_name} files generated.")
        except Exception as e:
            print(f"An error occurred while generating the file: {e}")
    else:
        print("Invalid language. Please select a language avaiable")
