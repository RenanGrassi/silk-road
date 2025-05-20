from sqlalchemy.orm import relationship
from sqlalchemy import String, ForeignKey, Double, Column, Integer
from src.services.database import Base


class ProductModel(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, auto_increment=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Double, nullable=False)
    images = relationship(
        "ImageModel",
        back_populates="product",
        cascade="all, delete-orphan",
    )
    sales = relationship(
        "TransactionModel",
        back_populates="product",
        cascade="all, delete-orphan",
    )
    status = Column(String(10), default="ativo")
    shop_id = Column(ForeignKey("shop.id"), nullable=False)
    shop = relationship("ShopModel", back_populates="products")
    transactions = relationship(
        "TransactionModel",
        back_populates="product",
        foreign_keys="[TransactionModel.product_id]",
    )


class ImageModel(Base):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    url = Column(String(255), nullable=False)
    product_id = Column(ForeignKey("product.id"), nullable=False)
    product = relationship(ProductModel, back_populates="images")
