import requests
from sqlalchemy import text

from app.config import API_URL
from app.db.connection import engine
from app.db.init_db import create_table


def fetch_articles():
    response = requests.get(API_URL, timeout=60)
    response.raise_for_status()
    return response.json()


def load_articles_to_db():
    create_table()
    articles = fetch_articles()

    insert_sql = text("""
        INSERT INTO wired_articles
        (title, url, description, author, scraped_at, source)
        VALUES
        (:title, :url, :description, :author, :scraped_at, :source)
        ON CONFLICT (url) DO NOTHING
    """)

    with engine.begin() as conn:
        for article in articles:
            conn.execute(insert_sql, {
                "title": article.get("title"),
                "url": article.get("url"),
                "description": article.get("description"),
                "author": article.get("author"),
                "scraped_at": article.get("scraped_at"),
                "source": article.get("source", "Wired.com")
            })

    print(f"Load selesai. Total data: {len(articles)}")


if __name__ == "__main__":
    load_articles_to_db()