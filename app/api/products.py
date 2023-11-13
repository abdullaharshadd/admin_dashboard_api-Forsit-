from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from models.product import ProductDB, Product, ProductCreate, ProductBase
from database import get_db
from sqlalchemy.future import select
from sqlalchemy import update, delete

router = APIRouter()

@router.post("/", response_model=Product)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_product = ProductDB(**product.dict()) 
        db.add(new_product)
        await db.commit()
        await db.refresh(new_product)
        return Product(**new_product.__dict__)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=list[Product])
async def get_all_products(
    name: str = Query(None, title="Filter by product name"),
    product_id: int = Query(None, title="Filter by product ID"),
    description: str = Query(None, title="Filter by product description"),
    price: float = Query(None, title="Filter by product price"),
    db: AsyncSession = Depends(get_db)
):
    try:
        statement = select(ProductDB)

        # Applying filtering based on the query parameters
        if name:
            statement = statement.where(ProductDB.name.ilike(f"%{name}%"))
        if product_id:
            statement = statement.where(ProductDB.id == product_id)
        if description:
            statement = statement.where(ProductDB.description.ilike(f"%{description}%"))
        if price is not None:
            statement = statement.where(ProductDB.price == price)

        result = await db.execute(statement)
        products_db = result.scalars().all()

        return products_db
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    try:
        statement = select(ProductDB).where(ProductDB.id == product_id)
        result = await db.execute(statement)
        
        product_db = result.scalar()
        
        if product_db is None:
            raise HTTPException(status_code=404, detail="Product not found")

        return product_db
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{product_id}", response_model=Product)
async def update_product(product_id: int, product_update: ProductBase, db: AsyncSession = Depends(get_db)):
    try:
        # Your logic to update the product in the database
        statement = update(ProductDB).where(ProductDB.id == product_id).values(**product_update.dict())
        await db.execute(statement)
        await db.commit()

        # Retrieve the updated product
        updated_product = await db.execute(select(ProductDB).where(ProductDB.id == product_id))
        updated_product_db = updated_product.scalar()

        if updated_product_db is None:
            raise HTTPException(status_code=404, detail="Product not found")

        return updated_product_db
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{product_id}", response_model=dict)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    try:
        # Check if the product exists before attempting to delete
        existing_product = await db.execute(select(ProductDB).where(ProductDB.id == product_id))
        existing_product_db = existing_product.scalar()
    
        if existing_product_db is None:
            raise HTTPException(status_code=404, detail="Product not found")
        # Delete the product from the database
        statement = delete(ProductDB).where(ProductDB.id == product_id)
        await db.execute(statement)
        return {"message": "Product deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Product not found or something went wrong")
