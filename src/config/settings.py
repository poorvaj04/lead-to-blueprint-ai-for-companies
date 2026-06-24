from pathlib import Path

from dotenv import load_dotenv
import os

# Project Root

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load .env

load_dotenv(BASE_DIR / ".env")


class Settings:

    # ====================================
    # Project
    # ====================================

    PROJECT_NAME = "AI Project Qualification System"

    VERSION = "1.0"

    DEBUG = True

    # ====================================
    # Database
    # ====================================

    DB_HOST = os.getenv("DB_HOST")

    DB_PORT = os.getenv("DB_PORT")

    DB_NAME = os.getenv("DB_NAME")

    DB_USER = os.getenv("DB_USER")

    DB_PASSWORD = os.getenv("DB_PASSWORD")

    DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # ====================================
    # Gemini
    # ====================================

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # ====================================
    # Ollama
    # ====================================

    OLLAMA_BASE_URL = "http://localhost:11434"

    OLLAMA_MODEL = "qwen3:8b"

    # ====================================
    # Groq
    # ====================================

    GROQ_API_KEYS = [
        os.getenv("GROQ_API_KEY_1"),
        os.getenv("GROQ_API_KEY_2"),
        os.getenv("GROQ_API_KEY_3"),
        os.getenv("GROQ_API_KEY_4")
    ]
    GROQ_API_KEYS = [k for k in GROQ_API_KEYS if k]

    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    GROQ_FALLBACK_MODEL = os.getenv("GROQ_FALLBACK_MODEL", "llama-3.1-8b-instant")

    # ====================================
    # Dashboard Auth
    # ====================================

    MANAGER_USERNAME = os.getenv("MANAGER_USERNAME", "admin")
    
    MANAGER_PASSWORD = os.getenv("MANAGER_PASSWORD", "securepassword123")

    # ====================================
    # Project Paths
    # ====================================

    DATA_DIR = BASE_DIR / "data"

    PROMPT_DIR = DATA_DIR / "prompts"

    AUDIO_DIR = DATA_DIR / "audio"

    COMPANY_DIR = DATA_DIR / "company"

    LOG_DIR = BASE_DIR / "logs"

    UPLOAD_DIR = BASE_DIR / "uploads"

    # ====================================
    # Logging
    # ====================================

    LOG_LEVEL = "INFO"

    # ====================================
    # Future Services
    # ====================================

    WHISPER_MODEL = "large-v3"

    MAX_CLARIFICATION_ROUNDS = 3

    # AI Models
    PRIMARY_LLM = "qwen3"
    FALLBACK_LLM = "gemini"
    # Company
    COMPANY_NAME = "ABC Software Solutions"
    COMPANY_DOMAIN = "Custom Software Development"


    # ====================================
    # Whisper
    # ====================================

    WHISPER_MODEL_PATH = os.getenv(
        "WHISPER_MODEL_PATH"
    )

    WHISPER_LANGUAGE = os.getenv(
        "WHISPER_LANGUAGE",
        "en"
    )

    WHISPER_MAX_NEW_TOKENS = int(
        os.getenv(
            "WHISPER_MAX_NEW_TOKENS",
            "256"
        )
    )


settings = Settings()