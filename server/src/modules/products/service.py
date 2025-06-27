from src.abstracts.abstract_crud_service import AbstractCRUDService
from src.modules.products.model import ProductModel
from src.services.database import provide_session
from src.modules.shop.service import ShopService
from sqlalchemy.orm import joinedload


class ProductService(AbstractCRUDService):
    def __init__(self):
        """
        Initialize the ProductService class.
        """
        self.shop_service = ShopService()

    """
    Service class for managing products.
    """

    @property
    def model(self):
        return ProductModel

    @provide_session()
    def create(self, config: dict, user_id: str, session) -> dict:
        shop = self.shop_service.get(user_id)
        if not shop:
            return {
                "error": "Shop not found",
                "status": 404,
            }
        config["shop_id"] = shop.get("id")
        product = self.model(**config)
        session.add(product)
        session.commit()
        session.refresh(product)
        return {c.name: getattr(product, c.name) for c in product.__table__.columns}

    @provide_session()
    def activate_announcement(self, product_id: str, user_id: str, session) -> dict:
        """
        Activate a product announcement.
        :param product_id: The ID of the product to activate.
        :param user_id: The ID of the user activating the product.
        :return: The activated product.
        """
        product = (
            session.query(self.model)
            .filter(self.model.id == product_id, self.model.shop.has(user_id=user_id))
            .first()
        )
        if not product:
            return {
                "error": "Product not found or you do not have permission to activate it",
                "status": 404,
            }
        product.is_active = True
        session.commit()
        session.refresh(product)
        return {c.name: getattr(product, c.name) for c in product.__table__.columns}

    @provide_session()
    def deactivate_announcement(self, product_id: str, user_id: str, session) -> dict:
        """
        Deactivate a product announcement.
        :param product_id: The ID of the product to deactivate.
        :param user_id: The ID of the user deactivating the product.
        :return: The deactivated product.
        """
        product = (
            session.query(self.model)
            .filter(self.model.id == product_id, self.model.shop.has(user_id=user_id))
            .first()
        )
        if not product:
            return {
                "error": "Product not found or you do not have permission to deactivate it",
                "status": 404,
            }
        product.is_active = False
        session.commit()
        session.refresh(product)
        return {c.name: getattr(product, c.name) for c in product.__table__.columns}

    @provide_session()
    def list(self, like: str, session) -> dict:
        """
        Get all products.
        :return: A list of all products.
        """
        if like:
            products = (
                session.query(self.model)
                .filter(self.model.name.ilike(f"%{like}%"))
                .filter(self.model.is_active is True)
                .options(joinedload(self.model.shop))
                .all()
            )
            return [
                {c.name: getattr(product, c.name) for c in product.__table__.columns}
                for product in products
            ]
        products = (
            session.query(self.model)
            .options(joinedload(self.model.shop))
            .filter(self.model.is_active is True)
            .all()
        )
        print(
            [
                {c.name: getattr(product, c.name) for c in product.__table__.columns}
                | {
                    "shop": (
                        {
                            c.name: getattr(product.shop, c.name)
                            for c in product.shop.__table__.columns
                        }
                        if product.shop
                        else None
                    )
                }
                for product in products
            ]
        )
        return [
            {c.name: getattr(product, c.name) for c in product.__table__.columns}
            | {
                "shop": (
                    {
                        c.name: getattr(product.shop, c.name)
                        for c in product.shop.__table__.columns
                    }
                    if product.shop
                    else None
                )
            }
            for product in products
        ]

    @provide_session()
    def get(self, product_id: str, session) -> dict:
        """
        Get a product by its ID.
        :param product_id: The ID of the product to retrieve.
        :return: The product if found, otherwise an error message.
        """
        product = session.query(self.model).filter(self.model.id == product_id).first()
        if not product:
            return {"error": "Product not found", "status": 404}
        return {c.name: getattr(product, c.name) for c in product.__table__.columns}

    @provide_session()
    def get_by_shop(self, user_id: str, session) -> dict:
        """
        Get all products for a specific shop.
        :param shop_id: The ID of the shop to retrieve products for.
        :return: A list of products for the specified shop.
        """
        products = (
            session.query(self.model).filter(self.model.shop.has(user_id=user_id)).all()
        )
        return [
            {c.name: getattr(product, c.name) for c in product.__table__.columns}
            for product in products
        ]

    @provide_session()
    def update(self, config: dict, user_id: str, session) -> dict:
        """
        Update an existing product.
        :param config: The configuration for the product.
        :param user_id: The ID of the user updating the product.
        :return: The updated product.
        """
        product = (
            session.query(self.model)
            .filter(self.model.id == config["id"], self.model.shop.has(user_id=user_id))
            .first()
        )
        if not product:
            return {
                "error": "Product not found or you do not have permission to update it",
                "status": 404,
            }
        for key, value in config.items():
            setattr(product, key, value)
        session.commit()
        session.refresh(product)
        return {c.name: getattr(product, c.name) for c in product.__table__.columns}

    @provide_session()
    def delete(self, product_id: int, user_id: str, session) -> dict:
        """
        Delete a product.
        :param config: The configuration for the product.
        :param user_id: The ID of the user deleting the product.
        :return: The deleted product.
        """
        product = (
            session.query(self.model)
            .filter(self.model.id == product_id, self.model.shop.has(user_id=user_id))
            .first()
        )
        if not product:
            return {
                "error": "Product not found or you do not have permission to delete it",
                "status": 404,
            }
        session.delete(product)
        session.commit()
        return {"message": "Product deleted successfully"}
