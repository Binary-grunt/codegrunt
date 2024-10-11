from openai_helpers import generated_exercice
import os


def create_folder(lang: str, subject: str) -> str:
    directory_name = f"{subject}_{lang}"

    try:
        os.mkdir(directory_name)
        print(f"Directory '{directory_name}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_name}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{directory_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return directory_name


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
            directory = create_folder(lang, subject)
            exercice = generated_exercice(subject, language_name)
            write_file(directory, subject, extension, exercice)

            print(f"{language_name} file generated successfully in '{directory}'.")
        except Exception as e:
            print(f"An error occurred while generating the file: {e}")
    else:
        print("Invalid language. Please select a language avaiable")


def write_file(directory: str, subject: str, extension: str, generated_text: str) -> str:
    num = 0
    while True:
        file_name = f"{subject}_{num}.{extension}"
        file_path = os.path.join(directory, file_name)
        if not os.path.exists(file_path):
            break
        num += 1

    # Écrire le fichier dans le dossier spécifié
    with open(file_path, "w") as generated_file:
        generated_file.write(generated_text)

    print(f"File '{file_name}' generated successfully in '{directory}'.")

    return file_path
