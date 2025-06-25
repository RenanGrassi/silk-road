from src.server.base_server import BaseServer
from src.singletons.token import GlobalToken
from src.server.models.products import ProductIdModel


class TransactionServer(BaseServer):
    """
    Product server class
    """

    @property
    def service_ns(self) -> str:
        """
        The namespace of the transaction service.
        :return: The namespace of the transaction service.
        """
        return "transactions"

    def buy(self, config: ProductIdModel) -> dict:
        """
        Buy a product.
        :param config: The configuration containing the product ID.
        :return: The transaction details.
        """
        return self.service.buy(config.product_id, **GlobalToken.get_token_kwargs())
