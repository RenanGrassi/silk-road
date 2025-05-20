import bcrypt
from datetime import timedelta, datetime
import jwt

SECRET_KEY = "random_secret_key"
ALGORITHM = "HS256"


class AuthService:

    @staticmethod
    def hash_password(plain_password: str) -> str:
        return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def check_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=48)):
        to_encode = data.copy()
        to_encode["exp"] = datetime.utcnow() + expires_delta
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def decode_access_token(token: str):
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def authenticate():
        """
        Authenticate the user using the provided token.
        """

        def wrapper(func):
            def inner(*args, **kwargs):
                token = kwargs.get("token")
                if token is None:
                    for arg in args:
                        print(arg)
                        if isinstance(arg, dict) and "token" in arg:
                            token = arg["token"]
                            break
                if token is None:
                    raise Exception("Token não fornecido")
                decoded_token = AuthService.decode_access_token(token)
                if decoded_token is None:
                    raise Exception("Token inválido ou expirado")
                return func(*args, auth=decoded_token, **kwargs)

            return inner

        return wrapper
