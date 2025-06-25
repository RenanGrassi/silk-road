from src.abstracts.abstract_crud_service import AbstractCRUDService
from src.modules.shop.model import ShopModel
from src.services.database import provide_session


class ShopService(AbstractCRUDService):
    """
    Service class for managing products.
    """

    @property
    def model(self):
        return ShopModel

    @provide_session()
    def get(self, user_id: str, session) -> dict:
        """
        Get all products.
        :return: A list of all products.
        """
        shop = session.query(self.model).filter(self.model.user_id == user_id).first()
        if not shop:
            return None
        return {c.name: getattr(shop, c.name) for c in shop.__table__.columns}

    @provide_session()
    def create(self, config: dict, user_id: str, session) -> dict:
        """
        Create a new product.
        :param config: The configuration for the product.
        :param user_id: The ID of the user creating the product.
        :return: The created product.
        """
        current_shop = self.get(user_id)
        if current_shop:
            return {
                "error": "Shop already exists",
                "status": 400,
            }
        config["user_id"] = user_id
        shop = self.model(**config)
        session.add(shop)
        session.commit()
        session.refresh(shop)
        return shop.to_dict()

    @provide_session()
    def update(self, config: dict, user_id: str, session) -> dict:
        """
        Update an existing product.
        :param config: The configuration for the product.
        :param user_id: The ID of the user updating the product.
        :return: The updated product.
        """
        current_shop = self.get(user_id)
        if not current_shop:
            return {
                "error": "Shop not found",
                "status": 404,
            }
        for key, value in config.items():
            setattr(current_shop, key, value)
        session.commit()
        session.refresh(current_shop)
        return current_shop.to_dict()
