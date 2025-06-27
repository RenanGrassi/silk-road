from src.modules.transactions.services import TransactionService
from src.services.auth import AuthService
import Pyro5.api


@Pyro5.api.expose
class TransactionRoute:
    """
    Route class for managing products.
    """

    def __init__(self):
        """
        Initialize the ProductRoute class.
        """
        self.service = TransactionService()

    @AuthService.authenticate()
    def buy(self, product_id: int, auth: dict, **kwargs) -> dict:
        """
        Buy a product.
        :param config: The configuration for the product.
        :param auth: The authentication information.
        :return: The transaction details.
        """
        return self.service.buy(product_id, auth["id"])
