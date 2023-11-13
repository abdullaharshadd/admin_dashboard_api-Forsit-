from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models.inventory import InventoryCreate, InventoryDB, Inventory

router = APIRouter()

@router.post("/", response_model=Inventory)
async def create_inventory(inventory_create: InventoryCreate, db: AsyncSession = Depends(get_db)):
    # Check if the product already has an existing inventory entry
    existing_inventory = await db.execute(
        select(InventoryDB).where(InventoryDB.product_id == inventory_create.product_id)
    )
    existing_inventory_data = existing_inventory.first()

    if existing_inventory_data:
        raise HTTPException(status_code=400, detail="Inventory entry already exists for the product")

    # Create a new inventory entry
    new_inventory_entry = InventoryDB(**inventory_create.dict())
    db.add(new_inventory_entry)
    await db.commit()
    await db.refresh(new_inventory_entry)

    return new_inventory_entry

@router.get("/{product_id}", response_model=Inventory)
async def get_product_inventory(product_id: int, db: AsyncSession = Depends(get_db)):
    statement = select(InventoryDB).where(InventoryDB.product_id == product_id)
    result = await db.execute(statement)
    inventory_data = result.first()

    if inventory_data is None:
        raise HTTPException(status_code=404, detail="Inventory not found for the product")

    return inventory_data

@router.put("/{product_id}", response_model=Inventory)
async def update_inventory(product_id: int, updated_inventory: InventoryCreate, db: AsyncSession = Depends(get_db)):
    # Check if the product exists in the inventory
    existing_inventory = await db.execute(select(InventoryDB).where(InventoryDB.product_id == product_id))
    existing_inventory_data = existing_inventory.first()

    if existing_inventory_data is None:
        raise HTTPException(status_code=404, detail="Inventory not found for the product")

    # Update inventory levels
    existing_inventory_data.quantity = updated_inventory.quantity
    existing_inventory_data.low_stock_alert = updated_inventory.low_stock_alert

    await db.commit()
    await db.refresh(existing_inventory_data)

    return existing_inventory_data

@router.delete("/inventory/{product_id}", response_model=dict)
async def delete_product_inventory(product_id: int, db: AsyncSession = Depends(get_db)):
    try:
        async with db.begin():
            # Check if the inventory entry exists before attempting to delete
            existing_inventory = await db.execute(
                select(InventoryDB).where(InventoryDB.product_id == product_id)
            )
            existing_inventory_data = existing_inventory.first()

            if existing_inventory_data is None:
                raise HTTPException(status_code=404, detail="Inventory not found for the product")

            # Delete the inventory entry
            statement = delete(InventoryDB).where(InventoryDB.product_id == product_id)
            await db.execute(statement)

            return {"message": "Inventory deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))