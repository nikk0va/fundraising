import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

def get_engine():
    u, p = os.getenv("POSTGRES_USER"), os.getenv("POSTGRES_PASSWORD")
    h, port, db = os.getenv("POSTGRES_HOST"), os.getenv("POSTGRES_PORT"), os.getenv("POSTGRES_DB")
    return create_engine(f"postgresql+psycopg://{u}:{p}@{h}:{port}/{db}")
