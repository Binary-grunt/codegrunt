import os
from core_utils.path_manager import PathManager


class ScoreManager:

    def __init__(self):
        self._total_score = 0
        self._exercises_completed = 0

    def score_count(self, result: str) -> None:
        """Update score based on evaluation result."""
        if "True" in result:
            self._total_score += 10
            self._exercises_completed += 1
            print(f'Good answer, your score is now: {
                  self._total_score} / 100.')
        else:
            print(f"Wrong answer, your score is: {self._total_score} / 100.")

    def mark_as_evaluated(self, file_path: str) -> None:
        """Record the evaluated file in evaluated_exercises.txt."""
        evaluated_file_path = PathManager.get_evaluated_file_path(file_path)
        with open(evaluated_file_path, 'a') as file:
            file.write(file_path + '\n')

    def has_been_evaluated(self, file_path: str) -> bool:
        """Check if a file has already been evaluated."""
        evaluated_file_path = PathManager.get_evaluated_file_path(file_path)
        if not os.path.exists(evaluated_file_path):
            return False

        with open(evaluated_file_path, 'r') as file:
            evaluated_files = file.read().splitlines()
        return file_path in evaluated_files

    def total_score(self) -> dict:
        """Return the total score and number of exercises completed."""
        return self._total_score

    def exercises_completed(self) -> int:
        """Return the number of exercises completed."""
        return self._exercises_completed
