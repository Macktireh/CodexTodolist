"""Modèle métier d'une tâche."""

from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from todolist.domain.exceptions import TaskValidationError


def utc_now() -> datetime:
    return datetime.now(UTC)


class TaskPriority(StrEnum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


@dataclass(slots=True)
class Task:
    title: str
    description: str = ""
    category: str = "Général"
    priority: TaskPriority = TaskPriority.NORMAL
    due_date: date | None = None
    completed: bool = False
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        self.title = self._validate_title(self.title)
        self.description = self.description.strip()
        self.category = self.category.strip() or "Général"
        if len(self.category) > 40:
            raise TaskValidationError("La catégorie ne peut pas dépasser 40 caractères.")
        if isinstance(self.priority, str):
            try:
                self.priority = TaskPriority(self.priority)
            except ValueError as error:
                raise TaskValidationError("La priorité sélectionnée n'est pas valide.") from error

    @staticmethod
    def _validate_title(title: str) -> str:
        normalized = title.strip()
        if not normalized:
            raise TaskValidationError("Le titre de la tâche est obligatoire.")
        if len(normalized) > 120:
            raise TaskValidationError("Le titre ne peut pas dépasser 120 caractères.")
        return normalized

    def update(
        self,
        title: str,
        description: str = "",
        category: str = "Général",
        priority: TaskPriority = TaskPriority.NORMAL,
        due_date: date | None = None,
    ) -> None:
        self.title = self._validate_title(title)
        self.description = description.strip()
        normalized_category = category.strip() or "Général"
        if len(normalized_category) > 40:
            raise TaskValidationError("La catégorie ne peut pas dépasser 40 caractères.")
        self.category = normalized_category
        try:
            self.priority = TaskPriority(priority)
        except ValueError as error:
            raise TaskValidationError("La priorité sélectionnée n'est pas valide.") from error
        self.due_date = due_date
        self.updated_at = utc_now()

    def set_completed(self, completed: bool) -> None:
        self.completed = completed
        self.updated_at = utc_now()

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "priority": self.priority.value,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "completed": self.completed,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Task":
        return cls(
            id=str(data["id"]),
            title=str(data["title"]),
            description=str(data.get("description", "")),
            category=str(data.get("category", "Général")),
            priority=TaskPriority(str(data.get("priority", TaskPriority.NORMAL.value))),
            due_date=(
                date.fromisoformat(str(data["due_date"]))
                if data.get("due_date")
                else None
            ),
            completed=bool(data.get("completed", False)),
            created_at=datetime.fromisoformat(str(data["created_at"])),
            updated_at=datetime.fromisoformat(str(data["updated_at"])),
        )
