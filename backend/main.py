from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS設定（Next.jsと通信可能にする）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要に応じて限定
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB接続関数
def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        ssl={"ssl": {}},  # ← これでSSL接続が有効化されます
    )

@app.get("/product/{prd_id}")
def get_product(prd_id: int):
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT NAME, PRICE FROM m_product_gataro WHERE PRD_ID = %s", (prd_id,))
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Product not found")
            return result
    finally:
        if conn:
            conn.close()
