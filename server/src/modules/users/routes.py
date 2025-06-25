from src.modules.users.service import UserService
from src.services.auth import AuthService

import Pyro5.api


@Pyro5.api.expose
class UserRoute:
    """
    Route class for managing products.
    """

    def __init__(self):
        """
        Initialize the ProductRoute class.
        """
        self.service = UserService()

    def login(self, config: dict) -> dict:
        """
        Login a user.
        :param config: The configuration for the login.
        :return: The result of the login.
        """
        return self.service.login(config)

    def create(self, config: dict) -> dict:
        """
        Create a new user.
        :param config: The configuration for the user.
        :return: The created user.
        """
        password = AuthService.hash_password(config["password"])
        config["password"] = password
        user_created = self.service.create(config)
        print(user_created)
        return user_created

    @AuthService.authenticate()
    def get(self, config: dict, auth: dict) -> dict:
        """
        Get a user by ID.
        :param config: The configuration for the user.
        :return: The user with the given ID.
        """
        return self.service.read(auth["id"])

    def update(self, config: dict) -> dict:
        """
        Update a user by ID.
        :param config: The configuration for the user.
        :return: The updated user.
        """
        return self.service.update(config)

    def delete(self, config: dict) -> dict:
        """
        Delete a user by ID.
        :param config: The configuration for the user.
        :return: None
        """
        return self.service.delete(config)
