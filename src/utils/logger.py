import logging
from pathlib import Path

from src.config.settings import settings

# Create logs directory
Path(settings.LOG_DIR).mkdir(parents=True, exist_ok=True)


def get_logger(name: str):
    """
    Create and return a named logger.
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Console Output
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File Output
    file_handler = logging.FileHandler(
        settings.LOG_DIR / f"{name.lower()}.log",
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.propagate = False

    return logger


# ===============================
# Project Loggers
# ===============================

system_logger = get_logger("System")

agent_logger = get_logger("Agent")

database_logger = get_logger("Database")

workflow_logger = get_logger("Workflow")

reasoning_logger = get_logger("Reasoning")