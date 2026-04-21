import psycopg2

conn = psycopg2.connect(
    host="127.0.0.1",
    port=5432,
    dbname="wired",
    user="postgres",
    password="postgres"
)

print("Koneksi berhasil")
conn.close()