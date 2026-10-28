import sys
import pandas as pd
from sqlalchemy import text
from db import get_engine

COLS = {
    "Дата та час операції": "operation_ts",
    "Категорія операції": "category",
    "Сума": "amount",
    "Валюта": "currency",
    "Додаткова інформація": "counterparty",
    "Коментар до платежу": "comment",
    "Залишок": "balance",
    "Валюта залишку": "balance_currency",
}

path, campaign_id = sys.argv[1], int(sys.argv[2])
df = pd.read_csv(path, dtype=str, encoding="utf-8-sig").rename(columns=COLS)
for c in ["amount", "balance"]:
    if c in df.columns:
        df[c] = (df[c].str.replace("\u00a0", "", regex=False)
                      .str.replace(" ", "", regex=False)
                      .str.replace(",", ".", regex=False))
df.insert(0, "source_row_no", range(1, len(df) + 1))
df["campaign_id"] = campaign_id
df["source_file"] = path
df["loaded_at"] = pd.Timestamp.now(tz="UTC")

engine = get_engine()
with engine.begin() as conn:
    if conn.execute(text("SELECT to_regclass('raw.donations_new')")).scalar():
        conn.execute(text("DELETE FROM raw.donations_new WHERE campaign_id = :c"), {"c": campaign_id})
    df.to_sql("donations_new", conn, schema="raw", if_exists="append", index=False)
print(f"loaded {len(df)} rows for campaign {campaign_id}")
