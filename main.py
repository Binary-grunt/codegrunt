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
    exercise_generated = False  # State to check if exercise has been generated

    while score_manager.exercises_completed() < 10:
        if not exercise_generated:
            print(" _____________________ \n"
                  "\n"
                  "Available commands: \n"
                  "generate - Generate a new exercise\n"
                  "\n")
        else:
            print(
                  "\n"
                  "After completing it, use the 'submit' command to evaluate it.\n"
                  "submit - Submit an exercise\n"
                  "\n")

        choice_command = input("Choose a command: ")

        if choice_command == "generate" and not exercise_generated:
            generate_command(cli_inputs)
            exercise_generated = True
        elif choice_command == "submit" and exercise_generated:
            submit_command(score_manager, cli_inputs)
        else:
            print("Invalid command. Please choose a valid option.")

if __name__ == '__main__':
    main()
