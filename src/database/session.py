from sqlalchemy.orm import sessionmaker

from src.database.db import engine

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)