"""Assemblage des différentes couches de l'application."""

from pathlib import Path

from todolist.application.task_service import TaskService
from todolist.infrastructure.json_task_repository import JsonTaskRepository
from todolist.presentation.main_window import MainWindow
from todolist.presentation.task_controller import TaskController


def default_data_file() -> Path:
    """Retourne le fichier de données situé à la racine du projet."""
    return Path(__file__).resolve().parents[2] / "data" / "tasks.json"


def main() -> None:
    repository = JsonTaskRepository(default_data_file())
    service = TaskService(repository)
    window = MainWindow()
    controller = TaskController(service, window)
    window.set_controller(controller)
    controller.refresh()
    controller.start_auto_refresh()
    window.mainloop()
