from commands import generate_command, read_code_file


# NOTE: Add system of logging to log the result and explaination
# for each exercice in .txt or .md local link to the folder,
# push after each evaluate command


if __name__ == '__main__':

    print("Hello, Welcome to Codegrunt. It's generator of exercice.")

    while True:

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
            read_code_file(analyze)
