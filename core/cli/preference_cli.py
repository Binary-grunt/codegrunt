from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel


class PreferenceCli:
    def __init__(self):
        """
        Initialize the PreferenceManager.
        """
        self.language = None
        self.subject = None
        self.level = None
        self.console = Console()

    def set_preferences(self):
        """
        Prompt the user to set their preferences with a styled interface.
        """
        self.console.print(
            Panel(
                "[blue bold]Please configure your preferences[/blue bold]",
                expand=False,
                style="bold cyan",
            )
        )

        # Prompt user for preferences with validation
        self.language = Prompt.ask(
            "[bold green]Enter the programming language[/bold green] (e.g., python, cpp, java)"
        )
        self.subject = Prompt.ask(
            "[bold green]Enter the subject[/bold green] (e.g., OOP, data_structures)"
        )
        self.level = Prompt.ask(
            "[bold green]Enter the difficulty level[/bold green] (e.g., beginner/intermediate/advanced)",
            choices=["beginner", "intermediate", "advanced", "expert"],
            default="beginner",
        )

        # Display summary of preferences
        self.console.print(
            Panel(
                f"[cyan bold]Preferences set[/cyan bold]:\n\n"
                f"[yellow]Language[/yellow]: {self.language}\n"
                f"[yellow]Subject[/yellow]: {self.subject}\n"
                f"[yellow]Level[/yellow]: {self.level}",
                title="[bold green]Preferences Summary[/bold green]",
                title_align="center",
                expand=False,
                style="cyan",
            )
        )

    def get_preferences(self):
        """
        Return the current preferences.

        Returns:
            tuple: (language, subject, level)
        """
        if not self.language or not self.subject or not self.level:
            self.console.print(
                "[red]Preferences have not been set. Please configure them first.[/red]"
            )
            return None, None, None
        return self.language, self.subject, self.level
