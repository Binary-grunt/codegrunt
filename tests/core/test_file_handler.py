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
    # Create a new directory inside the temp directory
    test_dir = temp_directory / "test_subdir"
    assert not test_dir.exists()

    # Initialize FileHandler
    FileHandler(str(test_dir))

    # Verify directory was created
    assert test_dir.exists()
    assert test_dir.is_dir()


def test_save_to_file(temp_directory):
    # Initialize FileHandler
    handler = FileHandler(str(temp_directory))

    # Define file name and content
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
    # Initialize FileHandler
    handler = FileHandler(str(temp_directory))

    # Define file name and empty content
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
    # Initialize FileHandler
    handler = FileHandler(str(temp_directory))

    # Define multiple files and their contents
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
