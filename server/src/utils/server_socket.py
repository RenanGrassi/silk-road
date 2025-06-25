import Pyro5.api
from src.modules.products.routes import ProductRoute
from src.modules.users.routes import UserRoute


def register_daemon():
    """
    Register the Pyro5 daemon and expose the ProductRoute.
    """
    ns = Pyro5.api.locate_ns()
    daemon = Pyro5.api.Daemon(host="0.0.0.0")
    uri_products = daemon.register(ProductRoute, "products")
    ns.register("products", str(uri_products).replace("0.0.0.0", "silk-road-server"))
    print(f"ProductRoute URI: {uri_products}")
    uri_users = daemon.register(UserRoute, "users")
    ns.register("users", str(uri_users).replace("0.0.0.0", "silk-road-server"))
    print(f"UserRoute URI: {uri_users}")
    daemon.requestLoop()
