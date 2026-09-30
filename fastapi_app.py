"""Задания №6, №9 и повышенные №2, №9 лабораторной работы №6."""

from fastapi import FastAPI


app = FastAPI(title="Задачи")


@app.get("/hello")
def hello() -> dict[str, str]:
    return {"message": "Привет, FastAPI!"}
