# app/main.py

from fastapi import FastAPI, Depends
from api import products, sales, inventory
import sys
from pathlib import Path
from database import async_session
from authentication.auth import validate_requester
from datadog_logging.logger import logInfo, logError

# Assuming the script is in the current_folder
current_folder = Path(__file__).resolve().parent
project_root = current_folder.parent

# Add the project root to the Python path
sys.path.append(str(project_root))

import asyncio
from scripts.create_tables_and_populate_data import create_tables, create_fake_amazon_data

async def main(app):
    try:
        await create_tables()
        await create_fake_amazon_data(async_session())
        logInfo("Database initialized successfully", "Fake data inserted sucessfully", "normal")
    except:
        logError("Database not initialized successfully", "Fake data not inserted sucessfully", "critical")

app = FastAPI()

# Use asyncio.create_task to run main in the background
asyncio.create_task(main(app))

app.include_router(products.router, prefix="/products", tags=["Products"], dependencies=[Depends(validate_requester)])
app.include_router(sales.router, prefix="/sales", tags=["Sales"], dependencies=[Depends(validate_requester)])
app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"], dependencies=[Depends(validate_requester)])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    logInfo("App is running successfully", "App is running successfully", 5)
