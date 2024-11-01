from cli.generate_command import generate_command
from cli.submit_command import submit_command
from core_utils.score_manager import ScoreManager
from cli.inputs import Inputs

# TODO: Add system of logging to log the result and explaination
# for each exercice in .txt or .md local link to the folder,
# push after each evaluate command


def main():
    print("Hello, Welcome to Codegrunt. It's a generator of exercises.")

    cli_inputs = Inputs()
    score_manager = ScoreManager()
    while score_manager.exercises_completed() < 10:

        print(" _____________________ \n"
              "\n"
              "Available commands: \n"
              "generate - Generate a new exercise\n"
              " _____________________ \n"

              )

        choice_command = input("Choose a command: ")

        if choice_command == "generate":
            generate_command(cli_inputs)
        elif choice_command == "submit":
            submit_command(score_manager, cli_inputs)
        else:
            print("Invalid command. Please choose 'generate'")


if __name__ == '__main__':
    main()
