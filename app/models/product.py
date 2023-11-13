from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, Index
from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData
from . import Base

class ProductBase(BaseModel):
    name: str
    description: str
    price: float

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

# Define SQLAlchemy model for the products table
class ProductDB(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(1000))
    price = Column(Float)

    __table_args__ = (
        Index('idx_product_name', name),
        Index('idx_product_price', price),
    )
