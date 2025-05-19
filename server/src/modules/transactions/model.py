from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.services.database import Base
from src.modules.products.model import ProductModel


class TransactionModel(Base):
    __tablename__ = "transaction"
    id = Column(Integer, primary_key=True)
    buyer_id = Column(ForeignKey("user.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    product_id = Column(ForeignKey("product.id"), nullable=False)
    seller_id = Column(ForeignKey("user.id"), nullable=False)
    buyer = relationship(
        "UserModel",
        back_populates="transactions_buyer",
        foreign_keys=[buyer_id],
    )
    seller = relationship(
        "UserModel",
        back_populates="transactions_seller",
        foreign_keys=[seller_id],
    )
    product = relationship(
        ProductModel,
        back_populates="transactions",
        foreign_keys=[product_id],
    )
