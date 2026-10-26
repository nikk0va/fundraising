import json, os, random, time, uuid
from pathlib import Path
from fastapi import FastAPI, Header, HTTPException

STATE = Path("/state/state.json")
TOKEN = os.getenv("MOCK_TOKEN", "fake-token")
JAR_ID = os.getenv("MOCK_JAR_ID", "SIMJAR001")
NAMES = ["Олена Коваль", "Андрій Мельник", "Ірина Бондар", "Максим Шевчук",
         "Марія Ткачук", "Олег Романюк", "Софія Кравець", "Тарас Лисенко"]
AMOUNTS = [50, 100, 100, 200, 200, 500, 1000, 2000]
app = FastAPI()


def load():
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {"last_gen": int(time.time()), "balance": 0, "txs": []}


def generate(s):
    now = int(time.time())
    n = min((now - s["last_gen"]) // 90, 20)  # ~1 донат на 90 с, поки ніхто не питав
    if n <= 0:
        return
    for t in sorted(random.randint(s["last_gen"], now) for _ in range(n)):
        amount = random.choice(AMOUNTS) * 100
        s["balance"] += amount
        who = "🐈" if random.random() < 0.3 else random.choice(NAMES)
        s["txs"].append({
            "id": uuid.uuid4().hex[:16], "time": t,
            "description": f"Від: {who}", "mcc": 4829, "originalMcc": 4829,
            "amount": amount, "operationAmount": amount, "currencyCode": 980,
            "commissionRate": 0, "cashbackAmount": 0,
            "balance": s["balance"], "hold": False,
        })
    s["last_gen"] = now


def check(token):
    if token != TOKEN:
        raise HTTPException(status_code=403, detail="Unknown 'X-Token'")


@app.get("/personal/client-info")
def client_info(x_token: str = Header(...)):
    check(x_token)
    s = load()
    return {"clientId": "sim", "name": "Simulated Client",
            "jars": [{"id": JAR_ID, "title": "Simulated jar",
                      "currencyCode": 980, "balance": s["balance"]}]}


@app.get("/personal/statement/{account}/{t_from}/{t_to}")
def statement(account: str, t_from: int, t_to: int, x_token: str = Header(...)):
    check(x_token)
    s = load()
    generate(s)
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(s))
    out = [t for t in s["txs"] if t_from <= t["time"] <= t_to]
    return sorted(out, key=lambda t: -t["time"])
