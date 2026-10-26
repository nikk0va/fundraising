import os
import sys
import time
import requests
from sqlalchemy import text
from db import get_engine

URL, TOKEN, JAR = os.environ["MONO_API_URL"], os.environ["MONO_TOKEN"], os.environ["MONO_JAR_ID"]
campaign_id = int(sys.argv[1])

DDL = """
CREATE TABLE IF NOT EXISTS raw.donations_api (
    id text PRIMARY KEY, tx_time bigint, description text, comment text,
    amount bigint, balance bigint, currency_code int,
    jar_id text, campaign_id int, loaded_at timestamptz DEFAULT now())
"""
INSERT = """
INSERT INTO raw.donations_api
    (id, tx_time, description, comment, amount, balance, currency_code, jar_id, campaign_id)
VALUES (:id, :tx_time, :description, :comment, :amount, :balance, :currency_code, :jar_id, :campaign_id)
ON CONFLICT (id) DO NOTHING
"""

engine = get_engine()
with engine.begin() as conn:
    conn.execute(text(DDL))
    last = conn.execute(text("SELECT max(tx_time) FROM raw.donations_api WHERE jar_id = :j"),
                        {"j": JAR}).scalar()

now = int(time.time())
t_from = (last + 1) if last else now - 7 * 86400
r = requests.get(f"{URL}/personal/statement/{JAR}/{t_from}/{now}",
                 headers={"X-Token": TOKEN}, timeout=30)
r.raise_for_status()
txs = r.json()

rows = [{"id": t["id"], "tx_time": t["time"], "description": t.get("description"),
         "comment": t.get("comment"), "amount": t["amount"], "balance": t.get("balance"),
         "currency_code": t.get("currencyCode"), "jar_id": JAR, "campaign_id": campaign_id}
        for t in txs]
if rows:
    with engine.begin() as conn:
        conn.execute(text(INSERT), rows)
print(f"fetched {len(rows)} transactions since {t_from}")
