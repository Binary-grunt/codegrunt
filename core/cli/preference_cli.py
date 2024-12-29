import difflib
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from config.constants import SUPPORTED_SUBJECTS, FILE_EXTENSIONS, SUPPORTED_LEVELS


class PreferenceCli:
    def __init__(self):
        """
        Initialize the PreferenceManager.
        """
        self.language = None
        self.subject = None
        self.level = None
        self.console = Console()

    def correct_subject(self, user_input: str) -> str:
        """
        Correct the subject based on fuzzy matching with `difflib`.

        Args:
            user_input (str): The user's input for the subject.

        Returns:
            str: The closest matching subject, or None if no match is found.
        """
        suggestions = difflib.get_close_matches(user_input, SUPPORTED_SUBJECTS, n=1, cutoff=0.5)
        if suggestions:
            corrected_subject = suggestions[0]
            self.console.print(f"[yellow]Did you mean: {corrected_subject}?[/yellow]")
            confirmation = Prompt.ask(
                "[bold green]Confirm subject?[/bold green] (yes/no)",
                choices=["yes", "no"],
                default="yes"
            )
            if confirmation == "yes":
                return corrected_subject
        else:
            self.console.print(f"[red]No matching subject found for '{user_input}'[/red]")
        return None

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
        while True:
            self.language = Prompt.ask(
                "[bold green]Enter the programming language[/bold green] (e.g., python, cpp, java)"
            )
            if self.language.lower() in FILE_EXTENSIONS:
                break
            self.console.print(f"[red]Invalid language. Supported: {', '.join(FILE_EXTENSIONS.keys())}[/red]")

        # Prompt and validate subject with fuzzy matching
        while True:
            raw_subject = Prompt.ask(
                "[bold green]Enter the subject[/bold green] (e.g., OOP, data_structures)"
            )
            self.subject = self.correct_subject(raw_subject)
            if self.subject:  # If a valid correction is found
                break

        # Prompt and validate level
        while True:
            self.level = Prompt.ask(
                "[bold green]Enter the difficulty level[/bold green]",
                choices=SUPPORTED_LEVELS,
                default="beginner"
            )
            if self.level in SUPPORTED_LEVELS:
                break
            self.console.print(f"[red]Invalid level. Supported: {', '.join(SUPPORTED_LEVELS)}[/red]")

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
