import pandas as pd
from db import get_engine

rows = [
    (1, "Fundraiser 1", "2025-03-09", "2025-03-12"),
    (2, "Fundraiser 2", "2025-05-09", "2025-05-12"),
    (3, "Fundraiser 3", "2026-09-14", "2026-09-18"),
]
df = pd.DataFrame(rows, columns=["campaign_id", "name", "start_date", "end_date"])
df.to_sql("campaigns", get_engine(), schema="raw", if_exists="replace", index=False)
print("campaigns:", len(df))
