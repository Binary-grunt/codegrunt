from rich.console import Console
from rich.panel import Panel
from rich.text import Text


class Introduction:
    """
    Provides a textual introduction to the CodeGrunt CLI application,
    including instructions and usage details for new users.
    """

    @staticmethod
    def display() -> None:
        """
        Display the introduction panels
        """
        console = Console()

        # Title of the application
        title = Text("Welcome to the Codegrunt", style="bold blue")
        console.print(Panel(title, expand=False))

        # Description of the program
        description = """
            This program helps you practice programming skills interactively by:

            - Generating coding exercises based on your preferences.
            - Allowing you to test and submit your solutions.
            - Keeping track of your progress and stats.

            Here's how it works:
            1. Choose your language, subject, and difficulty level.
            2. Generate exercises tailored to your preferences.
            3. Test your solutions locally and submit them for analysis.
            4. View detailed statistics for your progress and session scores.

            [bold green]Improve your skills one exercise at a time![/bold green]
            """
        console.print(Panel(description, style="cyan", border_style="blue"))

        # Instructions for using the menu
        instructions = """
            Menu Options:
            [bold cyan]1.[/bold cyan] Generate an exercise: Create a new coding challenge.
            [bold cyan]2.[/bold cyan] Run your solution: Test the exercise locally.
            [bold cyan]3.[/bold cyan] Submit your solution: Submit and get feedback.
            [bold cyan]4.[/bold cyan] View user stats (global): Check your overall progress.
            [bold cyan]5.[/bold cyan] View current session stats: See stats for the current session.
            [bold cyan]6.[/bold cyan] Exit: Quit the application.

            [bold yellow]Note:[/bold yellow] Your progress is saved locally and
            you can resume where you left off.
            """
        console.print(Panel(instructions, style="magenta", border_style="cyan"))

        # Motivational message
        motivation = Text(
            "Happy Coding! Let's tackle those coding challenges together!",
            style="bold green"
        )
        console.print(Panel(motivation, expand=False))
