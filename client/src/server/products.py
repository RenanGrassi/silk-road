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

    def list(self) -> dict:
        return self.service.list(**GlobalToken.get_token_kwargs())

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

    def get(self, config: ProductIdModel) -> dict:
        """Get a product by its ID.
        :param config: The configuration containing the product ID.
        :return: The product with the specified ID.
        """
        return self.service.get(config.product_id)

    def update(self, config: ProductModel) -> dict:
        """
        Update an existing product.
        :param config: The product configuration to update.
        :return: The updated product.
        """
        return self.service.update(
            config.model_dump(), **GlobalToken.get_token_kwargs()
        )

    def delete(self, config: ProductIdModel) -> dict:
        """
        Delete a product.
        :param config: The product ID to delete.
        :return: The deleted product.
        """
        return self.service.delete(config.product_id, **GlobalToken.get_token_kwargs())

    def get_by_shop(self) -> dict:
        """
        Get products by shop ID.
        :param user_id: The ID of the user whose shop's products are to be retrieved.
        :return: A list of products for the specified shop.
        """
        return self.service.get_by_shop(**GlobalToken.get_token_kwargs())
