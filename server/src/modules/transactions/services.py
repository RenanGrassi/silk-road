from src.abstracts.abstract_crud_service import AbstractCRUDService
from src.modules.transactions.model import TransactionModel
from src.services.database import provide_session
from src.modules.products.service import ProductService
from src.modules.shop.service import ShopService
from src.modules.users.service import UserService


class TransactionService(AbstractCRUDService):
    def __init__(self):
        """
        Initialize the TransactionService class.
        """
        self.product_service = ProductService()
        self.shop_service = ShopService()
        self.user_service = UserService()

    """
    Service class for managing transactions.
    """

    @property
    def model(self):
        return TransactionModel

    @provide_session()
    def buy(self, product_id: str, user_id: str, session) -> dict:
        user = self.user_service.get(user_id)
        if not user:
            return {
                "error": "User not found",
                "status": 404,
            }
        product = self.product_service.get(product_id)
        if not product:
            return {
                "error": "Product not found",
                "status": 404,
            }
        if not product.get("is_active"):
            return {
                "error": "Product is not active",
                "status": 400,
            }
        if user.get("balance") < product.get("price"):
            return {
                "error": "Insufficient balance",
                "status": 400,
            }
        shop = self.shop_service.get_by_id(product.get("shop_id"))
        if not shop:
            return {
                "error": "Shop not found",
                "status": 404,
            }
        transaction = self.model(
            buyer_id=shop.get("user_id"),
            quantity=1,
            product_id=product.get("id"),
            seller_id=user_id,
        )
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        user["balance"] -= product.get("price")
        self.user_service.update(user_id, user)
        buyer = self.user_service.get(shop.get("user_id"))
        buyer["balance"] += product.get("price")
        self.user_service.update(shop.get("user_id"), buyer)
        return {
            c.name: getattr(transaction, c.name) for c in transaction.__table__.columns
        }
