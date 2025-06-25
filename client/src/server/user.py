from src.server.base_server import BaseServer


class UserServer(BaseServer):
    """
    User server class for managing user-related operations.
    """

    @property
    def service_ns(self) -> str:
        """
        The namespace of the user service.
        :return: The namespace of the user service.
        """
        return (
            "users"  # This should match the name used in the Pyro5 daemon registration.
        )

    def register(self, config: dict) -> dict:
        """
        Register a new user.
        :param config: The configuration for the user.
        :return: The created user.
        """
        return self.service.create(config)

    def login(self, config: dict) -> dict:
        """
        Login a user.
        :param config: The configuration for the login.
        :return: The result of the login.
        """
        return self.service.login(config)
