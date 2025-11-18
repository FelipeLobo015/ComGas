import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

USER = os.getenv("USER_DB")
PASSWORD = os.getenv("PASSWORD_DB")
HOST = os.getenv("HOST_DB")
PORT = os.getenv("PORT_DB")
DBNAME = os.getenv("DBNAME_DB")

def conectar():
    try:
        conn = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            dbname=DBNAME
        )
        return conn
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco: {e}")
        return None
