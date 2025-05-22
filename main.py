# main.py
import os
from uuid import uuid4
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
from dotenv import load_dotenv
import urllib.parse as urlparse
from prompt_engineering import generate_responses

load_dotenv()

app = FastAPI()

# Enable CORS for your Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("FRONTEND_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class QueryRequest(BaseModel):
    user_id: str
    query: str

def get_db_connection():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL environment variable is not set")

    urlparse.uses_netloc.append("postgres")
    parsed_url = urlparse.urlparse(db_url)
    print(parsed_url)
    return psycopg2.connect(
        dbname=parsed_url.path[1:],
        user=parsed_url.username,
        password=parsed_url.password,
        host=parsed_url.hostname,
        port=parsed_url.port,
        sslmode='require'  # <--- add this!
    )
@app.post("/generate")
def generate(q: QueryRequest):
    try:
        casual, formal = generate_responses(q.query)
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO prompts (id, user_id, query, casual_response, formal_response, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (str(uuid4()), q.user_id, q.query, casual, formal, datetime.utcnow())
            )
            conn.commit()
        conn.close()
        return {"casual_response": casual, "formal_response": formal}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
def history(user_id: str):
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT query, casual_response, formal_response, created_at
                  FROM prompts
                 WHERE user_id = %s
                 ORDER BY created_at DESC
                """,
                (user_id,)
            )
            rows = cur.fetchall()
        conn.close()
        return [
            {
                "query": q,
                "casual": c,
                "formal": f,
                "timestamp": t.isoformat(),
            }
            for q, c, f, t in rows
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
