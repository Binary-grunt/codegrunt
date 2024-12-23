import pytest
from datetime import datetime
from unittest.mock import MagicMock
from core.exercise_generator import ExerciseGenerator
from common.utils.validator import Validator


class MockExerciseManager:
    def generate_exercise(self, subject, language, level):
        return f"# This is a {level} {language} exercise on {subject}"


class MockFileHandler:
    def __init__(self, base_path):
        self.base_path = base_path
        self.saved_files = []

    def save_to_file(self, file_name, content):
        file_path = f"{self.base_path}/{file_name}"
        self.saved_files.append((file_name, content))
        return file_path


@pytest.fixture
def mock_exercise_manager():
    return MockExerciseManager()


@pytest.fixture
def mock_file_handler_class(monkeypatch):
    monkeypatch.setattr("core.exercise_generator.FileHandler", MockFileHandler)


def test_validate_input():
    assert Validator.validate_input("Python", "language") == "Python"
    with pytest.raises(ValueError, match="Language cannot be empty."):
        Validator.validate_input("", "language")


def test_get_base_path(mock_exercise_manager):
    generator = ExerciseGenerator("python", "OOP", "advanced", mock_exercise_manager)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    expected_path = f"exercises/python/OOP_advanced_{timestamp}"
    assert generator.get_base_path() == expected_path


def test_generate_and_save_exercise(mock_exercise_manager, mock_file_handler_class):
    generator = ExerciseGenerator("python", "OOP", "advanced", mock_exercise_manager)

    # Generate and save an exercise
    file_path = generator.generate_and_save_exercise()
    base_path = generator.get_base_path()

    # Check if the file was saved correctly
    assert file_path == f"{base_path}/OOP_1.py"
    assert generator.iteration == 2  # Iteration should increment


def test_generate_and_save_exercise_multiple(mock_exercise_manager, mock_file_handler_class):
    generator = ExerciseGenerator("python", "OOP", "advanced", mock_exercise_manager)

    # Save multiple exercises
    generator.generate_and_save_exercise()
    generator.generate_and_save_exercise()
    generator.generate_and_save_exercise()

    base_path = generator.get_base_path()
    assert generator.iteration == 4  # Iteration should increment after each save


def test_generate_exercise_content(mock_exercise_manager):
    generator = ExerciseGenerator("python", "OOP", "advanced", mock_exercise_manager)
    content = generator._generate_exercise_content()
    expected_content = "# This is a advanced python exercise on OOP"
    assert content == expected_content


def test_construct_file_name(mock_exercise_manager):
    generator = ExerciseGenerator("python", "advanced_OOP", "advanced", mock_exercise_manager)
    generator.iteration = 5
    file_name = generator._construct_file_name()
    assert file_name == "OOP_5.py"
