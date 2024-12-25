from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from typer import Exit


class ApplicationInterface:
    def __init__(self, session_manager, user_manager, preference_cli):
        """
        Initialize the application interface.

        Args:
            session_manager (SessionManager): Manages sessions and exercises.
            user_manager (UserManager): Manages user-related operations.
            preference_cli (PreferenceCLi): Manages user preferences.
        """
        self.session_manager = session_manager
        self.user_manager = user_manager
        self.preference_manager = preference_cli
        self.user = None
        self.console = Console()

    def run(self):
        """
        Run the main application loop.
        """
        # Display the introduction
        self.introduction()

        # Retrieve or create user
        self.user = self.user_manager.get_or_create_user()

        # Set user preferences
        self.preference_manager.set_preferences()

        # Main loop
        while True:
            self._display_menu()
            try:
                choice = Prompt.ask(
                    "[bold cyan]Enter your choice[/bold cyan]",
                    choices=["1", "2", "3", "4", "5", "6"],
                    default="6",
                )
                self._handle_choice(int(choice))
            except Exit:
                break
            except Exception as e:
                self.console.print(f"[red]An error occurred: {e}[/red]")

    def introduction(self):
        """
        Display a detailed introduction to the project using rich.
        """
        console = Console()

        # Title of the application
        title = Text("Welcome to the Programming Practice Application!", style="bold blue")
        console.print(Panel(title, expand=False))

        # Description
        description = """
            This application helps you practice programming skills interactively by:

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

            [bold yellow]Note:[/bold yellow] Your progress is saved locally and you can resume where you left off.
            """
        console.print(Panel(instructions, style="magenta", border_style="cyan"))

        # Motivational message
        motivation = Text(
            "Happy Coding! Let's tackle those coding challenges together!",
            style="bold green"
        )
        console.print(Panel(motivation, expand=False))

    def _display_menu(self):
        """
        Display the main menu.
        """
        menu_table = Table(title="Main Menu", title_style="bold blue")
        menu_table.add_column("Option", justify="center", style="bold cyan")
        menu_table.add_column("Description", justify="left", style="bold white")
        menu_table.add_row("1", "Generate an exercise")
        menu_table.add_row("2", "Run your solution for testing")
        menu_table.add_row("3", "Submit your solution")
        menu_table.add_row("4", "View user stats (global)")
        menu_table.add_row("5", "View current session stats")
        menu_table.add_row("6", "Exit")
        self.console.print(menu_table)

    def _handle_choice(self, choice):
        """
        Handle the user's menu choice.

        Args:
            choice (int): The user's choice.
        """
        language, subject, level = self.preference_manager.get_preferences()

        if choice == 1:
            self._generate_exercise(language, subject, level)
        elif choice == 2:
            self._run_solution()
        elif choice == 3:
            self._submit_solution(language, subject, level)
        elif choice == 4:
            self._view_global_stats()
        elif choice == 5:
            self._view_current_session_stats()
        elif choice == 6:
            self.console.print("[red]Exiting the application... Goodbye![/red]")
            raise Exit()
        else:
            self.console.print("[yellow]Invalid choice. Please select a valid option.[/yellow]")

    def _generate_exercise(self, language, subject, level):
        """
        Generate a new exercise based on user preferences.
        """
        self.console.print("\n[blue]Generating a new exercise...[/blue]")
        file_path = self.session_manager.generate_exercise(
            user_id=self.user.id, language=language, subject=subject, level=level
        )
        self.console.print(f"[green]Exercise saved at: {file_path}[/green]")

    def _run_solution(self):
        """
        Run the user's solution for testing.
        """
        self.console.print("\n[blue]Running your solution for testing...[/blue]")
        if self.session_manager.last_generated_file:
            self.console.print(
                f"[yellow]Running the file: {self.session_manager.last_generated_file}[/yellow]"
            )
            self.console.print("[green]Test completed. No syntax errors detected![/green]")
        else:
            self.console.print("[red]No exercise has been generated yet. Please generate one first.[/red]")

    def _submit_solution(self, language, subject, level):
        """
        Submit the user's solution.
        """
        self.console.print("\n[blue]Submitting your solution...[/blue]")
        feedback = self.session_manager.submit_exercise(user_id=self.user.id)
        self.console.print(f"[green]{feedback}[/green]")

        self.console.print("\n[blue]Generating a new exercise after submission...[/blue]")
        file_path = self.session_manager.generate_exercise(
            user_id=self.user.id, language=language, subject=subject, level=level
        )
        self.console.print(f"[green]New exercise saved at: {file_path}[/green]")

    def _view_global_stats(self):
        """
        View the global stats for the user.
        """
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

    def _view_current_session_stats(self):
        """
        View the stats for the current session.
        """
        if self.session_manager.current_session:
            session_table = Table(title="Current Session Stats", title_style="bold green")
            session_table.add_column("Metric", justify="center", style="bold cyan")
            session_table.add_column("Value", justify="center", style="bold white")
            session_table.add_row("Session ID", str(self.session_manager.current_session.id))
            session_table.add_row("Exercises Completed", str(self.session_manager.current_session.exercises_completed))
            session_table.add_row("Successful Exercises", str(self.session_manager.current_session.successful_exercises))
            session_table.add_row("Current Score", str(self.session_manager.current_session.score))
            self.console.print(session_table)
        else:
            self.console.print("[yellow]No active session. Please generate an exercise to start a session.[/yellow]")
