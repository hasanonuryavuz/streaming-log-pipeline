"""Generate reproducible sample HTTP logs without holding all rows in RAM."""
import argparse
import csv
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def generate(total_rows: int = 1_000_000, output: Path = BASE_DIR / "logs.csv") -> None:
    random.seed(42)
    levels = ["INFO", "WARN", "ERROR", "CRITICAL"]
    statuses = [200, 403, 404, 500, 502, 503]
    methods = ["GET", "POST", "PUT", "DELETE"]
    routes = ["/home", "/login", "/api", "/payment"]
    with output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["log"])
        for _ in range(total_rows):
            ip = f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}"
            level = random.choice(levels)
            status = random.choice(statuses)
            method = random.choice(methods)
            route = random.choice(routes)
            writer.writerow([f"{ip} {level} {method} {route} {status}"])
    print(f"{total_rows:,} log kaydi olusturuldu.")
    print(f"Dosya: {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate sample CSV log data")
    parser.add_argument("--rows", type=int, default=1_000_000, help="Number of generated rows")
    args = parser.parse_args()
    if args.rows < 1:
        parser.error("--rows must be greater than zero")
    generate(total_rows=args.rows)
