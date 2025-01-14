from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from config.constants import GENERAL_SUBJECTS, FILE_EXTENSIONS, SUPPORTED_LEVELS


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
        Prompt the user to set their preferences with validation and fuzzy matching.
        """
        self.console.print(
            Panel(
                "[blue bold]Please configure your preferences[/blue bold]",
                expand=False,
                style="bold cyan",
            )
        )

        # Prompt and validate language
        self._set_language()

        # Prompt and validate subject with fuzzy matching
        self._set_subject()

        # Prompt and validate level
        self._set_level()

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

    def _set_language(self):
        while True:
            self.language = Prompt.ask(
                "[bold green]Choose the programming language[/bold green]",
                choices=list(FILE_EXTENSIONS.keys()),
                default="python",
            )
            break  # No further validation needed since choices are predefined

    def _set_subject(self):
        while True:
            self.subject = Prompt.ask(
                "[bold green]Choose the subject[/bold green]",
                choices=GENERAL_SUBJECTS,
                default="OOP",
            )
            break

    def _set_level(self):
        while True:
            self.level = Prompt.ask(
                "[bold green]Choose the difficulty level[/bold green]",
                choices=SUPPORTED_LEVELS,
                default="beginner",
            )
            break
