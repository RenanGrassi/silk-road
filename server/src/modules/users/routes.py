from src.abstracts.abstract_route import AbstractRoute
from src.modules.users.service import UserService


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
