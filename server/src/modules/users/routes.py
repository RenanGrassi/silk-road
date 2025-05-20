from src.abstracts.abstract_route import AbstractRoute
from src.modules.users.service import UserService
from src.services.auth import AuthService


class ProductRoute(AbstractRoute):
    """
    Route class for managing products.
    """

    def __init__(self):
        """
        Initialize the ProductRoute class.
        """
        self.service = UserService()

    @classmethod
    def group(cls) -> str:
        """
        The path of the route.
        :return: The path of the route.
        """
        return "users"

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
        return self.service.create(config)

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
