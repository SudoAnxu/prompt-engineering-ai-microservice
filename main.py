# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime
import psycopg2
import os
from dotenv import load_dotenv
from prompt_engineering import generate_responses

load_dotenv()
app = FastAPI()

class QueryRequest(BaseModel):
    user_id: str
    query: str

def get_db_connection():
    print("PGHOST:", os.getenv("PGHOST"))
    print("PGDATABASE:", os.getenv("PGDATABASE"))
    print("PGUSER:", os.getenv("PGUSER"))
    print("PGPASSWORD:", os.getenv("PGPASSWORD"))
    return psycopg2.connect(
        host=os.getenv("PGHOST"),
        database=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD")
    )

@app.post("/generate")
def generate(query_req: QueryRequest):
    try:
        casual, formal = generate_responses(query_req.query)
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO prompts (id, user_id, query, casual_response, formal_response, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (str(uuid4()), query_req.user_id, query_req.query, casual, formal, datetime.utcnow()))
        conn.commit()
        cur.close()
        conn.close()
        return {"casual_response": casual, "formal_response": formal}
    except Exception as e:
        print("Error in /generate:", e)
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/history")
def history(user_id: str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT query, casual_response, formal_response, created_at
        FROM prompts
        WHERE user_id = %s ORDER BY created_at DESC
    """, (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"query": q, "casual": c, "formal": f, "timestamp": t.isoformat()} for q, c, f, t in rows]
