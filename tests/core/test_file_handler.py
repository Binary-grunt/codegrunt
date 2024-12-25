import os
import pytest
from core.file_handler import FileHandler


@pytest.fixture
def temp_directory(tmp_path):
    """
    Provides a temporary directory for testing.
    """
    return tmp_path


def test_ensure_directory_exists(temp_directory):
    """
    Test that the directory is created if it doesn't exist.
    """
    test_dir = temp_directory / "test_subdir"
    assert not test_dir.exists()

    # Initialize FileHandler
    FileHandler(str(test_dir))

    # Verify the directory was created
    assert test_dir.exists()
    assert test_dir.is_dir()


def test_save_to_file(temp_directory):
    """
    Test saving content to a file.
    """
    handler = FileHandler(str(temp_directory))
    file_name = "test_file.txt"
    content = "This is a test content."

    # Save the file
    file_path = handler.save_to_file(file_name, content)

    # Verify file path and content
    assert os.path.exists(file_path)
    assert os.path.isfile(file_path)

    with open(file_path, "r", encoding="utf-8") as file:
        saved_content = file.read()
    assert saved_content == content


def test_save_to_file_with_empty_content(temp_directory):
    """
    Test saving an empty file.
    """
    handler = FileHandler(str(temp_directory))
    file_name = "empty_file.txt"
    content = ""

    # Save the file
    file_path = handler.save_to_file(file_name, content)

    # Verify file path and content
    assert os.path.exists(file_path)
    assert os.path.isfile(file_path)

    with open(file_path, "r", encoding="utf-8") as file:
        saved_content = file.read()
    assert saved_content == ""


def test_multiple_files_in_directory(temp_directory):
    """
    Test saving multiple files in the same directory.
    """
    handler = FileHandler(str(temp_directory))
    files = {
        "file1.txt": "Content of file 1",
        "file2.txt": "Content of file 2",
        "file3.txt": "Content of file 3",
    }

    # Save all files
    for file_name, content in files.items():
        handler.save_to_file(file_name, content)

    # Verify all files are created with correct content
    for file_name, content in files.items():
        file_path = os.path.join(temp_directory, file_name)
        assert os.path.exists(file_path)
        assert os.path.isfile(file_path)

        with open(file_path, "r", encoding="utf-8") as file:
            saved_content = file.read()
        assert saved_content == content


def test_get_extension():
    """
    Test retrieving file extensions for supported languages.
    """
    assert FileHandler.get_extension("python") == "py"
    assert FileHandler.get_extension("cpp") == "cpp"
    assert FileHandler.get_extension("java") == "java"
    assert FileHandler.get_extension("javascript") == "js"

    # Unsupported language
    with pytest.raises(ValueError, match="Unsupported language: unknown"):
        FileHandler.get_extension("unknown")


def test_initialize_session_path(temp_directory):
    """
    Test session-specific path initialization.
    """
    root_dir = str(temp_directory)
    language = "python"
    subject = "OOP"
    level = "beginner"
    session_id = 1

    session_path = FileHandler.initialize_session_path(
        root_dir, language, subject, level, session_id
    )
    expected_path = os.path.join(root_dir, language, f"{level}_{subject}_{session_id}")

    # Verify the session path
    assert session_path == expected_path
    assert os.path.exists(session_path)
    assert os.path.isdir(session_path)


def test_get_next_iteration(temp_directory):
    """
    Test determining the next file iteration in a directory.
    """
    handler = FileHandler(str(temp_directory))
    subject = "exercise"

    # Create some files to simulate iterations
    handler.save_to_file(f"{subject}_1.txt", "Content 1")
    handler.save_to_file(f"{subject}_2.txt", "Content 2")
    handler.save_to_file(f"{subject}_3.txt", "Content 3")

    # Verify the next iteration
    next_iteration = handler.get_next_iteration(subject)
    assert next_iteration == 4

    # Test when no files exist
    handler_empty = FileHandler(str(temp_directory / "empty_dir"))
    assert handler_empty.get_next_iteration(subject) == 1
