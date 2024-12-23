import pytest
from common.utils.validator import Validator


def test_validate_name_valid():
    # Valid names
    valid_names = ["subject_name", "level-1", "Python3"]
    for name in valid_names:
        try:
            Validator.validate_name(name, "field")
        except ValueError:
            pytest.fail(f"Validator.validate_name raised an exception for valid name: {name}")


def test_validate_name_invalid():
    # Invalid names
    invalid_names = ["", "invalid name!", "name@123", "name$", " "]
    for name in invalid_names:
        with pytest.raises(ValueError, match="Invalid field name"):
            Validator.validate_name(name, "field")


def test_validate_content_valid():
    # Valid contents
    valid_contents = ["Some content", "    Indented content", "Content\nWith\nLines"]
    for content in valid_contents:
        try:
            Validator.validate_content(content)
        except ValueError:
            pytest.fail(f"Validator.validate_content raised an exception for valid content: {content}")


def test_validate_content_invalid():
    # Invalid contents
    invalid_contents = ["", "   ", "\n\t"]
    for content in invalid_contents:
        with pytest.raises(ValueError, match="Content cannot be empty."):
            Validator.validate_content(content)


def test_validate_input_valid():
    # Valid inputs
    valid_inputs = ["Valid input", "Another_Valid-Input"]
    for input_value in valid_inputs:
        result = Validator.validate_input(input_value, "field_name")
        assert result == input_value.strip()


def test_validate_input_invalid():
    # Invalid inputs
    invalid_inputs = ["", "   ", "\n"]
    for input_value in invalid_inputs:
        with pytest.raises(ValueError, match="Field_name cannot be empty."):
            Validator.validate_input(input_value, "field_name")
