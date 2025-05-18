from abc import ABC, abstractmethod


class AbstractRoute(ABC):
    """
    Abstract base class for routes.
    """

    @property
    @abstractmethod
    def group(self) -> str:
        """
        The path of the route.
        :return: The path of the route.
        """
        pass
