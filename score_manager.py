from config import EVALUATED_FILES
import os


def score_count(result: str, global_score: dict) -> str:
    if "True" in result:
        global_score["total_score"] += 10
        global_score["exercises_completed"] += 1
        print(f'Good answer, your score is now  : {
              global_score["total_score"]} / 100.')
    else:
        print(f"Wrong answer, your score is : {
              global_score['total_score']} / 100.")


def mark_as_evaluated(file_path: str) -> str:
    with open(EVALUATED_FILES, 'a') as file:
        file.write(file_path + '\n')


def has_been_evaluated(file_path: str) -> str:
    if not os.path.exists(EVALUATED_FILES):
        return False

    with open(EVALUATED_FILES, 'r') as file:
        # Lit tous les chemins de fichiers déjà évalués (avec extensions)
        evaluated_files = file.read().splitlines()
    # Retourne True si le chemin complet du fichier (y compris l'extension) est dans la liste
    return file_path in evaluated_files
