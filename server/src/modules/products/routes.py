from src.modules.products.service import ProductService
from src.services.auth import AuthService

import Pyro5.api


@Pyro5.api.expose
class ProductRoute:
    """
    Route class for managing products.
    """

    def __init__(self):
        """
        Initialize the ProductRoute class.
        """
        self.service = ProductService()

    def get(self, config: dict) -> dict:
        """
        Get all products.
        :return: A list of all products.
        """
        return self.service.list()
