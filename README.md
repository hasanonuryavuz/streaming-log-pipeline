# Streaming Log Pipeline

Memory-efficient log analysis with Polars LazyFrame, Regex, FastAPI and a web dashboard.

## Features
- Lazy CSV scanning with Polars
- Regex extraction of IP addresses, HTTP status codes and log levels
- Streaming aggregation by error level and HTTP status
- FastAPI JSON endpoints
- Interactive dashboard with charts and tables
- Reproducible log data generator

## Technologies
Python, Polars, FastAPI, Uvicorn, Regex, HTML, CSS and JavaScript.

## Project Files
- `main.py` - Log parsing and FastAPI service
- `generate_logs.py` - Generate one million sample records
- `dashboard.html` - Interactive analytics dashboard
- `requirements.txt` - Python dependencies

## Installation
```bash
pip install -r requirements.txt
```

## Usage
Generate sample logs:
```bash
python generate_logs.py
```
Start the API:
```bash
python -m uvicorn main:app --reload
```
Open the dashboard: http://127.0.0.1:8000/dashboard

API documentation: http://127.0.0.1:8000/docs

JSON analysis: http://127.0.0.1:8000/analyze

## Test Results
The application was demonstrated with 1,000,000 generated log records.

| Level | Count |
|---|---:|
| ERROR | 249,948 |
| WARN | 249,920 |
| CRITICAL | 249,568 |
| Total matching records | 749,436 |

18 groups were produced across three log levels and six HTTP status codes. INFO records are excluded from the error distribution.

## Notes
Polars lazy scanning and streaming execution help reduce memory pressure. Peak RAM consumption and performance on files larger than available memory have not yet been benchmarked.

## Author
GitHub: @hasanonuryavuz
