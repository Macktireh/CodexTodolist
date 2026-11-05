"""Coordination entre l'interface graphique et le service métier."""

from todolist.application.task_service import TaskService
from todolist.domain.exceptions import TodolistError
from todolist.presentation.main_window import MainWindow
from todolist.presentation.task_dialog import show_task_dialog


class TaskController:
    def __init__(self, service: TaskService, window: MainWindow) -> None:
        self._service = service
        self._window = window

    def refresh(self) -> None:
        all_tasks = self._service.list_tasks()
        self._window.render_overview(all_tasks)
        tasks = all_tasks
        selected_filter = self._window.selected_filter()
        query = self._window.search_text()

        if selected_filter == "À faire":
            tasks = [task for task in tasks if not task.completed]
        elif selected_filter == "Terminées":
            tasks = [task for task in tasks if task.completed]

        priority_filter = self._window.selected_priority_filter()
        priority_values = {
            "Urgentes": "urgent",
            "Hautes": "high",
            "Normales": "normal",
            "Basses": "low",
        }
        if priority_filter in priority_values:
            tasks = [task for task in tasks if task.priority.value == priority_values[priority_filter]]

        if query:
            tasks = [
                task
                for task in tasks
                if query in task.title.casefold()
                or query in task.description.casefold()
                or query in task.category.casefold()
            ]
        self._window.render_tasks(tasks, all_tasks)

    def reload(self, *, show_errors: bool = True) -> None:
        """Recharge le fichier de données puis actualise la liste affichée."""
        try:
            self._service.reload_tasks()
            self.refresh()
        except TodolistError as error:
            if show_errors:
                self._window.show_error(str(error))

    def start_auto_refresh(self, interval_ms: int = 2_000) -> None:
        """Surveille périodiquement les changements provenant du fichier JSON."""
        self._window.after(interval_ms, lambda: self._auto_refresh(interval_ms))

    def _auto_refresh(self, interval_ms: int) -> None:
        if self._window.auto_refresh_enabled():
            self.reload(show_errors=False)
        self._window.after(interval_ms, lambda: self._auto_refresh(interval_ms))

    def add_task(self) -> None:
        data = show_task_dialog(self._window, dialog_title="Nouvelle tâche")
        if data is None:
            return
        try:
            self._service.add_task(
                data.title,
                data.description,
                data.category,
                data.priority,
                data.due_date,
            )
            self.refresh()
        except TodolistError as error:
            self._window.show_error(str(error))

    def edit_selected(self) -> None:
        task_id = self._selected_id()
        if task_id is None:
            return
        self.edit_task(task_id)

    def edit_task(self, task_id: str) -> None:
        try:
            task = self._service.get_task(task_id)
            data = show_task_dialog(
                self._window,
                dialog_title="Modifier la tâche",
                title=task.title,
                description=task.description,
                category=task.category,
                priority=task.priority,
                due_date=task.due_date,
            )
            if data is not None:
                self._service.update_task(
                    task_id,
                    data.title,
                    data.description,
                    data.category,
                    data.priority,
                    data.due_date,
                )
                self.refresh()
        except TodolistError as error:
            self._window.show_error(str(error))

    def delete_selected(self) -> None:
        task_id = self._selected_id()
        if task_id is None:
            return
        try:
            task = self._service.get_task(task_id)
            if self._window.confirm_delete(task.title):
                self._service.delete_task(task_id)
                self.refresh()
        except TodolistError as error:
            self._window.show_error(str(error))

    def toggle_selected(self) -> None:
        task_id = self._selected_id()
        if task_id is None:
            return
        self.toggle_task(task_id)

    def toggle_task(self, task_id: str) -> None:
        try:
            self._service.toggle_task(task_id)
            self.refresh()
        except TodolistError as error:
            self._window.show_error(str(error))

    def _selected_id(self) -> str | None:
        task_id = self._window.selected_task_id()
        if task_id is None:
            self._window.request_selection()
        return task_id
