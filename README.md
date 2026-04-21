# Wired ETL Pipeline
Pipeline ETL sederhana untuk scraping artikel dari Wired.com, melakukan transformasi data, dan menyimpannya ke PostgreSQL menggunakan Apache Airflow.

---

## Overview
Project ini membangun alur data end-to-end:
1. **Scraping** → Mengambil artikel dari Wired.com menggunakan Selenium
2. **Transformasi** → Membersihkan data 
3. **Load** → Menyimpan data ke PostgreSQL
4. **Orkestrasi** → Menggunakan Apache Airflow untuk otomatisasi pipeline
5. **API (Opsional)** → Menyajikan data melalui FastAPI

---

## Project Structure

```text
Responsi-IPBD/
├── app/
│   ├── api/            # FastAPI endpoint
│   ├── db/             # Koneksi & query database
│   ├── pipeline/       # Transform & load
│   ├── scraper/        # Selenium scraper
│   └── config.py
│
├── dags/
│   └── wired_pipeline_dag.py   # Airflow DAG
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Cara Menjalankan

### 1. Aktifkan virtual environment

```bash
venv\Scripts\activate
```

---

### 2. Jalankan Docker

```bash
docker compose up -d
```

---

### 3. Inisialisasi database

```bash
python -m app.db.init_db
```

---

### 4. Jalankan pipeline manual

```bash
python -m app.pipeline.load_to_db
```

---

### 5. Jalankan API

```bash
uvicorn app.api.main:app --reload
```

Akses:

```
http://127.0.0.1:8000/articles
```

---

### 6. Jalankan Airflow

Buka:

```
http://localhost:8080
```

---

## Contoh Query

### 1. Judul & author (tanpa "By")

```sql
SELECT title, clean_author 
FROM wired_articles;
```

---

### 2. Top 3 author

```sql
SELECT clean_author, COUNT(*) 
FROM wired_articles
GROUP BY clean_author
ORDER BY COUNT(*) DESC
LIMIT 3;
```

---

### 3. Cari keyword (AI, Climate, Security)

```sql
SELECT *
FROM wired_articles
WHERE title ILIKE '%AI%'
   OR title ILIKE '%Climate%'
   OR title ILIKE '%Security%';
```
