from src.server.base_server import BaseServer
from src.server.models.shop import ShopModel
from src.singletons.token import GlobalToken


class ShopServer(BaseServer):
    """
    Shop server class for managing user-related operations.
    """

    @property
    def service_ns(self) -> str:
        """
        The namespace of the user service.
        :return: The namespace of the shop service.
        """
        return (
            "shop"  # This should match the name used in the Pyro5 daemon registration.
        )

    def get(self) -> dict:
        """
        Get a shop by User ID.
        :param auth: The authentication information containing the user ID.
        :return: The user with the given ID.
        """
        return self.service.get(**{"token": GlobalToken.get_token()})

    def create(self, config: ShopModel) -> dict:
        """
        Create a new shop.
        :param config: The configuration for the shop.
        :return: The created shop.
        """
        return self.service.create(config.model_dump())
