from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="DevOps Project API")

tasks = []


class Task(BaseModel):
    title: str
    description: str


@app.get("/")
def root():
    return {"message": "API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/tasks")
def get_tasks():
    return tasks


@app.post("/tasks")
def create_task(task: Task):
    task_data = task.model_dump()
    tasks.append(task_data)
    return {"message": "task created", "task": task_data}
