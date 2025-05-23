from src.abstracts.abstract_route import AbstractRoute
from src.modules.products.service import ProductService


class ProductRoute(AbstractRoute):
    """
    Route class for managing products.
    """

    def __init__(self):
        """
        Initialize the ProductRoute class.
        """
        self.service = ProductService()

    @classmethod
    def group(cls) -> str:
        """
        The path of the route.
        :return: The path of the route.
        """
        return "products"

    def get(self, config: dict) -> dict:
        """
        Get all products.
        :return: A list of all products.
        """
        return self.service.list()
