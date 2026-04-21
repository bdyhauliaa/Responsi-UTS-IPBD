import json
from fastapi import FastAPI, HTTPException
from pathlib import Path

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = BASE_DIR / "data" / "raw" / "wired_articles.json"

@app.get("/")
def root():
    return {"message": "Wired API Running"}

@app.get("/articles")
def get_articles():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Data not found: {DATA_FILE}")