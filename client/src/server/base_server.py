from abc import ABC, abstractmethod
import Pyro5.api


class BaseServer(ABC):
    def __init__(self):
        ns = Pyro5.api.locate_ns()
        uri = ns.lookup(self.service_ns)
        self.service = Pyro5.api.Proxy(uri)

    @property
    @abstractmethod
    def service_ns(self) -> str:
        """
        The namespace of the service.
        :return: The namespace of the service.
        """
        pass
