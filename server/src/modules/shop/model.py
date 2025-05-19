from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer, Column
from src.services.database import Base
from src.modules.users.model import UserModel


class ShopModel(Base):
    __tablename__ = "shop"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    user_id = Column(ForeignKey("user.id"), nullable=False)
    user = relationship(
        UserModel,
        back_populates="shop",
        cascade="all, delete-orphan",
        single_parent=True,
    )
    products = relationship(
        "ProductModel",
        back_populates="shop",
        foreign_keys="[ProductModel.shop_id]",
        cascade="all, delete-orphan",
    )
