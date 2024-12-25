import pytest
from unittest.mock import MagicMock
from core.exercise_generator import ExerciseGenerator
from common.utils.validator import Validator


# Mock Classes
class MockExerciseManager:
    def generate_exercise(self, subject, language, level):
        return f"# This is a {level} {language} exercise on {subject}"


class MockFileHandler:
    def __init__(self, base_path):
        self.base_path = base_path
        self.saved_files = []
        self.iteration = 1

    def save_to_file(self, file_name, content):
        file_path = f"{self.base_path}/{file_name}"
        self.saved_files.append((file_name, content))
        return file_path

    def get_extension(self, language):
        return {"python": "py", "cpp": "cpp", "java": "java"}.get(language.lower(), "txt")

    def get_next_iteration(self, subject):
        return len(self.saved_files) + 1

    @staticmethod
    def initialize_session_path(root_dir, language, subject, level, session_id):
        return f"{root_dir}/{language}/{level}_{subject}_{session_id}"


# Fixtures
@pytest.fixture
def mock_exercise_manager():
    return MockExerciseManager()


@pytest.fixture
def mock_file_handler_class(monkeypatch):
    """
    Monkeypatch the FileHandler class to replace it with MockFileHandler.
    """
    monkeypatch.setattr("core.exercise_generator.FileHandler", MockFileHandler)


# Tests
def test_validate_input():
    """
    Test input validation using Validator.
    """
    assert Validator.validate_input("Python", "language") == "Python"
    with pytest.raises(ValueError, match="Language cannot be empty."):
        Validator.validate_input("", "language")


def test_initialize_session_path(mock_exercise_manager, mock_file_handler_class):
    """
    Test the session-specific path initialization.
    """
    session_id = 1
    generator = ExerciseGenerator("python", "OOP", "advanced", session_id, mock_exercise_manager)
    expected_path = f"exercises/python/advanced_OOP_{session_id}"
    assert generator.file_handler.base_path == expected_path


def test_generate_and_save_exercise(mock_exercise_manager, mock_file_handler_class):
    """
    Test generating and saving a single exercise.
    """
    session_id = 1
    generator = ExerciseGenerator("python", "OOP", "advanced", session_id, mock_exercise_manager)

    # Generate and save an exercise
    file_path = generator.generate_and_save_exercise()

    # Check file properties
    assert file_path == f"exercises/python/advanced_OOP_{session_id}/OOP_1.py"
    assert len(generator.file_handler.saved_files) == 1
    assert generator.file_handler.saved_files[0][0] == "OOP_1.py"


def test_generate_and_save_multiple_exercises(mock_exercise_manager, mock_file_handler_class):
    """
    Test generating and saving multiple exercises in the same session.
    """
    session_id = 2
    generator = ExerciseGenerator("python", "OOP", "intermediate", session_id, mock_exercise_manager)

    # Generate and save multiple exercises
    generator.generate_and_save_exercise()
    generator.generate_and_save_exercise()
    generator.generate_and_save_exercise()

    # Verify iteration and files
    assert len(generator.file_handler.saved_files) == 3
    assert generator.file_handler.saved_files[2][0] == "OOP_3.py"


def test_generate_exercise_content(mock_exercise_manager):
    """
    Test content generation for an exercise.
    """
    session_id = 1
    generator = ExerciseGenerator("python", "OOP", "beginner", session_id, mock_exercise_manager)
    content = generator.exercise_manager.generate_exercise("OOP", "python", "beginner")
    expected_content = "# This is a beginner python exercise on OOP"
    assert content == expected_content


def test_construct_file_name(mock_exercise_manager, mock_file_handler_class):
    """
    Test the file naming logic for exercises.
    """
    session_id = 3
    generator = ExerciseGenerator("python", "data_structures", "advanced", session_id, mock_exercise_manager)
    generator.file_handler.saved_files = [("data_structures_1.py", "content")]
    file_name = generator.generate_and_save_exercise().split("/")[-1]
    assert file_name == "data_structures_2.py"
