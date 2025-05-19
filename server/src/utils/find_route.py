from src.abstracts.base_request import BaseDTO
import os
from src.abstracts.abstract_route import AbstractRoute
import importlib
import inspect


class RouteRequests:
    """
    Class to find the route for a given request.
    """

    def __init__(self):
        """
        Initialize the RouteRequests class.
        """

        self.routes: list[AbstractRoute] = self.find_route_classes()
        print(f"Routes: {self.routes}")

    def find_route_classes(self, path: str | None = None):
        """
        Find recursively the route in modules/*/*/routes.py.
        """
        # Iterate through all routes
        base_dir = (
            os.path.join(os.path.dirname(__file__), "..", "modules")
            if path is None
            else path
        )
        classes = []
        for module_dir in os.listdir(base_dir):
            module_path = os.path.join(base_dir, module_dir)
            print(f"Module path: {module_path}")
            if module_path.endswith("routes.py") and os.path.isfile(module_path):
                # Dynamically import the routes.py file
                spec = importlib.util.spec_from_file_location("routes", module_path)
                routes_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(routes_module)
                inspect_classes = inspect.getmembers(routes_module, inspect.isclass)
                route_classes = [
                    cls
                    for name, cls in inspect_classes
                    if issubclass(cls, AbstractRoute) and cls is not AbstractRoute
                ]
                classes.extend(route_classes)
            elif os.path.isdir(module_path):
                classes.extend(self.find_route_classes(module_path))
        return classes

    def find_route(self, dto: BaseDTO):
        """
        Find the route for the given request.
        """
        # Get the request method and path
        groups = [cls.group() for cls in self.routes]
        print(f"Grupos: {groups}")
        class_group = next(
            (cls for cls in self.routes if cls.group() == dto.group), None
        )
        if class_group is None:
            print(f"Grupo {dto.group} não encontrado.")
            return None
        instance = class_group()
        method = getattr(instance, dto.method, None)
        if method is None:
            print(f"Método {dto.method} não encontrado.")
            return None
        # Call the method and return the result
        return method(dto.conf)
