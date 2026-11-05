from datetime import UTC, date

import pytest

from todolist.domain.exceptions import TaskValidationError
from todolist.domain.task import Task, TaskPriority


def test_task_normalizes_its_text() -> None:
    task = Task(title="  Préparer la démo  ", description="  Avant vendredi  ")

    assert task.title == "Préparer la démo"
    assert task.description == "Avant vendredi"
    assert task.created_at.tzinfo is UTC


@pytest.mark.parametrize("title", ["", "   "])
def test_task_rejects_empty_title(title: str) -> None:
    with pytest.raises(TaskValidationError, match="obligatoire"):
        Task(title=title)


def test_task_can_be_updated_and_completed() -> None:
    task = Task(title="Ancien titre")
    previous_update = task.updated_at

    task.update("Nouveau titre", "Une description")
    task.set_completed(True)

    assert task.title == "Nouveau titre"
    assert task.description == "Une description"
    assert task.completed is True
    assert task.updated_at >= previous_update


def test_task_round_trip_as_dictionary() -> None:
    original = Task(
        title="Persistante",
        description="Texte",
        category="Projet",
        priority=TaskPriority.HIGH,
        due_date=date(2026, 11, 8),
        completed=True,
    )

    restored = Task.from_dict(original.to_dict())

    assert restored == original


def test_legacy_task_gets_defaults_for_new_fields() -> None:
    original = Task(title="Ancienne tâche")
    data = original.to_dict()
    for field in ("category", "priority", "due_date"):
        data.pop(field)

    restored = Task.from_dict(data)

    assert restored.category == "Général"
    assert restored.priority is TaskPriority.NORMAL
    assert restored.due_date is None
