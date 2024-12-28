from rich.console import Console
from rich.prompt import Prompt
from typer import Exit
from core.cli import Introduction, MenuLogic, MenuRenderer, PreferenceCli
from core.session_manager import SessionManager
from core.managers import UserManager


class CliController:
    """
    Orchestrates the main command-line interface flow for CodeGrunt,
    handling user input, menu rendering, and dispatching to the appropriate logic.
    """

    def __init__(
        self,
        session_manager: SessionManager,
        user_manager: UserManager,
        preference_manager: PreferenceCli
    ) -> None:
        """
        Initialize the CLI controller with the required managers and preferences.

        Args:
            session_manager (SessionManager): Manages sessions, exercises, and related logic.
            user_manager (UserManager): Handles user creation and retrieval.
            preference_manager (PreferenceCli): Manages user preferences (language, subject, level).
        """
        self.console = Console()
        self.session_manager = session_manager
        self.user_manager = user_manager
        self.preference_manager = preference_manager
        self.user = None

        # Initialize MenuLogic with all needed dependencies
        self.menu_logic = MenuLogic(
            console=self.console,
            preference_manager=self.preference_manager,
            session_manager=self.session_manager,
            user_manager=self.user_manager
        )

    def run(self) -> None:
        """
        Launch the main application loop, displaying menus and handling user choices.
        """
        # 1. Display the introduction text
        Introduction.display()

        # 2. Retrieve or create the current user
        self.user = self.user_manager.get_or_create_user()
        self.menu_logic.set_current_user(self.user)

        # 3. Prompt user for initial preferences (language, subject, level)
        self.preference_manager.set_preferences()

        # 4. Main loop: display menu, prompt user, handle choice
        while True:
            # Check if an exercise has already been generated
            exercise_generated = bool(self.session_manager.last_generated_file)

            # Render the menu based on whether an exercise exists or not
            MenuRenderer.display_menu(exercise_generated)

            # Define the valid choices and default choice accordingly
            if not exercise_generated:
                valid_choices = ["1", "2", "3"]
                default_choice = "3"
            else:
                valid_choices = ["1", "2", "3", "4", "5"]
                default_choice = "5"

            try:
                # Prompt the user for a choice
                choice = Prompt.ask(
                    "[bold cyan]Enter your choice[/bold cyan]",
                    choices=valid_choices,
                    default=default_choice,
                )
                # Delegate choice handling
                self._handle_choice(choice, exercise_generated)
            except Exit:
                # Graceful exit from the application
                break
            except Exception as e:
                # Catch and display any unexpected error
                self.console.print(f"[red]An error occurred: {e}[/red]")

    def _handle_choice(self, choice: str, exercise_generated: bool) -> None:
        """
        Dispatch the user's choice to the appropriate menu logic method.

        Args:
            choice (str): The choice selected by the user in the menu.
            exercise_generated (bool): Indicates whether an exercise has already been generated.
        """
        # Ensure MenuLogic knows the current user (in case it changed or was just set)
        self.menu_logic.set_current_user(self.user)

        if not exercise_generated:
            self.menu_logic.handle_choice_pre_exercise(choice)
        else:
            self.menu_logic.handle_choice_post_exercise(choice)
