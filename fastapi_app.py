"""Задания №6, №9 и повышенные №2, №9 лабораторной работы №6."""

from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import Base, SessionLocal, Task, engine


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)


class TaskUpdate(TaskCreate):
    completed: bool


class TaskView(TaskCreate):
    id: int
    completed: bool


def get_session():
    with SessionLocal() as session:
        yield session


SessionDependency = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title="Задачи", lifespan=lifespan)


def find_task(task_id: int, session: Session) -> Task:
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(404, "Задача не найдена")
    return task


@app.get("/hello")
def hello() -> dict[str, str]:
    return {"message": "Привет, FastAPI!"}


@app.get("/tasks", response_model=list[TaskView])
def list_tasks(session: SessionDependency) -> list[Task]:
    return list(session.scalars(select(Task).order_by(Task.id)))


@app.post("/tasks", response_model=TaskView, status_code=201)
def create_task(payload: TaskCreate, session: SessionDependency) -> Task:
    task = Task(title=payload.title)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.get("/tasks/{task_id}", response_model=TaskView)
def read_task(task_id: int, session: SessionDependency) -> Task:
    return find_task(task_id, session)


@app.put("/tasks/{task_id}", response_model=TaskView)
def update_task(
    task_id: int, payload: TaskUpdate, session: SessionDependency
) -> Task:
    task = find_task(task_id, session)
    task.title = payload.title
    task.completed = payload.completed
    session.commit()
    session.refresh(task)
    return task


@app.patch("/tasks/{task_id}/complete", response_model=TaskView)
def complete_task(task_id: int, session: SessionDependency) -> Task:
    task = find_task(task_id, session)
    task.completed = True
    session.commit()
    session.refresh(task)
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, session: SessionDependency) -> None:
    task = find_task(task_id, session)
    session.delete(task)
    session.commit()
