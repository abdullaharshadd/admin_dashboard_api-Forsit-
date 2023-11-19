from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, text
from models.sale import SaleCreate, Sale, SaleDB
from models.inventory import InventoryCreate, Inventory, InventoryDB
from database import get_db
from sqlalchemy.future import select
from datetime import date
from pydantic import parse_obj_as
from datadog_logging.logger import logInfo, logError  # Import your log functions here
from fastapi.responses import JSONResponse

router = APIRouter()

# Sales Endpoints

@router.post("/", response_model=Sale)
async def create_sale(sale: SaleCreate, db: AsyncSession = Depends(get_db)):
    try:
        async with db.begin():
            new_sale = SaleDB(**sale.dict())
            db.add(new_sale)
            await db.commit()
            await db.refresh(new_sale)
            logInfo("Sale created successfully", "Sale created successfully", "normal")
            return Sale(**new_sale.__dict__)
    except Exception as e:
        logError("Error creating sale", str(e), "critical")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{sale_id}", response_model=Sale)
async def get_sale(sale_id: int, db: AsyncSession = Depends(get_db)):
    try:
        statement = select(SaleDB).where(SaleDB.id == sale_id)
        result = await db.execute(statement)
        sale_db = result.scalar()

        if sale_db is None:
            return JSONResponse(content={"detail": "Sale not found"}, status_code=404)

        logInfo("fetched sales succesfully", "fetched sales succesfully", "normal")
        return Sale(**sale_db.__dict__)
    except Exception as e:
        logError("Error fetching sale", str(e), "critical")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/", response_model=list[Sale])
async def get_all_sales(db: AsyncSession = Depends(get_db)):
    try:
        statement = select(SaleDB)
        result = await db.execute(statement)
        sales_db = result.scalars().all()

        sales = []
        for sale in sales_db:
            sale_dict = sale.__dict__
            sale_dict['sale_date'] = str(sale_dict['sale_date'])
            sale_model = parse_obj_as(Sale, sale_dict)
            sales.append(sale_model)

        logInfo("fetched sale succesfully", "fetched sale succesfully", "normal")
        return sales
    except Exception as e:
        logError("Error fetching sales", str(e), "critical")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/revenue/daily", response_model=dict)
async def get_daily_revenue(db: AsyncSession = Depends(get_db)):
    try:
        statement = select(
            func.DATE_FORMAT(SaleDB.sale_date, "%Y-%m-%d").label('day'),
            func.sum(SaleDB.revenue).label('total_revenue')
        ).group_by(func.DATE_FORMAT(SaleDB.sale_date, "%Y-%m-%d"))

        result = await db.execute(statement)
        revenue_data = result.fetchall()
        logInfo("fetched daily revenue succesfully", "fetched daily revenue succesfully", "normal")
        return {"daily_revenue": [{"day": row.day, "total_revenue": row.total_revenue} for row in revenue_data]}
    except Exception as e:
        logError("Error fetching daily revenue", str(e), "critical")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/revenue/weekly", response_model=dict)
async def get_weekly_revenue(db: AsyncSession = Depends(get_db)):
    try:
        statement = select(
            func.DATE_FORMAT(SaleDB.sale_date, "%Y-%m-%d").label('week_start'),
            func.sum(SaleDB.revenue).label('total_revenue')
        ).group_by(
            func.DATE_FORMAT(SaleDB.sale_date - func.DAYOFWEEK(SaleDB.sale_date) + 1, "%Y-%m-%d"),
            SaleDB.sale_date
        )

        result = await db.execute(statement)
        revenue_data = result.fetchall()
        logInfo("fetched weekly revenue succesfully", "fetched weekly revenue succesfully", "normal")

        return {"weekly_revenue": [{"week_start": row.week_start, "total_revenue": row.total_revenue} for row in revenue_data]}
    except Exception as e:
        logError("Error fetching weekly revenue", str(e), "critical")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/revenue/monthly", response_model=dict)
async def get_monthly_revenue(db: AsyncSession = Depends(get_db)):
    try:
        statement = select(
            func.DATE_FORMAT(SaleDB.sale_date, "%Y-%m").label('month'),
            func.sum(SaleDB.revenue).label('total_revenue')
        ).group_by(func.DATE_FORMAT(SaleDB.sale_date, "%Y-%m"))

        result = await db.execute(statement)
        revenue_data = result.fetchall()
        logInfo("fetched monthly revenue succesfully", "fetched monthly revenue succesfully", "normal")

        return {"monthly_revenue": [{"month": row.month, "total_revenue": row.total_revenue} for row in revenue_data]}
    except Exception as e:
        logError("Error fetching monthly revenue", str(e), "critical")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/revenue/annual", response_model=dict)
async def get_annual_revenue(db: AsyncSession = Depends(get_db)):
    try:
        statement = select(
            func.DATE_FORMAT(SaleDB.sale_date, "%Y").label('year'),
            func.sum(SaleDB.revenue).label('total_revenue')
        ).group_by(func.DATE_FORMAT(SaleDB.sale_date, "%Y"))

        result = await db.execute(statement)
        revenue_data = result.fetchall()

        logInfo("fetched annual revenue succesfully", "fetched annual revenue succesfully", "normal")
        return {"annual_revenue": [{"year": row.year, "total_revenue": row.total_revenue} for row in revenue_data]}
    except Exception as e:
        logError("Error fetching annual revenue", str(e), "critical")
        raise HTTPException(status_code=500, detail="Internal Server Error")
