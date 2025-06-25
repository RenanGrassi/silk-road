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
