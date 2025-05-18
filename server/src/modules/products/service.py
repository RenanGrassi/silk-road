from src.abstracts.abstract_crud_service import AbstractCRUDService
from src.modules.products.model import ProductModel


class ProductService(AbstractCRUDService):
    """
    Service class for managing products.
    """

    @property
    def model(self):
        return ProductModel
