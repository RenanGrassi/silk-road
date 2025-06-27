from src.abstracts.abstract_crud_service import AbstractCRUDService
from src.modules.users.model import UserModel
from src.services.database import provide_session
from src.services.auth import AuthService


class UserService(AbstractCRUDService):
    """
    Service class for managing products.
    """

    @property
    def model(self):
        return UserModel

    @provide_session()
    def login(self, config: dict, session) -> dict:
        """
        Login a user.
        :param config: The configuration for the login.
        :return: The result of the login.
        """
        print("Login attempt with config:", config)
        user = (
            session.query(self.model)
            .filter(self.model.email == config.get("email"))
            .first()
        )
        print("User found:", user)
        if not user:
            return {
                "error": "User not found",
                "status": 404,
            }
        validate = AuthService.check_password(config.get("password"), user.password)
        if not validate:
            return {
                "error": "Invalid password",
                "status": 401,
            }
        access_token = AuthService.create_access_token(
            data={"email": user.email, "id": user.id}
        )
        return {
            "access_token": access_token,
        }

    @provide_session()
    def get(self, user_id: str, session) -> dict:
        """
        Get a user by their ID.
        :param user_id: The ID of the user.
        :return: The user with the specified ID.
        """
        user = session.query(self.model).filter(self.model.id == user_id).first()
        if not user:
            return {
                "error": "User not found",
                "status": 404,
            }
        return {c.name: getattr(user, c.name) for c in user.__table__.columns}

    @provide_session()
    def add_balance(self, amount: float, user_id: str, session) -> dict:
        """
        Add balance to a user.
        :param user_id: The ID of the user.
        :param amount: The amount to add.
        :return: The updated user.
        """
        user = session.query(self.model).filter(self.model.id == user_id).first()
        if not user:
            return {
                "error": "User not found",
                "status": 404,
            }
        user.balance += amount
        session.commit()
        session.refresh(user)
        return {c.name: getattr(user, c.name) for c in user.__table__.columns}
