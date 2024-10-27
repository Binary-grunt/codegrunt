import os


def get_evaluated_file_path(file_path: str) -> str:
    """Get the path of evaluated_exercises.txt in the same directory as the file being evaluated."""
    directory = os.path.dirname(file_path)
    return os.path.join(directory, 'evaluated_exercises.txt')


def score_count(result: str, global_score: dict) -> str:
    if "True" in result:
        global_score["total_score"] += 10
        global_score["exercises_completed"] += 1
        print(f'Good answer, your score is now  : {
              global_score["total_score"]} / 100.')
    else:
        print(f"Wrong answer, your score is : {
              global_score['total_score']} / 100.")


def mark_as_evaluated(file_path: str) -> None:
    evaluated_file_path = get_evaluated_file_path(file_path)
    with open(evaluated_file_path, 'a') as file:
        file.write(file_path + '\n')


def has_been_evaluated(file_path: str) -> bool:
    evaluated_file_path = get_evaluated_file_path(file_path)
    if not os.path.exists(evaluated_file_path):
        return False

    with open(evaluated_file_path, 'r') as file:
        evaluated_files = file.read().splitlines()
    return file_path in evaluated_files
