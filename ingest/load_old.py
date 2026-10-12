import sys
import pandas as pd
from sqlalchemy import text
from db import get_engine

COLS = {
    "Учасники/Participants": "donor_label",
    "Донати/Donations": "amount",
    "Валюти/Currencies": "currency",
    "У грн/In UAH": "amount_uah",
    "Способи переказу/Transfer methods": "source",
}

path, campaign_id = sys.argv[1], int(sys.argv[2])
df = pd.read_csv(path, sep=None, engine="python", dtype=str, encoding="utf-8-sig")
df.columns = [c.strip() for c in df.columns]
df = df[[c for c in df.columns if c in COLS]].rename(columns=COLS)
for c in ["amount", "amount_uah"]:
    df[c] = df[c].str.replace(" ", "", regex=False).str.replace(",", ".", regex=False)
df["campaign_id"] = campaign_id
df["source_file"] = path
df["loaded_at"] = pd.Timestamp.now(tz="UTC")

with get_engine().begin() as conn:
    if conn.execute(text("SELECT to_regclass('raw.donations_old')")).scalar():
        conn.execute(text("DELETE FROM raw.donations_old WHERE campaign_id = :c"), {"c": campaign_id})
    df.to_sql("donations_old", conn, schema="raw", if_exists="append", index=False)
print(f"loaded {len(df)} rows for campaign {campaign_id}")
