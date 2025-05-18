from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Double
from src.services.database import Base


class ProductModel(Base):
    __tablename__ = "product"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(Double, nullable=False)
    images: Mapped[list["ImageModel"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
    status: Mapped[str] = mapped_column(String(10), default="ativo")
    shop_id: Mapped[int] = mapped_column(ForeignKey("shop.id"), nullable=False)


class ImageModel(Base):
    __tablename__ = "image"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"), nullable=False)
    product: Mapped[ProductModel] = relationship(back_populates="images")
    status: Mapped[str] = mapped_column(String(10), default="ativo")
