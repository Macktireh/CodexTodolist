"""Service applicatif chargé des cas d'utilisation liés aux tâches."""

from collections.abc import Iterable
from datetime import date

from todolist.domain.exceptions import TaskNotFoundError
from todolist.domain.task import Task, TaskPriority
from todolist.infrastructure.task_repository import TaskRepository


class TaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self._repository = repository
        self._tasks = repository.load_all()

    def list_tasks(self) -> list[Task]:
        return sorted(
            self._tasks,
            key=lambda task: (task.completed, -task.created_at.timestamp()),
        )

    def reload_tasks(self) -> list[Task]:
        """Recharge les tâches depuis le stockage persistant."""
        self._tasks = self._repository.load_all()
        return self.list_tasks()

    def add_task(
        self,
        title: str,
        description: str = "",
        category: str = "Général",
        priority: TaskPriority = TaskPriority.NORMAL,
        due_date: date | None = None,
    ) -> Task:
        task = Task(
            title=title,
            description=description,
            category=category,
            priority=priority,
            due_date=due_date,
        )
        self._tasks.append(task)
        self._save()
        return task

    def update_task(
        self,
        task_id: str,
        title: str,
        description: str = "",
        category: str = "Général",
        priority: TaskPriority = TaskPriority.NORMAL,
        due_date: date | None = None,
    ) -> Task:
        task = self.get_task(task_id)
        task.update(title, description, category, priority, due_date)
        self._save()
        return task

    def delete_task(self, task_id: str) -> None:
        task = self.get_task(task_id)
        self._tasks.remove(task)
        self._save()

    def set_task_completed(self, task_id: str, completed: bool) -> Task:
        task = self.get_task(task_id)
        task.set_completed(completed)
        self._save()
        return task

    def toggle_task(self, task_id: str) -> Task:
        task = self.get_task(task_id)
        return self.set_task_completed(task_id, not task.completed)

    def get_task(self, task_id: str) -> Task:
        try:
            return next(task for task in self._tasks if task.id == task_id)
        except StopIteration as error:
            raise TaskNotFoundError("Cette tâche n'existe plus.") from error

    def _save(self) -> None:
        self._repository.save_all(self._tasks)

    @property
    def tasks(self) -> Iterable[Task]:
        return tuple(self._tasks)
