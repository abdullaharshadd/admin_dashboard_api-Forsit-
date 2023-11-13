from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

import configparser

config = configparser.ConfigParser()
config.read('../config.ini')

# Read database configuration
database_url = config['database']['DATABASE_URL']

# Asynchronous engine and session
async_engine = create_async_engine(database_url, echo=True)

async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Function to get asynchronous database session
async def get_db():
    db = async_session()
    try:
        yield db
    finally:
        await db.close()
