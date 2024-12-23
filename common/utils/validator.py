import re


class Validator:
    """
    Utility class for validating names and parameters.
    """

    @staticmethod
    def validate_name(name: str, field: str) -> None:
        """
        Validates a name for fields like subject, level, or language.

        Args:
            name (str): The name to validate.
            field (str): The name of the field being validated.

        Raises:
            ValueError: If the name is invalid.
        """
        if not re.match(r"^[a-zA-Z0-9_\-]+$", name):
            raise ValueError(f"Invalid {field} name: {name}")

    @staticmethod
    def validate_content(content: str) -> None:
        """
        Validates that content is not empty.

        Args:
            content (str): The content to validate.

        Raises:
            ValueError: If the content is empty.
        """
        if not content.strip():
            raise ValueError("Content cannot be empty.")

    @staticmethod
    def validate_input(value: str, field_name: str) -> str:
        """
        Validates that the input value is not empty and returns it.

        Args:
            value (str): The input value to validate.
            field_name (str): Name of the field being validated.

        Returns:
            str: The validated value.

        Raises:
            ValueError: If the value is empty or invalid.
        """
        if not value or not value.strip():
            raise ValueError(f"{field_name.capitalize()} cannot be empty.")
        return value.strip()
