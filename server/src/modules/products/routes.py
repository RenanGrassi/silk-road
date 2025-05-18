from src.abstracts.abstract_route import AbstractRoute


class ProductRoute(AbstractRoute):
    """
    Route class for managing products.
    """

    @property
    def group(self) -> str:
        """
        The path of the route.
        :return: The path of the route.
        """
        return "products"

    async def get(self):
        """
        Get all products.
        :return: A list of all products.
        """
        return await self.service.list()
