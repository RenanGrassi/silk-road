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

    @AuthService.authenticate()
    def activate_announcement(self, config: dict, auth: dict, **kwargs) -> dict:
        """
        Activate a product announcement.
        :param config: The configuration for the product.
        :param auth: The authentication information.
        :return: The activated product.
        """
        return self.service.activate_announcement(config.get("product_id"), auth["id"])

    @AuthService.authenticate()
    def deactivate_announcement(self, config: dict, auth: dict, **kwargs) -> dict:
        """Deactivate a product announcement.
        :param config: The configuration for the product.
        :param auth: The authentication information.
        :return: The deactivated product.
        """
        return self.service.deactivate_announcement(config, auth["id"])

    def list(self, config: dict) -> dict:
        """
        Get all products.
        :return: A list of all products.
        """
        return self.service.list(config)

    def create(self, config: dict) -> dict:
        """
        Create a new product.
        :param config: The configuration for the product.
        :return: The created product.
        """
        return self.service.create(config)
