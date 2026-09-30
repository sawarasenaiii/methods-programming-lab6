"""Среднее задание №1: минимальное Flask-приложение."""

from flask import Flask

app = Flask(__name__)


@app.get("/")
def hello() -> str:
    return "Привет, Flask!"
