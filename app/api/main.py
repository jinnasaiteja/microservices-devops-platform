import os
import psycopg2
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="DevOps Project API")


class Task(BaseModel):
    title: str
    description: str


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        database=os.getenv("DB_NAME", "devopsdb"),
        user=os.getenv("DB_USER", "devopsuser"),
        password=os.getenv("DB_PASSWORD", "devopspass"),
    )


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            status VARCHAR(50) NOT NULL DEFAULT 'pending'
        )
        """
    )

    conn.commit()
    cur.close()
    conn.close()


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"message": "API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/tasks")
def get_tasks():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, title, description, status FROM tasks ORDER BY id")
    rows = cur.fetchall()

    tasks = []
    for row in rows:
        tasks.append(
            {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "status": row[3],
            }
        )

    cur.close()
    conn.close()
    return tasks


@app.post("/tasks")
def create_task(task: Task):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO tasks (title, description, status) VALUES (%s, %s, %s) RETURNING id",
        (task.title, task.description, "pending"),
    )
    task_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return {
        "message": "task created",
        "task": {
            "id": task_id,
            "title": task.title,
            "description": task.description,
            "status": "pending",
        },
    }
