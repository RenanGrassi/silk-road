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

    def list(self, like: str) -> dict:
        """
        Get all products.
        :return: A list of all products.
        """
        return self.service.list(like)

    @AuthService.authenticate()
    def create(self, config: dict, auth: dict, **kwargs) -> dict:
        """
        Create a new product.
        :param config: The configuration for the product.
        :return: The created product.
        """
        return self.service.create(config, auth["id"])

    @AuthService.authenticate()
    def update(self, config: dict, auth: dict, **kwargs) -> dict:
        """
        Update an existing product.
        :param config: The configuration for the product.
        :return: The updated product.
        """
        return self.service.update(config, auth["id"])

    @AuthService.authenticate()
    def delete(self, config: dict, auth: dict, **kwargs) -> dict:
        """
        Delete a product.
        :param config: The configuration for the product.
        :return: The deleted product.
        """
        return self.service.delete(config, auth["id"])

    def get(self, config: dict) -> dict:
        """
        Get a product by its ID.
        :param config: The configuration containing the product ID.
        :return: The product with the specified ID.
        """
        return self.service.get(config.get("product_id"))

    @AuthService.authenticate()
    def get_by_shop(self, auth: dict, **kwargs) -> dict:
        """
        Get all products for a specific shop.
        :param config: The configuration containing the shop ID.
        :param auth: The authentication information.
        :return: A list of products for the specified shop.
        """
        return self.service.get_by_shop(auth["id"])
