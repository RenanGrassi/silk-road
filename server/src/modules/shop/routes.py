from src.modules.shop.service import ShopService
from src.services.auth import AuthService
import Pyro5.api


@Pyro5.api.expose
class ShopRoute:
    """
    Route class for managing products.
    """

    def __init__(self):
        """
        Initialize the ProductRoute class.
        """
        self.service = ShopService()

    @AuthService.authenticate()
    def get(self, auth: dict, **kwargs) -> dict:
        """
        Get all products.
        :return: A list of all products.
        """
        return self.service.get(auth["id"])

    @AuthService.authenticate()
    def create(self, config: dict, auth: dict, **kwargs) -> dict:
        """
        Create a new product.
        :param config: The configuration for the product.
        :return: The created product.
        """
        return self.service.create(config, auth["id"])
