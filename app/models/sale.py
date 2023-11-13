from pydantic import BaseModel
from sqlalchemy import Column, Integer, ForeignKey, Float, Date, Index
from models.product import ProductDB
from sqlalchemy.orm import declarative_base
from . import Base

class SaleBase(BaseModel):
    product_id: int
    quantity_sold: int
    sale_date: Date

    class Config:
        arbitrary_types_allowed = True

class SaleCreate(SaleBase):
    pass

class Sale(SaleBase):
    id: int
    revenue: float

# Define SQLAlchemy model for the sales table
class SaleDB(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), index=True)
    quantity_sold = Column(Integer)
    sale_date = Column(Date)
    revenue = Column(Float)

    __table_args__ = (
        Index('idx_quantity_sold',quantity_sold),
        Index('idx_sale_date', sale_date),
    )
