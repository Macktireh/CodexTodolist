"""Objets partagés par les tests."""

from collections.abc import Iterable

import pytest

from todolist.application.task_service import TaskService
from todolist.domain.task import Task
from todolist.infrastructure.task_repository import TaskRepository


class InMemoryTaskRepository(TaskRepository):
    def __init__(self, tasks: Iterable[Task] = ()) -> None:
        self.tasks = list(tasks)

    def load_all(self) -> list[Task]:
        return list(self.tasks)

    def save_all(self, tasks: Iterable[Task]) -> None:
        self.tasks = list(tasks)


@pytest.fixture
def repository() -> InMemoryTaskRepository:
    return InMemoryTaskRepository()


@pytest.fixture
def service(repository: InMemoryTaskRepository) -> TaskService:
    return TaskService(repository)
