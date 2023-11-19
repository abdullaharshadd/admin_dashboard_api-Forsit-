from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from database import get_db
from models.inventory import InventoryCreate, InventoryDB, Inventory
from datadog_logging.logger import logInfo, logError
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/", response_model=Inventory)
async def create_inventory(inventory_create: InventoryCreate, db: AsyncSession = Depends(get_db)):
    try:
        existing_inventory = await db.execute(
            select(InventoryDB).where(InventoryDB.product_id == inventory_create.product_id)
        )
        existing_inventory_data = existing_inventory.first()

        if existing_inventory_data:
            raise HTTPException(status_code=400, detail="Inventory entry already exists for the product")

        new_inventory_entry = InventoryDB(**inventory_create.dict())
        db.add(new_inventory_entry)
        await db.commit()
        await db.refresh(new_inventory_entry)
        logInfo("Inventory created successfully", "Inventory created successfully", "normal")
        return new_inventory_entry
    except Exception as e:
        logError("Error creating inventory", str(e), "critical")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{product_id}", response_model=Inventory)
async def get_product_inventory(product_id: int, db: AsyncSession = Depends(get_db)):
    try:
        statement = select(InventoryDB).where(InventoryDB.product_id == product_id)
        result = await db.execute(statement)
        inventory_data = result.scalar()

        if inventory_data is None:
            return JSONResponse(content={"detail": "Inventory not found"}, status_code=404)

        logInfo("Fetched product inventory successfully", "Fetched product inventory successfully", "normal")
        return inventory_data
    except Exception as e:
        logError("Failed to fetch product inventory", str(e), "critical")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/{product_id}", response_model=Inventory)
async def update_inventory(product_id: int, updated_inventory: InventoryCreate, db: AsyncSession = Depends(get_db)):
    try:
        existing_inventory = await db.execute(select(InventoryDB).where(InventoryDB.product_id == product_id))
        existing_inventory_data = existing_inventory.first()

        if existing_inventory_data is None:
            raise HTTPException(status_code=404, detail="Inventory not found for the product")

        existing_inventory_data.quantity = updated_inventory.quantity
        existing_inventory_data.low_stock_alert = updated_inventory.low_stock_alert

        await db.commit()
        await db.refresh(existing_inventory_data)
        logInfo("Product inventory updated successfully", "Product inventory updated successfully", "normal")
        return existing_inventory_data
    except Exception as e:
        logError("Failed to update product inventory", str(e), "critical")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/inventory/{product_id}", response_model=dict)
async def delete_product_inventory(product_id: int, db: AsyncSession = Depends(get_db)):
    try:
        async with db.begin():
            existing_inventory = await db.execute(
                select(InventoryDB).where(InventoryDB.product_id == product_id)
            )
            existing_inventory_data = existing_inventory.first()

            if existing_inventory_data is None:
                raise HTTPException(status_code=404, detail="Inventory not found for the product")

            statement = delete(InventoryDB).where(InventoryDB.product_id == product_id)
            await db.execute(statement)
            logInfo("Product inventory deleted successfully", "Product inventory deleted successfully", "normal")
            return {"message": "Inventory deleted successfully"}
    except Exception as e:
        logError("Failed to delete product inventory", str(e), "critical")
        raise HTTPException(status_code=500, detail="Internal Server Error")
