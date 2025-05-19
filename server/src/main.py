import asyncio
from src.utils.server_socket import SocketServer
from src.modules.users.model import UserModel
from src.modules.shop.model import ShopModel
from src.modules.products.model import ProductModel
from src.modules.transactions.model import TransactionModel
from src.services.database import Base, engine, provide_session
from src.services.auth import AuthService


@provide_session()
def create_user(session):
    """
    Função para criar um usuário.
    """
    retry_user = (
        session.query(UserModel).filter(UserModel.email == "murillo@gmail.com").first()
    )
    if retry_user:
        return
    else:
        user = UserModel(
            name="Murillo",
            email="murillo@gmail.com",
            password=AuthService.hash_password("123456"),
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


async def main():
    create_user()
    server = SocketServer()
    await server.start()


async def start():
    """
    Função para iniciar o servidor.
    """
    asyncio.run(main())


if __name__ == "__main__":
    """
    Função principal para iniciar o servidor.
    """
    Base.metadata.create_all(bind=engine)
    asyncio.run(main())
