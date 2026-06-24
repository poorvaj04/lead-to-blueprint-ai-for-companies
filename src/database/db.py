from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

from src.config.settings import settings
from src.utils.logger import database_logger

try:
    engine = create_engine(
        settings.DATABASE_URL,
        echo=False,
        future=True
    )

    database_logger.info("Database Engine Created Successfully")

except SQLAlchemyError as e:
    database_logger.error(f"Database Engine Error: {e}")
    raise