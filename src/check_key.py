# src/check_key.py

from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("GEMINI_API_KEY")

print("Loaded:", bool(key))
print("First 10 chars:", key[:10])
print("Length:", len(key))