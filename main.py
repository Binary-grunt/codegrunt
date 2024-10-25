from commands.generate_command import generate_command
from commands.submit_command import submit_command
from config import GLOBAL_SCORE

# TODO: Add system of logging to log the result and explaination
# for each exercice in .txt or .md local link to the folder,
# push after each evaluate command


def main():
    print("Hello, Welcome to Codegrunt. It's generator of exercice.")

    while GLOBAL_SCORE["exercises_completed"] < 10:

        print(" _____________________ \n"
              "\n"
              "To continue, you have 1 command available \n"
              "generate - For generate exercice\n"
              )
        choice_command = input("Choice a command : ")

        if choice_command == "generate":
            generate_command()
        elif choice_command == "submit":
            # Evaluate the files
            analyze = input("Write the name of the file to evaluate : ")
            submit_command(analyze, GLOBAL_SCORE)


if __name__ == '__main__':
    main()
