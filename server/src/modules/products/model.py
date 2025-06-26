from sqlalchemy.orm import relationship
from sqlalchemy import String, ForeignKey, Double, Column, Integer, Boolean
from src.services.database import Base


class ProductModel(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Double, nullable=False)

    sales = relationship(
        "TransactionModel",
        back_populates="product",
        cascade="all, delete-orphan",
    )

    is_active = Column(Boolean, default=False, nullable=False)
    shop_id = Column(ForeignKey("shop.id"), nullable=False)
    shop = relationship("ShopModel", back_populates="products")

    transactions = relationship(
        "TransactionModel",
        back_populates="product",
        foreign_keys="[TransactionModel.product_id]",
    )
