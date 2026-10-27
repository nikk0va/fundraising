import pandas as pd
from sqlalchemy import text
from db import get_engine

rows = [
    (1, "Fundraiser 1", "2025-03-09", "2025-03-12"),
    (2, "Fundraiser 2", "2025-05-09", "2025-05-12"),
    (4, "Fundraiser 4", "2024-07-07", "2024-07-13"),
    (3, "Fundraiser 3", "2026-09-14", "2026-09-18"),
    (99, "Simulated live fundraiser", "2026-10-18", "2026-12-31"),
]
df = pd.DataFrame(rows, columns=["campaign_id", "name", "start_date", "end_date"])

with get_engine().begin() as conn:
    if conn.execute(text("SELECT to_regclass('raw.campaigns')")).scalar():
        conn.execute(text("TRUNCATE raw.campaigns"))
    df.to_sql("campaigns", conn, schema="raw", if_exists="append", index=False)
print("campaigns:", len(df))
