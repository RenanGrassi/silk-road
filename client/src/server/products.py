from src.server.base_server import BaseServer
from src.singletons.token import GlobalToken
from src.server.models.products import ProductModel, ProductIdModel


class ProductServer(BaseServer):
    """
    Product server class
    """

    @property
    def service_ns(self) -> str:
        """
        The namespace of the products service.
        :return: The namespace of the products service.
        """
        return "products"  # This should match the name used in the Pyro5 daemon registration.

    def list(self, like: str | None = None) -> dict:
        return self.service.get(like=like)

    def create(self, config: ProductModel) -> dict:
        """
        Create a new product.
        :param config: The product configuration to create.
        :return: The created product.
        """
        return self.service.create(
            config.model_dump(), **GlobalToken.get_token_kwargs()
        )

    def activate_announcement(self, config: ProductIdModel) -> dict:
        """
        Activate a product announcement.
        :param config: The product ID to activate.
        :return: The activated product.
        """
        return self.service.activate_announcement(
            config.product_id, **GlobalToken.get_token_kwargs()
        )

    def deactivate_announcement(self, config: ProductIdModel) -> dict:
        """
        Deactivate a product announcement.
        :param config: The product ID to deactivate.
        :return: The deactivated product.
        """
        return self.service.deactivate_announcement(
            config.product_id, **GlobalToken.get_token_kwargs()
        )
