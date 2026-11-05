import pytest
from datetime import date

from todolist.application.task_service import TaskService
from todolist.domain.exceptions import TaskNotFoundError
from todolist.domain.task import Task, TaskPriority


def test_service_adds_and_persists_task(service: TaskService, repository) -> None:
    task = service.add_task("Écrire les tests", "Avec pytest")

    assert service.list_tasks() == [task]
    assert repository.tasks == [task]


def test_service_updates_task(service: TaskService) -> None:
    task = service.add_task("Titre initial")

    updated = service.update_task(task.id, "Titre final", "Description")

    assert updated.title == "Titre final"
    assert updated.description == "Description"


def test_service_toggles_completion(service: TaskService) -> None:
    task = service.add_task("À valider")

    service.toggle_task(task.id)
    assert task.completed is True

    service.toggle_task(task.id)
    assert task.completed is False


def test_service_deletes_task(service: TaskService, repository) -> None:
    task = service.add_task("À supprimer")

    service.delete_task(task.id)

    assert service.list_tasks() == []
    assert repository.tasks == []


def test_service_rejects_unknown_task(service: TaskService) -> None:
    with pytest.raises(TaskNotFoundError):
        service.delete_task("unknown")


def test_service_reloads_tasks_changed_outside_the_application(
    service: TaskService, repository
) -> None:
    external_task = Task(title="Ajoutée depuis le fichier")
    repository.tasks = [external_task]

    tasks = service.reload_tasks()

    assert tasks == [external_task]


def test_service_adds_task_metadata(service: TaskService) -> None:
    task = service.add_task(
        "Livrer la version",
        category="Projet",
        priority=TaskPriority.URGENT,
        due_date=date(2026, 11, 5),
    )

    assert task.category == "Projet"
    assert task.priority is TaskPriority.URGENT
    assert task.due_date == date(2026, 11, 5)
