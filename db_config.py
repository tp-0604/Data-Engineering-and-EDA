import os
from dotenv import load_dotenv
import psycopg2
from sqlalchemy import create_engine

load_dotenv()

PG_HOST = os.getenv("PG_HOST")
PG_DBNAME = os.getenv("PG_DBNAME")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_PORT = os.getenv("PG_PORT")

def get_psycopg_conn():
    return psycopg2.connect(
        host=PG_HOST,
        dbname=PG_DBNAME,
        user=PG_USER,
        password=PG_PASSWORD,
        port=PG_PORT,
        sslmode="require"
    )

def get_engine():
    return create_engine(
        f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DBNAME}?sslmode=require"
    )
