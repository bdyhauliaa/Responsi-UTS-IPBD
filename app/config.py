import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL", "postgresql://postgres:postgres@localhost:5432/wired")
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/articles")
SCRAPE_TARGET = int(os.getenv("SCRAPE_TARGET", "100"))

print("DEBUG DB_URL =", DB_URL)