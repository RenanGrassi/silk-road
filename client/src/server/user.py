from src.server.base_server import BaseServer
from src.server.models.user import LoginModel, RegisterModel
from src.singletons.token import GlobalToken


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

    def register(self, config: LoginModel) -> dict:
        """
        Register a new user.
        :param config: The configuration for the user.
        :return: The created user.
        """
        return self.service.create(config.model_dump())

    def login(self, config: RegisterModel) -> dict:
        """
        Login a user.
        :param config: The configuration for the login.
        :return: The result of the login.
        """
        return self.service.login(config.model_dump())

    def get(self) -> dict:
        """
        Get a user by ID.
        :param auth: The authentication information containing the user ID.
        :return: The user with the given ID.
        """
        return self.service.get(**{"token": GlobalToken.get_token()})
