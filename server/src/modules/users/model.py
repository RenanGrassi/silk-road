from sqlalchemy.orm import relationship
from sqlalchemy import String, Column, Integer
from src.services.database import Base


class UserModel(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, auto_increment=True)
    name = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    shop = relationship(
        "ShopModel",
        back_populates="user",
        cascade="all, delete-orphan",
        single_parent=True,
    )
    transactions_buyer = relationship(
        "TransactionModel",
        back_populates="buyer",
        foreign_keys="[TransactionModel.buyer_id]",
    )
    transactions_seller = relationship(
        "TransactionModel",
        back_populates="seller",
        foreign_keys="[TransactionModel.seller_id]",
    )
