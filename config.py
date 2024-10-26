# Languages options
LANGUAGES = {
    '1': 'PHP',
    '2': 'JavaScript',
    '3': 'Python',
}


# Global dictionary for file extensions and language names
LANGUAGE_EXTENSIONS = {
    "javascript": ("js", "JavaScript"),
    "python": ("py", "Python"),
    "php": ("php", "PHP"),
}

FILE_EXTENSION_MAP = {
    "py": "python",
    "js": "javascript",
    "php": "php"
}

# Path for the current exercise file
CURRENT_EXERCISE_FILE_PATH = None


def set_current_exercise_path(path: str):
    """Set the path for the current exercise file."""
    global CURRENT_EXERCISE_FILE_PATH
    CURRENT_EXERCISE_FILE_PATH = path


def get_current_exercise_path() -> str:
    """Get the path for the current exercise file."""
    return CURRENT_EXERCISE_FILE_PATH


# Score settings
GLOBAL_SCORE = {
    "total_score": 0,
    "exercises_completed": 0
}

#  Path for the file that contains the evaluated exercises
EVALUATED_FILES = "evaluated_exercises.txt"
