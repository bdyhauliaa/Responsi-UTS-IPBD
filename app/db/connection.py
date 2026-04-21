from sqlalchemy import create_engine
from sqlalchemy.engine import URL

connection_url = URL.create(
    drivername="postgresql+pg8000",
    username="postgres",
    password="postgres",
    host="127.0.0.1",
    port=5433,   # ⬅️ SESUAIKAN
    database="wired",
)

engine = create_engine(connection_url, echo=False, future=True)