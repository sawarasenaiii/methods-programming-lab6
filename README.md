# Лабораторная работа №6 — веб-программирование

Ляшенко Матвей Андреевич, группа 221141, вариант 9, лабораторная №6

| Уровень | № | Реализация |
| --- | --- | --- |
| Средний | 9 | Jinja2-шаблон со списком задач |
| Средний | 1 | Flask «Hello World» |
| Средний | 6 | FastAPI «Hello» |
| Повышенный | 9 | SQLAlchemy-модель задач |
| Повышенный | 2 | FastAPI + SQLite: CRUD API с созданием, чтением, изменением и удалением |

## REST API задач

| Метод | Путь | Действие |
| --- | --- | --- |
| GET | `/tasks` | список задач |
| POST | `/tasks` | создать задачу |
| GET | `/tasks/{task_id}` | получить задачу |
| PUT | `/tasks/{task_id}` | изменить название и статус |
| PATCH | `/tasks/{task_id}/complete` | отметить выполненной |
| DELETE | `/tasks/{task_id}` | удалить задачу |

## Запуск

```bash
python3 -m pip install -r requirements.txt
flask --app flask_app run
uvicorn fastapi_app:app --reload
python3 -m unittest discover -s tests -v
```

Flask доступен на `http://127.0.0.1:5000/`, FastAPI и Swagger - на
`http://127.0.0.1:8000/docs`. База `tasks.db` создаётся автоматически рядом
с приложением и исключена из Git.
