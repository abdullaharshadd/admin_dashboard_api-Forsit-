import sys
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine,  AsyncSession
import asyncio

# Assuming the script is in the current_folder
current_folder = Path(__file__).resolve().parent
project_root = current_folder.parent

# Add the project root to the Python path
sys.path.append(str(project_root))

from app.database import async_session, async_engine
# from app.models.product import ProductDB
from app.models import Base
from app.models.product import ProductDB
from app.models.sale import SaleDB
from app.models.inventory import InventoryDB
from datetime import datetime, timedelta
import random

async def create_fake_amazon_data(db: AsyncSession):
    try:
        async with db.begin():
            # Create sample products without the "category" field
            products = [
                ProductDB(
                    name=f"Product-{i}",
                    description=f"Description for Product-{i}",
                    price=random.uniform(10.0, 500.0),
                )
                for i in range(1, 51)
            ]

            # Add products to the database
            db.add_all(products)

        product_ids = [product.id for product in products]

        async with db.begin():
            # Create sample sales
            sales = [
                SaleDB(
                    product_id=random.choice(product_ids),
                    quantity_sold=random.randint(1, 20),
                    sale_date=datetime.utcnow() - timedelta(days=random.randint(1, 365)),
                    revenue=random.uniform(10.0, 500.0),
                )
                for _ in range(1, 41)
            ]

            # Add sales to the database
            db.add_all(sales)

        async with db.begin():
            # Create sample inventory
            inventory_entries = [
                InventoryDB(
                    product_id=random.choice(product_ids),
                    quantity=random.randint(10, 100),
                    low_stock_alert=random.choice([True, False]),
                )
                for _ in range(1, 41)
            ]

            # Add inventory entries to the database
            db.add_all(inventory_entries)

        print("Assumed Amazon data created successfully.")
    except Exception as e:
        print(f"Error creating assumed Amazon data: {e}")

async def create_tables():
    try:
        # Create tables
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        print("Tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")
        # Log the full exception traceback for debugging
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(create_tables())
