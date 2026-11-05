"""Contrat de persistance des tâches."""

from abc import ABC, abstractmethod
from collections.abc import Iterable

from todolist.domain.task import Task


class TaskRepository(ABC):
    @abstractmethod
    def load_all(self) -> list[Task]:
        """Charge toutes les tâches."""

    @abstractmethod
    def save_all(self, tasks: Iterable[Task]) -> None:
        """Enregistre toutes les tâches."""
