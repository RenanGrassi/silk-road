import Pyro5.api
from src.modules.products.routes import ProductRoute
from src.modules.users.routes import UserRoute
from src.modules.shop.routes import ShopRoute
from src.modules.transactions.routes import TransactionRoute


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
    uri_shop = daemon.register(ShopRoute, "shop")
    ns.register("shop", str(uri_shop).replace("0.0.0.0", "silk-road-server"))
    print(f"ShopRoute URI: {uri_shop}")
    uri_transactions = daemon.register(TransactionRoute, "transactions")
    ns.register(
        "transactions", str(uri_transactions).replace("0.0.0.0", "silk-road-server")
    )
    print(f"TransactionRoute URI: {uri_transactions}")
    daemon.requestLoop()
