from pydantic import BaseModel
from sqlalchemy import Column, Integer, Boolean, ForeignKey, Float, Index
from models.product import ProductDB
from sqlalchemy.orm import declarative_base
from . import Base

class InventoryBase(BaseModel):
    product_id: int
    quantity: int
    low_stock_alert: bool

class InventoryCreate(InventoryBase):
    pass

class Inventory(InventoryBase):
    id: int

# Define SQLAlchemy model for the inventory table
class InventoryDB(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), index=True)
    quantity = Column(Integer)
    low_stock_alert = Column(Boolean, default=False)

    __table_args__ = (
        Index('idx_quantity', quantity),
        Index('idx_low_stock_alert', low_stock_alert),
    )
