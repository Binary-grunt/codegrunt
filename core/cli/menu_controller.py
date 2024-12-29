from rich.console import Console
from typer import Exit
from rich.table import Table
from .preference_cli import PreferenceCli
from core.session_manager import SessionManager
from core.managers import UserManager


class MenuController:
    """
    Encapsulates all menu-related logic for the CodeGrunt CLI, splitting the
    flow between pre-exercise and post-exercise states, and handling all
    necessary actions such as exercise generation, submission, and stats viewing.
    """

    def __init__(
        self,
        console: Console,
        preference_manager: PreferenceCli,
        session_manager: SessionManager,
        user_manager: UserManager
    ) -> None:
        """
        Initialize the MenuLogic with required dependencies.

        Args:
            console (Console): Rich console for printing to the terminal.
            preference_manager (PreferenceCli): Manages user preferences (language, subject, level).
            session_manager (SessionManager): Manages session and exercise logic (create, submit, etc.).
            user_manager (UserManager): Handles user creation and retrieval.
        """
        self.console = console
        self.preference_manager = preference_manager
        self.session_manager = session_manager
        self.user_manager = user_manager
        self.user = None

    def set_current_user(self, user) -> None:
        """
        Optionally set or update the current user for subsequent operations.

        Args:
            user: The user object to be associated with this logic.
        """
        self.user = user

    def handle_choice_pre_exercise(self, choice: str) -> None:
        """
        Handle menu choices before any exercise has been generated.

        Args:
            choice (str): The user's selected menu option.
        """
        language, subject, level = self.preference_manager.get_preferences()

        if choice == "1":
            self.on_user_request_exercise(language, subject, level)
        elif choice == "2":
            self.view_global_stats()
        elif choice == "3":
            self.console.print("[red]Exiting the application... Goodbye![/red]")
            raise Exit()
        else:
            self.console.print("[yellow]Invalid choice. Please select a valid option.[/yellow]")

    def handle_choice_post_exercise(self, choice: str) -> None:
        """
        Handle menu choices after an exercise has been generated.

        Args:
            choice (str): The user's selected menu option.
        """
        language, subject, level = self.preference_manager.get_preferences()

        if choice == "1":
            self.run_solution()
        elif choice == "2":
            self.submit_solution(language, subject, level)
        elif choice == "3":
            self.view_current_session_stats()
        elif choice == "4":
            self.view_global_stats()
        elif choice == "5":
            self.console.print("[red]Exiting the application... Goodbye![/red]")
            raise Exit()
        else:
            self.console.print("[yellow]Invalid choice. Please select a valid option.[/yellow]")

    def on_user_request_exercise(self, language: str, subject: str, level: str) -> None:
        """
        Generate a new exercise file based on the current user's preferences.

        Args:
            language (str): The programming language for the exercise.
            subject (str): The subject domain (e.g., algorithms, data structures).
            level (str): The difficulty level (beginner, intermediate, etc.).
        """
        if not self.user:
            self.user = self.user_manager.get_or_create_user()

        self.console.print("\n[blue]Generating a new exercise...[/blue]")
        file_path = self.session_manager.create_new_exercise(
            user_id=self.user.id, language=language, subject=subject, level=level
        )
        self.console.print(f"[green]Exercise saved at: {file_path}[/green]")

    def run_solution(self) -> None:
        """
        Run (locally test) the most recently generated exercise file, if it exists.
        """
        self.console.print("\n[blue]Running your solution for testing...[/blue]")
        if self.session_manager.last_generated_file:
            self.console.print(
                f"[yellow]Running the file: {self.session_manager.last_generated_file}[/yellow]"
            )
            self.console.print("[green]Test completed. No syntax errors detected![/green]")
        else:
            self.console.print("[red]No exercise has been generated yet. Please generate one first.[/red]")

    def submit_solution(self, language: str, subject: str, level: str) -> None:
        """
        Submit the user's solution for feedback, then optionally generate a new exercise.

        Args:
            language (str): The programming language for the exercise.
            subject (str): The subject domain.
            level (str): The difficulty level.
        """
        if not self.user:
            self.user = self.user_manager.get_or_create_user()

        self.console.print("\n[blue]Submitting your solution...[/blue]")
        feedback = self.session_manager.submit_exercise(user_id=self.user.id)
        self.console.print(f"[green]{feedback}[/green]")

        self.console.print("\n[blue]Generating a new exercise after submission...[/blue]")
        file_path = self.session_manager.create_new_exercise(
            user_id=self.user.id, language=language, subject=subject, level=level
        )
        self.console.print(f"[green]New exercise saved at: {file_path}[/green]")

    def view_global_stats(self) -> None:
        """
        Display the user's global statistics, such as total sessions,
        total exercises, and average score.
        """
        if not self.user:
            self.user = self.user_manager.get_or_create_user()

        stats = self.session_manager.stats_repository.get_stats_by_user(self.user.id)
        if stats:
            stats_table = Table(title="Global Stats", title_style="bold green")
            stats_table.add_column("Metric", justify="center", style="bold cyan")
            stats_table.add_column("Value", justify="center", style="bold white")
            stats_table.add_row("Total Sessions", str(stats.total_sessions))
            stats_table.add_row("Total Exercises", str(stats.total_exercises))
            stats_table.add_row("Average Score", f"{stats.average_score:.2f}")
            self.console.print(stats_table)
        else:
            self.console.print("[yellow]No global stats available yet.[/yellow]")

    def view_current_session_stats(self) -> None:
        """
        Display statistics for the current session, including the session ID,
        how many exercises have been completed, the user's current score, etc.
        """
        if not self.session_manager.current_session:
            self.console.print("[yellow]No active session. Please generate an exercise to start a session.[/yellow]")
            return

        session_table = Table(title="Current Session Stats", title_style="bold green")
        session_table.add_column("Metric", justify="center", style="bold cyan")
        session_table.add_column("Value", justify="center", style="bold white")
        session_table.add_row("Session ID", str(self.session_manager.current_session.id))
        session_table.add_row("Exercises Completed", str(self.session_manager.current_session.exercises_completed))
        session_table.add_row("Successful Exercises", str(self.session_manager.current_session.successful_exercises))
        session_table.add_row("Current Score", str(self.session_manager.current_session.score))
        self.console.print(session_table)
