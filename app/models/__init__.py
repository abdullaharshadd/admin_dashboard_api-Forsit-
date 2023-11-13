# app/models/__init__.py
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import your models so that they are accessible when importing the package
from .product import ProductDB
from .sale import SaleDB
from .inventory import InventoryDB