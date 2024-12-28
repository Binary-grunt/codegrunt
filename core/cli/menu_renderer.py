from rich.console import Console
from rich.table import Table


class MenuRenderer:
    """
    Responsible for rendering the CLI menu based on whether an exercise
    has already been generated or not.
    """

    @staticmethod
    def display_menu(exercise_generated: bool) -> None:
        """
        Display the main menu options in a Rich table.

        Args:
            exercise_generated (bool):
                Indicates whether an exercise has already been generated.
                - If False, the menu will show options to generate an exercise,
                  view global stats, or exit.
                - If True, the menu includes options to run or submit the solution,
                  view session or global stats, or exit.
        """
        console = Console()

        # Create a table with a title and two columns: Option and Description
        menu_table = Table(title="Main Menu", title_style="bold blue")
        menu_table.add_column("Option", justify="center", style="bold cyan")
        menu_table.add_column("Description", justify="left", style="bold white")

        # Render a different set of options depending on the exercise state
        if not exercise_generated:
            menu_table.add_row("1", "Generate an exercise")
            menu_table.add_row("2", "View user stats (global)")
            menu_table.add_row("3", "Exit")
        else:
            menu_table.add_row("1", "Run your solution")
            menu_table.add_row("2", "Submit your solution")
            menu_table.add_row("3", "View current session stats")
            menu_table.add_row("4", "View user stats (global)")
            menu_table.add_row("5", "Exit")

        # Print the table to the console
        console.print(menu_table)
