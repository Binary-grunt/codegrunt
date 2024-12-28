import pytest
from unittest.mock import patch
from rich.table import Table
from core.cli.menu_renderer import MenuRenderer


@pytest.fixture
def mock_console():
    """
    Fixture to mock the Rich Console.
    """
    with patch("core.cli.menu_renderer.Console") as MockConsole:
        yield MockConsole.return_value


def extract_table_rows(table):
    """
    Helper function to extract plain text rows from a Rich Table.
    """
    # Extract text data from columns in the table
    rows = []
    for row_index in range(len(table.columns[0]._cells)):  # Access the first column's cell count
        row = [col._cells[row_index] for col in table.columns]
        rows.append(row)
    return rows


def test_display_menu_exercise_not_generated(mock_console):
    """
    Test display_menu when no exercise has been generated.
    """
    # Call the method
    MenuRenderer.display_menu(exercise_generated=False)

    # Verify that a table was printed
    mock_console.print.assert_called_once()

    # Capture the Table object passed to the print method
    printed_table = mock_console.print.call_args[0][0]
    assert isinstance(printed_table, Table)

    # Verify the table's content
    expected_rows = [
        ["1", "Generate an exercise"],
        ["2", "View user stats (global)"],
        ["3", "Exit"],
    ]
    actual_rows = extract_table_rows(printed_table)
    assert actual_rows == expected_rows


def test_display_menu_exercise_generated(mock_console):
    """
    Test display_menu when an exercise has already been generated.
    """
    # Call the method
    MenuRenderer.display_menu(exercise_generated=True)

    # Verify that a table was printed
    mock_console.print.assert_called_once()

    # Capture the Table object passed to the print method
    printed_table = mock_console.print.call_args[0][0]
    assert isinstance(printed_table, Table)

    # Verify the table's content
    expected_rows = [
        ["1", "Run your solution"],
        ["2", "Submit your solution"],
        ["3", "View current session stats"],
        ["4", "View user stats (global)"],
        ["5", "Exit"],
    ]
    actual_rows = extract_table_rows(printed_table)
    assert actual_rows == expected_rows
