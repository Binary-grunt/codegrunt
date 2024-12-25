from rich import print


class UserManager:
    def __init__(self, session_manager):
        """
        Initialize the UserManager with a SessionManager instance.
        """
        self.session_manager = session_manager

    def get_or_create_user(self):
        """
        Retrieve the first user from the database or create a new one.

        Returns:
            User: The retrieved or newly created user.
        """
        user = self.session_manager.user_repository.get_first_user()
        if not user:
            print("[yellow]No user found in the database. Creating a new user...[/yellow]")
            user = self.session_manager.user_repository.add_user()
        else:
            print(f"[green]Existing user found with ID: {user.id}[/green]")
        return user
