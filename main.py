from commands.generate_command import generate_command
from commands.submit_command import submit_command
from config import GLOBAL_SCORE

# TODO: Add system of logging to log the result and explaination
# for each exercice in .txt or .md local link to the folder,
# push after each evaluate command


def main():
    print("Hello, Welcome to Codegrunt. It's a generator of exercises.")

    while GLOBAL_SCORE["exercises_completed"] < 10:

        print(" _____________________ \n"
              "\n"
              "Available commands: \n"
              "generate - Generate a new exercise\n"
              "submit - Submit the current exercise for evaluation\n")

        choice_command = input("Choose a command: ")

        if choice_command == "generate":
            generate_command()
        elif choice_command == "submit":
            submit_command(GLOBAL_SCORE)
        else:
            print("Invalid command. Please choose 'generate' or 'submit'.")


if __name__ == '__main__':
    main()
