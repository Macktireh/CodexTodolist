import json

import pytest

from todolist.domain.exceptions import StorageError
from todolist.domain.task import Task
from todolist.infrastructure.json_task_repository import JsonTaskRepository


def test_missing_file_returns_empty_list(tmp_path) -> None:
    repository = JsonTaskRepository(tmp_path / "tasks.json")

    assert repository.load_all() == []


def test_tasks_are_saved_and_loaded(tmp_path) -> None:
    file_path = tmp_path / "nested" / "tasks.json"
    repository = JsonTaskRepository(file_path)
    tasks = [Task(title="Première"), Task(title="Terminée", completed=True)]

    repository.save_all(tasks)
    restored = repository.load_all()

    assert restored == tasks
    assert json.loads(file_path.read_text(encoding="utf-8"))["version"] == 1


def test_invalid_json_raises_storage_error(tmp_path) -> None:
    file_path = tmp_path / "tasks.json"
    file_path.write_text("not json", encoding="utf-8")
    repository = JsonTaskRepository(file_path)

    with pytest.raises(StorageError, match="Impossible de lire"):
        repository.load_all()
