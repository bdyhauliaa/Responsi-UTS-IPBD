from sqlalchemy import text
from app.db.connection import engine

def create_table():
    query = """
    CREATE TABLE IF NOT EXISTS wired_articles (
        id SERIAL PRIMARY KEY,
        title TEXT,
        url TEXT UNIQUE,
        description TEXT,
        author TEXT,
        scraped_at TIMESTAMP,
        source TEXT
    );
    """

    with engine.begin() as conn:
        conn.execute(text(query))

if __name__ == "__main__":
    create_table()
    print("Tabel wired_articles berhasil dibuat.")