"""Persistance locale des tâches dans un fichier JSON."""

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from todolist.domain.exceptions import StorageError
from todolist.domain.task import Task
from todolist.infrastructure.task_repository import TaskRepository


class JsonTaskRepository(TaskRepository):
    FORMAT_VERSION = 1

    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path

    def load_all(self) -> list[Task]:
        if not self._file_path.exists():
            return []

        try:
            payload: dict[str, Any] = json.loads(
                self._file_path.read_text(encoding="utf-8")
            )
            raw_tasks = payload.get("tasks", [])
            if not isinstance(raw_tasks, list):
                raise ValueError("La propriété 'tasks' doit être une liste.")
            return [Task.from_dict(item) for item in raw_tasks]
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            raise StorageError(
                f"Impossible de lire le fichier de tâches : {self._file_path}"
            ) from error

    def save_all(self, tasks: Iterable[Task]) -> None:
        payload = {
            "version": self.FORMAT_VERSION,
            "tasks": [task.to_dict() for task in tasks],
        }
        temporary_file = self._file_path.with_suffix(self._file_path.suffix + ".tmp")

        try:
            self._file_path.parent.mkdir(parents=True, exist_ok=True)
            temporary_file.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            temporary_file.replace(self._file_path)
        except OSError as error:
            raise StorageError(
                f"Impossible d'enregistrer les tâches dans : {self._file_path}"
            ) from error
