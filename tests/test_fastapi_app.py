import tempfile
import unittest
from pathlib import Path

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from database import Base
from fastapi_app import (
    TaskCreate,
    TaskUpdate,
    complete_task,
    create_task,
    delete_task,
    list_tasks,
    read_task,
    update_task,
)


class FastApiDatabaseTests(unittest.TestCase):
    def test_crud_functions_use_database(self):
        with tempfile.TemporaryDirectory() as directory:
            database_path = Path(directory) / "test.db"
            engine = create_engine(f"sqlite:///{database_path}")
            Base.metadata.create_all(engine)

            with Session(engine, expire_on_commit=False) as session:
                task = create_task(TaskCreate(title="Проверить API"), session)
                titles = [item.title for item in list_tasks(session)]
                self.assertEqual(titles, ["Проверить API"])
                self.assertEqual(read_task(task.id, session).id, task.id)

                updated = update_task(
                    task.id,
                    TaskUpdate(title="Сдать API", completed=False),
                    session,
                )
                self.assertEqual(updated.title, "Сдать API")
                self.assertTrue(complete_task(task.id, session).completed)

                delete_task(task.id, session)
                self.assertEqual(list_tasks(session), [])

                with self.assertRaises(HTTPException):
                    read_task(task.id, session)
                with self.assertRaises(HTTPException):
                    delete_task(task.id, session)
