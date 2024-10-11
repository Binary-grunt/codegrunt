from generate_command import generate_command
from evaluated_command import evaluate_command

# TODO: Add system of logging to log the result and explaination
# for each exercice in .txt or .md local link to the folder,
# push after each evaluate command
global_score = {
    "total_score": 0,
    "exercises_completed": 0
}


def main():
    print("Hello, Welcome to Codegrunt. It's generator of exercice.")

    while global_score["exercises_completed"] < 10:

        print(" _____________________ \n"
              "\n"
              "To continue, you have 2 commands available \n"
              "generate - For generate exercice\n"
              "evaluate - For correct the provided path exercice\n"
              )
        choice_command = input("Choice a command : ")

        if choice_command == "generate":
            generate_command()
        elif choice_command == "evaluate":
            # Evaluate the files
            analyze = input("Write the name of the file to evaluate : ")
            evaluate_command(analyze, global_score)


if __name__ == '__main__':
    main()
