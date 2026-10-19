from pathlib import Path

import polars as pl
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

app = FastAPI(title="Streaming Log Pipeline", description="Bellek korumalı log analiz servisi", version="1.0.0")
BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = BASE_DIR / "logs.csv"


def parse_logs() -> pl.LazyFrame:
    if not LOG_FILE.exists():
        raise HTTPException(status_code=404, detail="Log dosyası bulunamadı. Önce python generate_logs.py komutunu çalıştırın.")

    logs = pl.scan_csv(LOG_FILE)
    if "log" not in logs.collect_schema().names():
        raise HTTPException(status_code=422, detail="CSV dosyasında 'log' sütunu bulunmalı.")

    return logs.with_columns(
        pl.col("log").str.extract(r"(\d{1,3}(?:\.\d{1,3}){3})", 1).alias("ip"),
        pl.col("log").str.extract(r"\b([1-5]\d{2})$", 1).alias("status"),
        pl.col("log").str.extract(r"\b(ERROR|WARN|CRITICAL)\b", 1).alias("level"),
    )


def analyze_logs() -> list[dict]:
    summary = (
        parse_logs()
        .filter(pl.col("level").is_not_null())
        .group_by("level", "status")
        .agg(pl.len().alias("count"))
        .sort("level", "status")
        .collect(engine="streaming")
    )
    return summary.to_dicts()


@app.get("/")
def home():
    return {"message": "Streaming Log Pipeline API", "status": "active"}


@app.get("/analyze")
def get_analysis():
    results = analyze_logs()
    return {"total_groups": len(results), "error_distribution": results}


@app.get("/dashboard")
def dashboard():
    return FileResponse(BASE_DIR / "dashboard.html")
