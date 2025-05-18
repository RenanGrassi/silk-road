from src.abstracts.base_request import BaseDTO
import os
from src.abstracts.abstract_route import AbstractRoute


class RouteRequests:
    """
    Class to find the route for a given request.
    """

    def __init__(self):
        """
        Initialize the RouteRequests class.
        """
        import importlib.util

        self.routes = []

        # Get the base directory for modules
        base_dir = os.path.join(os.path.dirname(__file__), "..", "modules")

        # Iterate through all subdirectories in modules/*/*
        for module_dir in os.listdir(base_dir):
            module_path = os.path.join(base_dir, module_dir)
            print(module_path)
            if os.path.isdir(module_path):
                for sub_dir in os.listdir(module_path):
                    sub_path = os.path.join(module_path, sub_dir)
                    if os.path.isdir(sub_path):
                        # Look for a file named "routes.py"
                        routes_file = os.path.join(sub_path, "routes.py")
                        if os.path.isfile(routes_file):
                            # Dynamically import the routes.py file
                            spec = importlib.util.spec_from_file_location(
                                "routes", routes_file
                            )
                            routes_module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(routes_module)

                            # Find the first class inheriting from AbstractRoute
                            for attr_name in dir(routes_module):
                                attr = getattr(routes_module, attr_name)
                                if (
                                    isinstance(attr, type)
                                    and issubclass(attr, AbstractRoute)
                                    and attr is not AbstractRoute
                                ):
                                    self.routes.append(attr())

    def find_route(self, dto: BaseDTO):
        """
        Find the route for the given request.
        """
        # Get the request method and path
        method = self.request.method.lower()
        path = self.request.path

        # Iterate through all routes
        for route in dto.routes:
            # Check if the route matches the request method and path
            if route.method == method and route.path == path:
                return route

        # If no matching route is found, return None
        return None
